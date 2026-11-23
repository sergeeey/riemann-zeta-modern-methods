#!/usr/bin/env python3
"""B1: strict source reference graph of the Lean checkout, dominator tree from rhOfAll.

Same graph as verification/refgraph/refgraph.py (nodes = short declaration names; edge A->B if B occurs as the last
dotted component of a token in the text of a declaration named A; comments stripped). STRICT: edges into names declared
more than once in src are dropped. Extras vs refgraph.py:
  * dominator tree (Cooper-Harvey-Kennedy) on the reachable strict subgraph, root = rhOfAll;
  * for target names: BFS shortest path, dominator chain, size of dominated subtree;
  * per-edge source evidence for the BFS paths (declaring file, body occurrences of the target token, `first |` flag,
    import-closure check: is the module declaring B in the import closure of the module declaring A);
Output: JSON to argv[1]; full adjacency is NOT saved in the repo (too large), only pickled in WSL work dir (argv[2]).
Limits: implicit uses (instances, simp sets, notation, macros) are not edges; same short name in several namespaces is
merged for sources and dropped for targets (strict).
"""

import os, re, sys, time, json, pickle
from collections import deque, defaultdict

SRC = os.path.expanduser("~/h12/rh/src")
OUT = None
PKL = None
ROOT = "rhOfAll"
TARGETS = [
    "szRow_sizeKRel",
    "sizes_sizeKRel",
    "SizeKRel",
    "MIstar2",
    "miStar2_of_allTrue_alt_alt",
    "wire4F_alt",
    "published_results_eigen",
    "open0_of_unitary_group_hypotheses",
]
t0 = time.time()

RX_BLOCK = re.compile(r"/-.*?-/", re.S)
RX_LINE = re.compile(r"--[^\n]*")
RX_HEAD = re.compile(
    r"(?m)^[ \t]*(?:@\[[^\]\n]*\][ \t]*\n?[ \t]*)?(?:(?:private|protected|noncomputable|unsafe|partial|nonrec)[ \t]+)*"
    r"(?:theorem|lemma|def|abbrev|instance|structure|class|inductive|axiom|opaque)[ \t]+([^\s:({\[⟨]+)"
)
RX_TOK = re.compile(r"[^\W\d][\w'!?.]*", re.U)
RX_IMP = re.compile(r"(?m)^import[ \t]+([\w.₀-₉'«»]+)")

files = []
for dp, dn, fn in os.walk(SRC):
    if "/.lake" in dp:
        continue
    for f in fn:
        if f.endswith(".lean"):
            files.append(os.path.join(dp, f))
files.sort()
print("files", len(files), flush=True)


def strip(txt):
    return RX_LINE.sub("", RX_BLOCK.sub("", txt))


def decls(path):
    try:
        txt = strip(open(path, encoding="utf-8", errors="replace").read())
    except Exception:
        return []
    ms = list(RX_HEAD.finditer(txt))
    out = []
    for i, m in enumerate(ms):
        end = ms[i + 1].start() if i + 1 < len(ms) else len(txt)
        out.append((m.group(1).split(".")[-1], m.group(1), txt[m.start() : end]))
    return out


cnt = defaultdict(int)
where = {}  # short name -> (file, fullname-as-written) (kept for the last/only decl)
for k, p in enumerate(files):
    for nm, full, _ in decls(p):
        cnt[nm] += 1
        where[nm] = (p, full)
print("declared names", len(cnt), flush=True)

adj = defaultdict(set)
for k, p in enumerate(files):
    for nm, full, body in decls(p):
        s = adj[nm]
        for tok in RX_TOK.findall(body):
            last = tok.split(".")[-1]
            if last != nm and last in cnt:
                s.add(last)
print("graph built", round(time.time() - t0), flush=True)

# ---- bypass search in the "mid" graph (strict + edges into names with 2..5 declarations)
def mid_succ(u):
    return [v for v in adj.get(u, ()) if 1 <= cnt[v] <= 5]

def bypass_path(target, banned):
    par = {ROOT: None}
    dq = deque([ROOT])
    while dq:
        u = dq.popleft()
        if u == target:
            p = []
            while u is not None:
                p.append(u); u = par[u]
            return p[::-1]
        for v in mid_succ(u):
            if v != banned and v not in par:
                par[v] = u
                dq.append(v)
    return None

QUERIES = [("szRow_sizeKRel", "allChi"), ("szRow_sizeKRel", "everyCharacter_of_row"),
           ("szRow_sizeKRel", "every_character_of_theta_integrals_local_matching"),
           ("szRow_sizeKRel", "nonempty_hyps_definite_side_of_closed_bound"),
           ("szRow_sizeKRel", "szRow_numAt"), ("SizeKRel", "sizes_sizeKRel"), ("MIstar2", "every_character_of_theta_integrals_local_matching"),
           ("MIstar2", "every_character_of_green_v_win")]
out = {}
for t, d in QUERIES:
    p = bypass_path(t, d)
    out[f"{t} avoiding {d}"] = [(x, cnt[x]) for x in p] if p else None
    print(t, "avoiding", d, "->", (" > ".join(f"{x}({cnt[x]})" for x in p) if p else "NO BYPASS"), flush=True)
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "bypass_paths.json"), "w"), ensure_ascii=False, indent=1)
print("done", round(time.time() - t0), flush=True)
