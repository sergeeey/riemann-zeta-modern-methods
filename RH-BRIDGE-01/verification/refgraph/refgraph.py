#!/usr/bin/env python3
"""Source-level reference graph of the Lean checkout; forward reachability from riemannHypothesis.

Nodes: short declaration names (last component). Edge A->B: B (declared somewhere in src) occurs as a
word (last dotted component) in the text of a declaration named A. Comments are stripped.
Limits (kept explicit): instances/simp lemmas/notation/macros used implicitly are NOT edges;
same short name in several namespaces is merged (loose) or dropped as a target (strict).
"""

import os, re, sys, time, json
from collections import deque, defaultdict

SRC = os.path.expanduser("~/h12/rh/src")
OUT = sys.argv[1]
t0 = time.time()

RX_BLOCK = re.compile(r"/-.*?-/", re.S)
RX_LINE = re.compile(r"--[^\n]*")
RX_HEAD = re.compile(
    r"(?m)^[ \t]*(?:@\[[^\]\n]*\][ \t]*\n?[ \t]*)?(?:(?:private|protected|noncomputable|unsafe|partial|nonrec)[ \t]+)*"
    r"(?:theorem|lemma|def|abbrev|instance|structure|class|inductive|axiom|opaque)[ \t]+([^\s:({\[⟨]+)"
)
RX_TOK = re.compile(r"[^\W\d][\w'!?.]*", re.U)

files = []
for dp, dn, fn in os.walk(SRC):
    if "/.lake" in dp:
        continue
    for f in fn:
        if f.endswith(".lean"):
            files.append(os.path.join(dp, f))
files.sort()
print("files", len(files), flush=True)


def decls(path):
    try:
        txt = open(path, encoding="utf-8", errors="replace").read()
    except Exception:
        return []
    txt = RX_LINE.sub("", RX_BLOCK.sub("", txt))
    ms = list(RX_HEAD.finditer(txt))
    out = []
    for i, m in enumerate(ms):
        end = ms[i + 1].start() if i + 1 < len(ms) else len(txt)
        nm = m.group(1).split(".")[-1]
        out.append((nm, txt[m.start() : end]))
    return out


# pass 1: declared short names and counts
cnt = defaultdict(int)
for k, p in enumerate(files):
    for nm, _ in decls(p):
        cnt[nm] += 1
    if k % 20000 == 0:
        print("pass1", k, len(cnt), round(time.time() - t0), flush=True)
print("declared names", len(cnt), "total decls", sum(cnt.values()), flush=True)

# pass 2: edges
adj = defaultdict(set)  # name -> set(names)
for k, p in enumerate(files):
    for nm, body in decls(p):
        s = adj[nm]
        for tok in RX_TOK.findall(body):
            last = tok.split(".")[-1]
            if last != nm and last in cnt:
                s.add(last)
    if k % 20000 == 0:
        print("pass2", k, round(time.time() - t0), flush=True)
print("edges", sum(len(v) for v in adj.values()), flush=True)


def bfs(starts, strict):
    par = {}
    dq = deque()
    for s in starts:
        if s in cnt:
            par[s] = None
            dq.append(s)
    while dq:
        u = dq.popleft()
        for v in adj.get(u, ()):
            if strict and cnt[v] != 1:
                continue
            if v not in par:
                par[v] = u
                dq.append(v)
    return par


def path(par, t):
    if t not in par:
        return None
    p = []
    while t is not None:
        p.append(t)
        t = par[t]
    return p[::-1]


names = (
    "SizeKRel szRow_sizeKRel sizes_sizeKRel SizesAt SizeN SizeM SizeK SizeT f_mul_m_le MIstar2 MIid MIUnit2 AuNZ MIDat "
    "miStar2_of_anchored miStar2_of_families miStar2_of_allTrue miStar2_of_allTrue_alt_alt joint_star_product_nonvanishing "
    "isometric_periods_of_unit_hypotheses exists_zeta_pairing_factors_through_periods RowMultiplicityCondition RowsAtSelAlt "
    "IndefiniteRealisationConstantBounds wire4F_alt wire_sel_alt open0_of_unitary_group_hypotheses published_results_eigen "
    "zeroFree_of_rpow_window lemmaL windowHyp_of_rpow harishChandraFinite OpenParameterStatements allRows_of_open0_alt "
    "row_rRows_of_parts_alt row_rRows_stage0_alt ElevenLe szTh rankBudget CountsIrreducibilityConstants Win_at RamRank_at "
    "ChCode_at ramShare_at_of frame_at_of DesignS"
).split()
found = set(
    """DesignS CountsIrreducibilityConstants harishChandraFinite SizesAt SizeT IndefiniteRealisationConstantBounds
zeroFree_of_rpow_window wire_sel_alt wire4F_alt windowHyp_of_rpow szTh szRow_sizeKRel sizes_sizeKRel row_rRows_stage0_alt
row_rRows_of_parts_alt rankBudget ramShare_at_of published_results_eigen open0_of_unitary_group_hypotheses miStar2_of_anchored
miStar2_of_allTrue_alt_alt lemmaL isometric_periods_of_unit_hypotheses frame_at_of exists_zeta_pairing_factors_through_periods
allRows_of_open0_alt Win_at SizeN SizeM SizeKRel SizeK RowsAtSelAlt RowMultiplicityCondition RamRank_at OpenParameterStatements
MIstar2 MIid MIUnit2 MIDat ElevenLe ChCode_at AuNZ""".split()
)

S_RH = ["rhOfAll"]
S_5 = ["rhOfAll", "allChi", "claimAll", "critAll"]
res = {}
for label, starts in (("RH", S_RH), ("FIVE", S_5)):
    for strict in (False, True):
        par = bfs(starts, strict)
        key = f"{label}_{'strict' if strict else 'loose'}"
        res[key] = {"reachable_nodes": len(par)}
        res[key]["targets"] = {n: path(par, n) for n in names}
res["decl_count"] = {n: cnt.get(n, 0) for n in names}
res["in_export"] = {n: (n in found) for n in names}
json.dump(res, open(OUT, "w"), ensure_ascii=False, indent=1)
print("done", round(time.time() - t0), flush=True)
