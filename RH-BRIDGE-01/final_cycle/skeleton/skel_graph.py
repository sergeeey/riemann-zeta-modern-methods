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
OUT = sys.argv[1]
PKL = sys.argv[2] if len(sys.argv) > 2 else None
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


# ---- strict reachable subgraph
def strict_succ(u):
    return [v for v in adj.get(u, ()) if cnt[v] == 1]


par = {ROOT: None}
dq = deque([ROOT])
order_bfs = [ROOT]
while dq:
    u = dq.popleft()
    for v in strict_succ(u):
        if v not in par:
            par[v] = u
            dq.append(v)
            order_bfs.append(v)
print("strict reachable", len(par), flush=True)

# ---- dominators (Cooper-Harvey-Kennedy)
ids = {n: i for i, n in enumerate(order_bfs)}
names = order_bfs
N = len(names)
succ = [[ids[v] for v in strict_succ(names[i]) if v in ids] for i in range(N)]
pred = [[] for _ in range(N)]
for u in range(N):
    for v in succ[u]:
        pred[v].append(u)
# reverse postorder via iterative DFS
visited = [False] * N
post = []
stack = [(0, iter(succ[0]))]
visited[0] = True
while stack:
    u, it = stack[-1]
    adv = False
    for v in it:
        if not visited[v]:
            visited[v] = True
            stack.append((v, iter(succ[v])))
            adv = True
            break
    if not adv:
        post.append(u)
        stack.pop()
rpo = post[::-1]
rpo_num = [0] * N
for i, u in enumerate(rpo):
    rpo_num[u] = i
idom = [-1] * N
idom[0] = 0


def intersect(a, b):
    while a != b:
        while rpo_num[a] > rpo_num[b]:
            a = idom[a]
        while rpo_num[b] > rpo_num[a]:
            b = idom[b]
    return a


changed = True
it_count = 0
while changed:
    changed = False
    it_count += 1
    for u in rpo[1:]:
        new = -1
        for p in pred[u]:
            if idom[p] != -1:
                new = p if new == -1 else intersect(p, new)
        if new != idom[u]:
            idom[u] = new
            changed = True
print("dominator iterations", it_count, round(time.time() - t0), flush=True)

# subtree sizes in the dominator tree
size = [1] * N
for u in reversed(rpo):
    if u != 0:
        size[idom[u]] += size[u]


def dom_chain(name):
    i = ids[name]
    ch = []
    while True:
        ch.append(names[i])
        if i == 0:
            break
        i = idom[i]
    return ch[::-1]


def bfs_path(name):
    p = []
    t = name
    while t is not None:
        p.append(t)
        t = par[t]
    return p[::-1]


# ---- import closure helper
mod_of = {}
for p in files:
    rel = os.path.relpath(p, SRC)[:-5].replace(os.sep, ".")
    mod_of[rel] = p
imp_cache = {}


def imports(p):
    if p not in imp_cache:
        try:
            t = open(p, encoding="utf-8", errors="replace").read()
        except Exception:
            t = ""
        imp_cache[p] = [mod_of[m] for m in RX_IMP.findall(t) if m in mod_of]
    return imp_cache[p]


def closure(p):
    seen = {p}
    st = [p]
    while st:
        x = st.pop()
        for y in imports(x):
            if y not in seen:
                seen.add(y)
                st.append(y)
    return seen


def edge_evidence(a, b):
    fa, fulla = where[a]
    fb, fullb = where[b]
    txt = strip(open(fa, encoding="utf-8", errors="replace").read())
    body = None
    for nm, full, bd in decls(fa):
        if nm == a:
            body = bd
    occ = []
    if body is not None:
        for tok in RX_TOK.findall(body):
            if tok.split(".")[-1] == b:
                occ.append(tok)
    first_alt = bool(body and re.search(r"first\s*\|", body))
    inclos = fb in closure(fa) or fb == fa
    return {
        "A": a,
        "A_file": os.path.relpath(fa, SRC),
        "A_decl": fulla,
        "B": b,
        "B_file": os.path.relpath(fb, SRC),
        "B_decl": fullb,
        "tokens_in_A_body": sorted(set(occ))[:4],
        "A_has_first_alt": first_alt,
        "B_module_in_import_closure_of_A": inclos,
        "same_file": fb == fa,
    }


res = {
    "root": ROOT,
    "strict_reachable": len(par),
    "total_declared_names": len(cnt),
    "dominator_iterations": it_count,
    "targets": {},
}
for t in TARGETS:
    if t not in ids:
        res["targets"][t] = None
        continue
    path = bfs_path(t)
    chain = dom_chain(t)
    ev = [edge_evidence(path[i], path[i + 1]) for i in range(len(path) - 1)]
    res["targets"][t] = {
        "bfs_path": path,
        "dominator_chain": chain,
        "dominated_subtree_size": {c: size[ids[c]] for c in chain},
        "dominators_not_on_bfs_path": [c for c in chain if c not in path],
        "edge_evidence": ev,
    }
# top dominators by subtree size close to the root (depth<=12) for orientation
depth = [0] * N
for u in rpo[1:]:
    depth[u] = depth[idom[u]] + 1
top = sorted(range(N), key=lambda i: -size[i])[:60]
res["top_dominators_by_subtree"] = [
    {
        "name": names[i],
        "depth": depth[i],
        "size": size[i],
        "idom": names[idom[i]] if i else None,
        "file": os.path.relpath(where[names[i]][0], SRC),
    }
    for i in top
]
# immediate dominators path nodes: file + full decl for every dominator in any chain
all_dom = sorted({c for t in res["targets"].values() if t for c in t["dominator_chain"]})
res["dominator_decls"] = {
    c: {
        "file": os.path.relpath(where[c][0], SRC),
        "decl_as_written": where[c][1],
        "subtree": size[ids[c]],
        "depth": depth[ids[c]],
    }
    for c in all_dom
}


# ---- declaration heads (statement as written, whitespace-normalised) for all chain dominators
def head_of(nm):
    f, full = where[nm]
    for n2, full2, bd in decls(f):
        if n2 == nm:
            h = re.sub(r"\s+", " ", bd)
            cut = h.find(":=")
            return h[: (cut if 0 < cut < 700 else 700)]
    return ""


for c in all_dom:
    res["dominator_decls"][c]["head"] = head_of(c)


# ---- robustness: strict graph + edges into names with 2..5 declarations ("mid" graph).
def mid_succ(u):
    return [v for v in adj.get(u, ()) if 1 <= cnt[v] <= 5]


def reach_avoiding(target, banned):
    seen = {ROOT}
    dq2 = deque([ROOT])
    while dq2:
        u = dq2.popleft()
        if u == target:
            return True
        for v in mid_succ(u):
            if v != banned and v not in seen:
                seen.add(v)
                dq2.append(v)
    return target in seen


dropped = sum(1 for u in names for v in adj.get(u, ()) if cnt[v] > 1)
res["strict_dropped_edges_from_reachable_into_ambiguous_names"] = dropped
for t, v in res["targets"].items():
    if not v:
        continue
    surv = {}
    for d in v["dominator_chain"][1:-1]:
        surv[d] = (
            "BYPASS_EXISTS_in_mid_graph" if reach_avoiding(t, d) else "still_dominator_in_mid_graph"
        )
    v["mid_graph_robustness"] = surv
print("robustness done", round(time.time() - t0), flush=True)
json.dump(res, open(OUT, "w"), ensure_ascii=False, indent=1)
if PKL:
    pickle.dump({"names": names, "idom": idom, "succ": succ}, open(PKL, "wb"))
print("done", round(time.time() - t0), flush=True)
