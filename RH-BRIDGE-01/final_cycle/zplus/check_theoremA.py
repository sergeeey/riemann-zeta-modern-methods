"""Numerical check (NUMERICALLY_CHECKED, not a proof) for A2.

Hypotheses = exactly those of Lean FrameLA1 (Formalism/HarderNarasimhan/StatementFrameF.lean):
  sum ||K_i - I||_HS^2 <= e R,  e <= 1/4;  Tr Q^2 <= (1+eta) (Tr Q)^2 / D;  sum codim E_i <= alpha R.
Claim A (independent review, re-derived on paper by the coordinator of this cycle):
  x - sqrt(eta x (1-x)) <= a := (alpha + sqrt(alpha e)) / (1 - sqrt e),   x = w/D,
  hence x <= eta + 2a, and eta + 2a <= eta + 4 alpha + 4 sqrt e   (original Lean/Zhang bound) when e <= 1/4.
Here e, eta, alpha are the ACTUAL values of each random instance (tightest admissible parameters).
Part 2: size of the improvement of the sqrt(e) part after integration over tau in [0,H] with alpha(tau)=u/(u+tau).
"""

import numpy as np, math, sys

rng = np.random.default_rng(20261123)


def instance():
    D = int(rng.integers(4, 40))
    m = int(rng.integers(1, 6))
    rs = [int(rng.integers(1, D + 1)) for _ in range(m)]
    noise = rng.choice([0.0, 0.02, 0.05, 0.15])
    Bs, gs = [], []
    for r in rs:
        G = rng.normal(size=(D, r)) + 1j * rng.normal(size=(D, r))
        Qm, _ = np.linalg.qr(G)  # D x r isometry
        Qm = Qm[:, :r]
        Bs.append(
            Qm + noise * (rng.normal(size=(D, r)) + 1j * rng.normal(size=(D, r))) / math.sqrt(D)
        )
        gs.append(1.0)
    return D, rs, Bs, gs


def run(N=4000):
    bad = 0
    cnt = 0
    worst = -1e9
    improve = []
    for _ in range(N):
        D, rs, Bs, gs = instance()
        R = sum(rs)
        Ks = [g * B.conj().T @ B for B, g in zip(Bs, gs)]
        hs = sum(np.linalg.norm(K - np.eye(K.shape[0]), "fro") ** 2 for K in Ks)
        e = hs / R
        if e > 0.25:
            continue
        Q = sum(g * B @ B.conj().T for B, g in zip(Bs, gs))
        t = np.trace(Q).real
        eta = max(0.0, (np.trace(Q @ Q).real) * D / t**2 - 1)
        # random subspaces E_i with random codims
        cols = []
        m_tot = 0
        for B, r in zip(Bs, rs):
            k = int(rng.integers(0, r + 1))  # codim
            m_tot += k
            if r - k > 0:
                M = rng.normal(size=(r, r - k)) + 1j * rng.normal(size=(r, r - k))
                Qe, _ = np.linalg.qr(M)
                cols.append(B @ Qe[:, : r - k])
        alpha = m_tot / R
        S = np.hstack(cols) if cols else np.zeros((D, 0))
        rank = np.linalg.matrix_rank(S, tol=1e-9) if S.shape[1] else 0
        w = D - rank
        x = w / D
        a = (alpha + math.sqrt(alpha * e)) / (1 - math.sqrt(e))
        lhs = x - math.sqrt(max(eta * x * (1 - x), 0))
        cnt += 1
        if (
            lhs > a + 1e-9
            or x > eta + 2 * a + 1e-9
            or (eta + 2 * a > eta + 4 * alpha + 4 * math.sqrt(e) + 1e-9 and alpha <= 1)
        ):
            bad += 1
        worst = max(worst, lhs - a)
        if alpha > 0:
            improve.append((4 * alpha + 4 * math.sqrt(e)) / (2 * a))
    print(f"Part1: instances={cnt} violations={bad} max(lhs-a)={worst:.3e}")
    if improve:
        print(
            f"  ratio old/new bound on (alpha,e)-part: min={min(improve):.2f} median={np.median(improve):.2f}"
        )


def part2():
    print(
        "Part2: integrated sqrt(e)-bracket, old 4*sqrt(e)*H  vs  new 2/(1-sqrt e)*2*sqrt(e*u)*(sqrt(u+H)-sqrt(u))"
    )
    print(
        "  e = sg^2/2 (e=2 e0, sqrt(e0)<=sg/2), eta = 5 sg (+3 sqrt(de) ignored), sg in {0.05, 0.01, 0.001}"
    )
    for sg in (0.05, 0.01, 0.001):
        e = sg**2 / 2
        eta = 5 * sg
        for u, H in ((1, 1), (1, 10), (1, 100), (10, 1), (0.1, 10)):
            old = 4 * math.sqrt(e) * H
            new = 2 / (1 - math.sqrt(e)) * 2 * math.sqrt(e * u) * (math.sqrt(u + H) - math.sqrt(u))
            tot_old = eta * H + old
            tot_new = eta * H + new
            print(
                f"  sg={sg:<6} u={u:<4} H={H:<4} sqrt(e)-part old={old:.4g} new={new:.4g} | total (eta+sqrt e part) old={tot_old:.4g} new={tot_new:.4g} ratio={tot_old / tot_new:.3f}"
            )


run()
part2()
