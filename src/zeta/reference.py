"""External reference values for the first nontrivial zeros of ζ(s).

Source: A. M. Odlyzko, "Tables of zeros of the Riemann zeta function",
https://www-users.cse.umn.edu/~odlyzko/zeta_tables/  — widely published,
also matching Wikipedia "Riemann hypothesis" and LMFDB.

Status: [MEMORY] — transcribed from well-known published tables. These are used
as an EXTERNAL positive control: the toolkit's independent root-finder and
mpmath.zetazero() must both reproduce them. Any transcription error here will
surface as a mismatch in the triple cross-check (that is the point).

Each entry is the imaginary part Im(ρ_n); the real part is 1/2 (the claim).
"""

# First 10 zeros — imaginary parts (Im ρ_n), n = 1..10.
ODLYZKO_FIRST_10: list[str] = [
    "14.134725141734693790",
    "21.022039638771554993",
    "25.010857580145688763",
    "30.424876125859513210",
    "32.935061587739189691",
    "37.586178158825671257",
    "40.918719012147495187",
    "43.327073280914999519",
    "48.005150881167159727",
    "49.773832477672302182",
]
