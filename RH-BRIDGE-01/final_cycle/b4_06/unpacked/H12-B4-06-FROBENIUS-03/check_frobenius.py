#!/usr/bin/env python3
"""Exact independent finite-field verification of B4-06 Frobenius substep.
Not a proof for all primes or a Lean kernel check.
"""
from math import comb
import json

def primes_upto(N):
    return [n for n in range(3,N+1) if n%4==3 and all(n%d for d in range(2,int(n**.5)+1))]

def mul(a,b,p,n):
    z=[0]*n
    for i,x in enumerate(a[:n]):
        if x:
            for j,y in enumerate(b[:n-i]):
                z[i+j]=(z[i+j]+x*y)%p
    return z

def power(a,k,p,n):
    assert k>=0 and a[0]%p==1
    z=[1]+[0]*(n-1)
    while k:
        if k&1: z=mul(z,a,p,n)
        a=mul(a,a,p,n);k//=2
    return z

def inverse(a,p,n):
    assert a[0]%p==1
    ans=[1]+[0]*(n-1)
    for k in range(1,n):
        ans[k]=(-sum(a[j]*ans[k-j] for j in range(1,k+1)))%p
    assert mul(ans,a,p,n)==[1]+[0]*(n-1)
    return ans

def exponent(a,k,p,n):
    if k<0: return power(inverse(a,p,n),-k,p,n)
    return power(a,k,p,n)

def residue_phi(j,p):
    # only for p-integral phi_j (j < p, with j=n0), no p cancellation needed
    return comb(2*j,j)*pow(4**j*(4*j+1),-1,p)%p

def test_one(p):
    n0=(p+1)//4
    n=n0+1
    # F coefficients below degree p from Phi; all denominator units at j<=n0.
    F=[1]+[residue_phi(j,p) for j in range(1,n)]
    M=p*(p+1)-2
    lhs=exponent(F,-M-1,p,n)
    assert lhs==F, (p,'Frobenius failure',lhs,F)
    # first low coefficient: a_n0 = -(2n0-1)^-1 [u^n0]F^-(p-1)
    low=exponent(F,-(p-1),p,n)
    a0=(-low[n0]*pow(2*n0-1,-1,p))%p
    assert a0==2*F[n0]%p
    # exceptional high coefficient, after removing the only nonintegral phi_q:
    # p a_n1 = 2 (p phi_q) [u^n0]F^(-M-1)
    high=(-2*lhs[n0])%p  # universal residue p phi_q=-1
    assert (high+a0)%p==0
    return {'p':p,'n0':n0,'phi_n0':F[n0],'a_n0':a0,'p_a_n1':high,
            'low_coefficient':low[n0],'high_coefficient':lhs[n0]}

def main():
    ps=primes_upto(199)
    out=[test_one(p) for p in ps]
    assert len(ps)==24,ps
    with open(__file__.replace('check_frobenius.py','results.json'),'w',encoding='utf-8') as f:
        json.dump({'scope':'Finite field truncation only; no Lean/kernel certification',
                   'checks':out,'count':len(out)},f,indent=2)
    print('PASS: Frobenius exponent identity and normalized coefficient congruence for',len(ps),'primes through',ps[-1])
    print('Cases:',[(v['p'],v['a_n0'],v['p_a_n1']) for v in out[:8]])
if __name__=='__main__':main()
