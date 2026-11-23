"""Print the top children (by dominated-subtree size) of selected nodes in the strict dominator tree.
Reads ~/h12/work/skel_dom.pkl written by skel_graph.py (not stored in the repo: large)."""

import os, pickle, sys

d = pickle.load(open(os.path.expanduser("~/h12/work/skel_dom.pkl"), "rb"))
names, idom, succ = d["names"], d["idom"], d["succ"]
N = len(names)
ids = {n: i for i, n in enumerate(names)}
kids = [[] for _ in range(N)]
for u in range(1, N):
    kids[idom[u]].append(u)
size = [1] * N
# subtree sizes (post-order by decreasing BFS index is not a topological order of the dom tree, so iterate)
order = []
st = [0]
while st:
    u = st.pop()
    order.append(u)
    st.extend(kids[u])
for u in reversed(order):
    for k in kids[u]:
        size[u] += size[k]
SEL = sys.argv[1:] or [
    "rhOfAll",
    "allChi",
    "everyCharacter",
    "everyCharacter_of_row",
    "every_character_of_literature_of_vWin",
    "every_character_of_theta_integrals_local_matching",
    "nonempty_hyps_definite_side_of_closed_bound",
    "hypotheses_nonempty_of_unramified_exponents_alt",
    "open0_of_unitary_group_hypotheses",
    "vwin_of_row",
    "every_character_of_green_v_win",
]
for s in SEL:
    if s not in ids:
        print("##", s, "absent")
        continue
    ks = sorted(kids[ids[s]], key=lambda k: -size[k])[:9]
    print(f"## {s} (subtree {size[ids[s]]}, {len(kids[ids[s]])} dom-children)")
    for k in ks:
        print(f"   {size[k]:7d}  {names[k]}")
