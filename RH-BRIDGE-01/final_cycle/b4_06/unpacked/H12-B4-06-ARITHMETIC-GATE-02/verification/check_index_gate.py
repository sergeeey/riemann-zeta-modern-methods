#!/usr/bin/env python3
"""Exact bounded audit of the indexing and p-adic valuation gate.
No floating arithmetic. Not a proof for all primes.
"""
from math import comb
from fractions import Fraction

def primes_upto(N):
    out=[]
    for p in range(3,N+1,4):
        if all(p%d for d in range(2,__import__('math').isqrt(p)+1)):
            out.append(p)
    return out

def vp_fact(n,p):
    z=0
    while n:
        n//=p
        z+=n
    return z

def vp(n,p):
    k=0
    while n%p==0:
        k+=1;n//=p
    return k

def unit_residue(x,p):
    x=Fraction(x)
    if x.denominator%p==0:
        raise ValueError('not p-integral')
    return x.numerator%p * pow(x.denominator%p,-1,p)%p

def check(p):
    r=(p-3)//4
    n0=(p+1)//4
    q=(p*p-1)//4
    n1=p*n0
    s=3*r+2
    assert q==r*p+s and n1==q+n0 and 2*q>n1
    assert s<p<=2*s
    nonintegral=[]
    denom_hits=[]
    for j in range(n1+1):
        denom=4*j+1
        if denom%p==0:
            d=denom//p
            assert d%4==3
            assert d<=p+1
            assert d<p or j==q
            if d<p:
                assert j%p==s
                assert 2*(j%p)>=p
            denom_hits.append((j,d))
        v=vp_fact(2*j,p)-2*vp_fact(j,p)-vp(denom,p)
        if v<0: nonintegral.append((j,v))
    assert nonintegral==[(q,-1)],(p,nonintegral)
    u=unit_residue(p*Fraction(comb(2*q,q),4**q*(4*q+1)),p)
    assert u==p-1
    return {'p':p,'n1':n1,'q':q,'denominator_hits':len(denom_hits),'unique_exceptional':True,'p_phi_q_mod_p':u}

if __name__=='__main__':
    ps=primes_upto(199)
    data=[check(p) for p in ps]
    print('PASS: %d primes through p=%d, all denominator hits, base-p carry, valuations and exceptional residues' %(len(ps),ps[-1]))
    print('Largest checked resonance n1:',data[-1]['n1'])
