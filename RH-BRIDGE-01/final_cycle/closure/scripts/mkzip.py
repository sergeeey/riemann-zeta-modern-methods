import os, sys, zipfile, hashlib

# usage: mkzip.py <path to RH-BRIDGE-01>; archive root = parent (worktree root)
R = sys.argv[1]
W = os.path.dirname(R.rstrip("/"))
os.chdir(W)
out = os.path.join("RH-BRIDGE-01", "H12-FINAL-CYCLE-01-2026-11-23.zip")
skip_names = {"H12-FINAL-CYCLE-01-2026-11-23.zip", "closure_archive_verification.log"}
if os.path.exists(out):
    os.remove(out)
n = 0
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    for d in ["RH-BRIDGE-01", "RH-NEXT-01", "RH-NEXT-02", "RH-NEXT-03"]:
        for root, _, files in os.walk(d):
            if "__pycache__" in root:
                continue
            for f in sorted(files):
                if f in skip_names:
                    continue
                z.write(os.path.join(root, f).replace("\\", "/"))
                n += 1
with zipfile.ZipFile(out) as z:
    bad = z.testzip()
print("entries:", n, "testzip:", bad)
print("size:", os.path.getsize(out), "sha256:", hashlib.sha256(open(out, "rb").read()).hexdigest())
