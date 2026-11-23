import json, sys, os

D = os.path.dirname(os.path.abspath(__file__))
r = json.load(open(os.path.join(D, "skeleton_result.json"), encoding="utf-8"))
print("reachable", r["strict_reachable"], "iters", r["dominator_iterations"])
for t, v in r["targets"].items():
    if not v:
        print("##", t, "NOT REACHED")
        continue
    print("##", t)
    print(" bfs_len", len(v["bfs_path"]), " dom_chain_len", len(v["dominator_chain"]))
    print(
        " DOM:", " > ".join(f"{c}[{v['dominated_subtree_size'][c]}]" for c in v["dominator_chain"])
    )
    print(" doms not on bfs path:", v["dominators_not_on_bfs_path"])
    bad = [
        e
        for e in v["edge_evidence"]
        if not e["tokens_in_A_body"] or not (e["B_module_in_import_closure_of_A"])
    ]
    fa = [e["A"] + "->" + e["B"] for e in v["edge_evidence"] if e["A_has_first_alt"]]
    print(
        " edges w/o token or import-closure:",
        [
            (e["A"], e["B"], e["tokens_in_A_body"], e["B_module_in_import_closure_of_A"])
            for e in bad
        ],
    )
    print(" edges whose A has `first |`:", fa)
print("## top dominators")
for x in r["top_dominators_by_subtree"][:25]:
    print(x["depth"], x["size"], x["name"], "<-", x["idom"], x["file"].split("/")[-1])
