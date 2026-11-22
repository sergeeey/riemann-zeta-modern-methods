"""NUMERICAL TEST (not a proof) of two finite-dimensional lemmas on near-isometric maps and span codimension.

Setting: H = C^D, maps B_i : C^{r_i} -> H, weights gamma_i > 0, K_i = gamma_i B_i^* B_i, Q = sum_i gamma_i B_i B_i^*, R = sum r_i,
t = Tr Q, E_i <= C^{r_i} subspaces with sum_i codim E_i <= eps R.  Target: w = codim_H( sum_i B_i E_i ).

Lemma Z (Zhang, preliminary note, Lemma 4.2, p. 41-42): if sum_i ||K_i - I||_HS^2 <= e R (e <= 1/4) and Tr(Q^2) <= (1+eta) Tr(Q)^2 / D, then
      w <= D (eta + 4 eps + 4 sqrt(e))   (eps <= 1).
Lemma Z+ (this mission; proof in candidate_lemma.md): if K_i <= (1+kappa) I for every i (operator order), sum_i Tr K_i >= (1 - e') R with e' < 1, and Tr(Q^2) <= (1+eta) t^2/D, then
      w <= D (eta + 2 (1+kappa) eps / (1 - e')).

The test builds random instances, computes the smallest admissible (e, eta, kappa, e', eps) from the data and checks both inequalities; it also builds the sharpness
family for the eta-term.  Run: python -I lemma_test.py
"""

import sys

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
rng = np.random.default_rng(20261122)


def random_instance(D, n_maps, mode):
    Bs, gam = [], []
    for _ in range(n_maps):
        r = int(rng.integers(max(2, D // 4), D + 1))
        G = rng.normal(size=(D, r)) + 1j * rng.normal(size=(D, r))
        Uq, _ = np.linalg.qr(G)  # D x r with orthonormal columns
        if mode == "near_iso":
            s = 1 + 0.08 * rng.normal(size=r)
        elif mode == "contract":  # K_i <= I but far from I in HS norm
            s = rng.uniform(0.3, 1.0, size=r)
        else:  # mixed with a few large singular values
            s = np.where(
                rng.random(r) < 0.1, rng.uniform(1.0, 1.6, size=r), rng.uniform(0.8, 1.0, size=r)
            )
        Vr, _ = np.linalg.qr(rng.normal(size=(r, r)) + 1j * rng.normal(size=(r, r)))
        Bs.append(Uq @ np.diag(s) @ Vr)
        gam.append(1.0)
    return Bs, gam


def analyse(D, Bs, gam, eps_target):
    R = sum(B.shape[1] for B in Bs)
    Ks = [g * B.conj().T @ B for B, g in zip(Bs, gam, strict=True)]
    Q = sum(g * B @ B.conj().T for B, g in zip(Bs, gam, strict=True))
    t = float(np.trace(Q).real)
    eHS = sum(np.linalg.norm(K - np.eye(K.shape[0]), "fro") ** 2 for K in Ks) / R
    eta = float(np.trace(Q @ Q).real) * D / t**2 - 1
    kappa = max(float(np.linalg.eigvalsh(K).max()) for K in Ks) - 1
    eprime = 1 - sum(float(np.trace(K).real) for K in Ks) / R
    # subspaces E_i with total codimension about eps_target * R
    cod = [int(round(eps_target * B.shape[1])) for B in Bs]
    cols = []
    for B, c in zip(Bs, cod, strict=True):
        r = B.shape[1]
        Vq, _ = np.linalg.qr(rng.normal(size=(r, r)) + 1j * rng.normal(size=(r, r)))
        keep = Vq[:, : max(r - c, 0)]
        if keep.shape[1]:
            cols.append(B @ keep)
    M = np.concatenate(cols, axis=1) if cols else np.zeros((D, 0))
    rank = int(np.linalg.matrix_rank(M, tol=1e-9)) if M.size else 0
    w = D - rank
    eps = sum(cod) / R
    return {"w": w, "eps": eps, "eHS": eHS, "eta": eta, "kappa": kappa, "eprime": eprime}


viol_Z = viol_Zp = n_Z = n_Zp = 0
worst_Z = worst_Zp = 0.0
for mode in ("near_iso", "contract", "mixed"):
    for D in (8, 16, 30):
        for n_maps in (3, 6, 12, 40):
            for eps_t in (0.0, 0.05, 0.15, 0.4):
                Bs, gam = random_instance(D, n_maps, mode)
                a = analyse(D, Bs, gam, eps_t)
                # Lemma Z (only when its hypotheses hold)
                if a["eHS"] <= 0.25 and a["eps"] <= 1 and a["eta"] >= 0:
                    n_Z += 1
                    bound = D * (a["eta"] + 4 * a["eps"] + 4 * np.sqrt(a["eHS"]))
                    worst_Z = max(worst_Z, a["w"] / bound if bound > 0 else 0)
                    viol_Z += a["w"] > bound + 1e-9
                # Lemma Z+
                if a["eprime"] < 1 and a["eta"] >= 0:
                    n_Zp += 1
                    bound = D * (
                        a["eta"]
                        + 2 * (1 + max(a["kappa"], 0)) * a["eps"] / (1 - max(a["eprime"], 0))
                    )
                    worst_Zp = max(worst_Zp, a["w"] / bound if bound > 0 else 0)
                    viol_Zp += a["w"] > bound + 1e-9
print(
    f"Lemma Z : instances with hypotheses satisfied {n_Z}, violations {viol_Z}, largest w/bound {worst_Z:.3f}"
)
print(
    f"Lemma Z+: instances with hypotheses satisfied {n_Zp}, violations {viol_Zp}, largest w/bound {worst_Zp:.3f}"
)

# Sharpness in eta (eps = 0, e = 0): Q = c * P_S with S of dimension (1-nu) D  =>  w = nu D, eta = nu/(1-nu)
print("\nSharpness of the eta term (eps = 0): w = nu D versus the bound D*eta = D*nu/(1-nu)")
for D, nu in ((20, 0.1), (40, 0.05), (100, 0.01)):
    dimS = D - int(round(nu * D))
    S = np.linalg.qr(rng.normal(size=(D, dimS)) + 1j * rng.normal(size=(D, dimS)))[0]
    B = S  # one map with orthonormal columns spanning S: K = I, Q = P_S
    Q = B @ B.conj().T
    eta = float(np.trace(Q @ Q).real) * D / float(np.trace(Q).real) ** 2 - 1
    w = D - np.linalg.matrix_rank(B, tol=1e-9)
    print(
        f"  D={D}, nu={nu}: w={w}, eta={eta:.5f}, bound D*eta={D * eta:.3f}, ratio w/(D eta)={w / (D * eta):.4f}"
    )
