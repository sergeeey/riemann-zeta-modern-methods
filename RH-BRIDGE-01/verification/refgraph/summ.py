import json, os, sys

r = json.load(open(os.path.expanduser("~/h12/work/refgraph_result.json")))
for k in ["RH_loose", "RH_strict", "FIVE_loose", "FIVE_strict"]:
    print(k, r[k]["reachable_nodes"])
print("name | decls_in_src | in_export | RH_strict | RH_loose | FIVE_loose (path length or -)")
for n, c in r["decl_count"].items():
    f = lambda k: len(r[k]["targets"][n]) if r[k]["targets"][n] else "-"
    print(n, c, r["in_export"][n], f("RH_strict"), f("RH_loose"), f("FIVE_loose"))
if len(sys.argv) > 1:
    for n in sys.argv[1:]:
        for k in ("RH_strict", "RH_loose"):
            print(k, n, " -> ".join(r[k]["targets"][n] or ["UNREACHED"]))
