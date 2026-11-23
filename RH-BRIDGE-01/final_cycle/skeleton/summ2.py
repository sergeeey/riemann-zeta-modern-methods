import json, os

D = os.path.dirname(os.path.abspath(__file__))
r = json.load(open(os.path.join(D, "skeleton_result.json"), encoding="utf-8"))
print(
    "dropped ambiguous edges from reachable:",
    r.get("strict_dropped_edges_from_reachable_into_ambiguous_names"),
)
for t, v in r["targets"].items():
    if not v:
        continue
    rb = v.get("mid_graph_robustness", {})
    keep = [d for d, s in rb.items() if s.startswith("still")]
    byp = [d for d, s in rb.items() if s.startswith("BYPASS")]
    print(
        "##",
        t,
        "| chain",
        len(v["dominator_chain"]),
        "| survive mid-graph:",
        keep,
        "| bypass:",
        byp,
    )
print("---- heads of dominators (<=330 chars)")
for c, d in sorted(r["dominator_decls"].items(), key=lambda kv: kv[1]["depth"]):
    print(f"[{d['depth']}] {c} ({d['file'].split('/')[-1]}; sub={d['subtree']})")
    print("    ", d.get("head", "")[:330])
