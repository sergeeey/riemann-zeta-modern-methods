"""For every edge on the BFS paths of the targets, print the first source line of A's file that names B (as a word),
so a human can see the syntactic reference. Writes edge_lines.out. Runs in WSL (reads ~/h12/rh/src)."""

import json, os, re

D = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.expanduser("~/h12/rh/src")
r = json.load(open(os.path.join(D, "skeleton_result.json"), encoding="utf-8"))
out = []
seen = set()
for t, v in r["targets"].items():
    if not v:
        continue
    out.append(f"##### path to {t}")
    for e in v["edge_evidence"]:
        key = (e["A"], e["B"])
        a, b = e["A"], e["B"]
        txt = (
            open(os.path.join(SRC, e["A_file"]), encoding="utf-8", errors="replace")
            .read()
            .splitlines()
        )
        # restrict to A's declaration region: from the head line mentioning A to the next top-level decl
        start = None
        for i, ln in enumerate(txt):
            if re.search(
                r"\b(theorem|def|lemma|abbrev|structure|class|inductive)\s+\S*\b"
                + re.escape(a)
                + r"\b",
                ln,
            ):
                start = i
                break
        hit = None
        if start is not None:
            for j in range(start, min(start + 400, len(txt))):
                if j > start and re.match(
                    r"^(theorem|def|lemma|abbrev|structure|class|inductive|end |namespace|section)",
                    txt[j],
                ):
                    break
                if re.search(r"(?<![\w'])" + re.escape(b) + r"(?![\w'])", txt[j]):
                    hit = (j + 1, txt[j].strip())
                    break
        tag = "" if key not in seen else "(dup) "
        seen.add(key)
        out.append(
            f"{tag}{a} -> {b} | {e['A_file'].split('/')[-1]}:{hit[0] if hit else '?'} | {(hit[1][:200] if hit else 'NO LINE FOUND IN DECL REGION')} | closure={e['B_module_in_import_closure_of_A']}"
        )
open(os.path.join(D, "edge_lines.out"), "w", encoding="utf-8").write("\n".join(out) + "\n")
print(len(out), "lines")
