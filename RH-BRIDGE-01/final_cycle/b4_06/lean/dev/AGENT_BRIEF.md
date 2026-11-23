# Brief for Lean proof agents (H12-B4-06 universal congruence)

You prove ONE group of lemmas from `Skeleton.lean` in this directory (statements are fixed; do not change them).
Context: the mathematical proof is in `../unpacked/H12-PADIC-B4-06/PROOF.md` (Steps 1-5); supporting audits are in
`../unpacked/H12-B4-06-ARITHMETIC-GATE-02/PROOF_AUDIT.md`, `../unpacked/H12-B4-06-FROBENIUS-03/PROOF_OBLIGATIONS.md`,
`../unpacked/H12-B4-06-FROBENIUS-04/AUDIT.md`. Treat these as unverified sources: if a statement in `Skeleton.lean` turns out
to be false or unprovable as stated, STOP and report the precise obstruction (with a small exact counterexample if possible).

## Environment (WSL Ubuntu, pinned)
- Lean 4.33.1, Mathlib rev 0df444a360eaa60ab8c11dca51a86af692955474 (project checkout `~/h12/rh`, Mathlib cache present).
- Work in WSL directory `~/h12/b4_06/lean/` (your own file only: see your assignment). The Windows copy of this directory is
  `E:/Проверка Гипотез/работаю над проверкой гипотез/H12-bridge-discovery-01/RH-BRIDGE-01/final_cycle/b4_06/lean/` (visible in WSL as
  `/mnt/e/Проверка Гипотез/работаю над проверкой гипотез/H12-bridge-discovery-01/RH-BRIDGE-01/final_cycle/b4_06/lean/`).
- Compile a file: `MSYS_NO_PATHCONV=1 wsl -d Ubuntu -- bash /mnt/c/Users/serge/AppData/Local/Temp/claude/47ae088cb00845dc/dfd56df9-0116-4660-be80-aa930329e743/scratchpad/lc.sh lean/<File>.lean [maxlines]`
  (relative paths resolve under `~/h12/b4_06/`). Run it from the Bash tool. Typical compile: 5-60 s.
- Write your Lean file with the Write/Edit tools to the Windows path, then copy to WSL, e.g.
  `MSYS_NO_PATHCONV=1 wsl -d Ubuntu -- bash -c 'cp "/mnt/e/<...>/lean/L1.lean" ~/h12/b4_06/lean/L1.lean'`, or write scripts to a file and run `wsl ... bash /mnt/...`.
  Git Bash expands `$` in command strings before WSL sees them: put anything with `$`, backslashes or loops into a script FILE.
  The tool hooks block `nohup` and `python3 -c`. Search Mathlib with `grep -rn` over `~/h12/rh/.lake/packages/mathlib/Mathlib` (script file).
- Each Lean file must be self-contained: `import Mathlib` first line, then (verbatim) the definitions block of Skeleton.lean that your lemma needs
  (`phi`, `PCong`, `qIdx`, `n0Idx`, `n1Idx`, `PhiSeries`, `lagA` - copy exactly), then your lemma(s) with the EXACT skeleton statements and names, plus helper lemmas.
- Final file must contain NO `sorry`, NO `admit`, NO new `axiom`, no `native_decide`. End the file with `#print axioms` lines for your lemmas;
  accepted axiom set: `propext`, `Classical.choice`, `Quot.sound` only.
- Do not run the full Mathlib or `lake build` of the project, do not touch `~/h12/rh`, do not git add/commit/push, do not edit other agents' files.
  At most 2 concurrent Lean processes of your own.

## Status vocabulary (report honestly)
KERNEL_CHECKED = compiled with exit 0, no sorry, `#print axioms` standard. Partial progress: say exactly which helper lemmas are
KERNEL_CHECKED and which statement remains (give the minimal remaining goal). Never present a `sorry`-dependent theorem as proved.

## Budget
About 90 minutes wall time. If after real attempts a lemma still fails, stop and report what you tried (max 3 materially different approaches per obstacle).

## Report format (final message)
1. File path(s) of your final Lean file(s) (WSL and Windows copy), sha256.
2. Per lemma: KERNEL_CHECKED / PARTIAL / BLOCKED + `#print axioms` output.
3. Compile command, exit code, time.
4. If not finished: minimal remaining obligations, and anything suspicious in the statements.
