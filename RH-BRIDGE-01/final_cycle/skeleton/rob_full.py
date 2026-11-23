import json, os
D = os.path.dirname(os.path.abspath(__file__))
r = json.load(open(os.path.join(D, "skeleton_result.json"), encoding="utf-8"))
v = r["targets"]["miStar2_of_allTrue_alt_alt"]
for d, s in v["mid_graph_robustness"].items():
    print(("SURVIVES " if s.startswith("still") else "BYPASS   "), d)
