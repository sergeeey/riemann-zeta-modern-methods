#!/usr/bin/env python3
"""Independent finite-ring checks; NOT a proof or Lean kernel certification."""
import json, random
from pathlib import Path

PRIMES=[3,7,11,19,23,31,43,47,59,67,71,79,83,103,107,127,131,139,151,163,167,179,191,199]
def mul(a,b,p):
    n=p
    c=[0]*n
    for i,x in enumerate(a):
        if x:
            for j in range(n-i):
                c[i+j]=(c[i+j]+x*b[j])%p
    return c

def powpoly(a,n,p):
    r=[1]+[0]*(p-1)
    while n:
        if n&1: r=mul(r,a,p)
        a=mul(a,a,p)
        n//=2
    return r

rng=random.Random(120618)
tested=0
for p in PRIMES:
    for j in range(5):
        a=[1]+[rng.randrange(p) for _ in range(p-1)]   # F = 1 + u A
        neg=[(-a[k])%p for k in range(p)]
        neg[0]=0
        # Inverse G = 1 - (F-1) + (F-1)^2 - ... truncated
        x=[0]+a[1:]
        g=[1]+[0]*(p-1)
        term=[1]+[0]*(p-1)
        for t in range(1,p):
            term=mul(term,neg,p)
            g=[(v+w)%p for v,w in zip(g,term)]
        one=[1]+[0]*(p-1)
        assert mul(a,g,p)==one
        assert powpoly(a,p,p)==one
        assert powpoly(a,p*(p+1),p)==one
        assert mul(a,powpoly(g,p*(p+1),p),p)==a
        tested+=1
print(json.dumps({"status":"PASS","prime_count":len(PRIMES),
                  "random_examples_per_prime":5,
                  "total_finite_ring_checks":tested,
                  "seed":120618,"not_a_universal_proof":True}))
