#!/bin/bash
# Build the single merged Lean file from the four verified lemma files + Final.lean
D="/mnt/e/Проверка Гипотез/работаю над проверкой гипотез/H12-bridge-discovery-01/RH-BRIDGE-01/final_cycle/b4_06/lean"
OUT="$D/B4_06_Universal.lean"
{
  echo "import Mathlib"
  echo
  echo "/-!"
  echo "# H12-B4-06: universal first-resonance congruence for \`lagA\`: p * lagA n1 = -(lagA n0) (mod p), p = 3 (mod 4)"
  echo "SCOPE (read together): here \`a_n\` means exactly \`lagA n\`, the Lagrange-inversion formula (1) of"
  echo "H12-PADIC-B4-06-PROOF.md. NOT formalized in this file: (i) the identification of \`lagA n\` with the"
  echo "Laurent coefficients of the Weierstrass wp function (checked numerically only, n <= 60), (ii) Step 5"
  echo "(the transfer wp -> h_n -> beta), (iii) the B4-05 two-source identity and the criterion c^((p^2-1)/4) = -1,"
  echo "(iv) the identification with the author's beta. The theorem name refers to the first Dwork resonance index"
  echo "n1 = p(p+1)/4 only; it is NOT the headline theorem of PROOF.md."
  echo "Build: concatenation of separately compiled modules (L1, L2/L5, L3a/L3d, L3b/L3c) + Final.lean;"
  echo "the file as a whole is compiled and checked by itself (provenance of the modules is not needed for the check)."
  echo "-/"
  echo
  echo "open PowerSeries"
  echo
  echo "namespace H12.B4"
  echo
  echo "noncomputable section"
  echo
  sed -n '17,36p' "$D/L1.lean"
  echo "/-! ===== L3a / L3d (power series perturbation, truncation invariance) ===== -/"
  sed -n '8,95p' "$D/L3a.lean"
  echo "/-! ===== L3b / L3c (nilpotent Frobenius mod p, reduction via Z_p) ===== -/"
  sed -n '8,130p' "$D/L3b.lean"
  echo "/-! ===== L1 (p-integrality of phi_j, j <= n1, j /= q) ===== -/"
  sed -n '37,139p' "$D/L1.lean"
  echo "/-! ===== L2 / L5 (p*phi_q = -1 mod p, phi_{n0} unit) ===== -/"
  sed -n '20,256p' "$D/L2.lean"
  cat "$D/Final.lean"
  echo
  echo "end"
  echo
  echo "end H12.B4"
  echo
  echo "#print axioms H12.B4.B4_06_first_resonance"
} > "$OUT"
wc -l "$OUT"
cp "$OUT" "$HOME/h12/b4_06/lean/B4_06_Universal.lean"
