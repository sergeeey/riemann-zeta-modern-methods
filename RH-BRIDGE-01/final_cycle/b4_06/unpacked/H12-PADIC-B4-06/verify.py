#!/usr/bin/env python3
"""Independent exact certificates supporting the all-primes proof in PROOF.md.
Checks do NOT replace the symbolic proof. No floating point is used.
"""
from fractions import Fraction as F
from math import comb, factorial
import json
from pathlib import Path


def v_p(n,p):
    if not n:return 10**8
    k=0
    while n%p==0:k+=1;n//=p
    return k

def residue(x,p):
    x=F(x)
    if x.denominator%p==0:raise ValueError('non p-integral')
    return (x.numerator%p)*pow(x.denominator%p,-1,p)%p

def phi(n):return F(comb(2*n,n),4**n*(4*n+1))

def first_lagrange_wp(nmax):
    # wp(z) z^2 = sum a_n (c z^4)^n; inverse of z=v*Phi(cv^4).
    pp=[phi(i) for i in range(nmax+1)]
    # for each n use (Phi)^{-(4n-2)}, truncating at degree n
    ans=[F(1)]
    for n in range(1,nmax+1):
        exponent=-(4*n-2)
        z=[F(0)]*(n+1);z[0]=1
        power=[F(0)]*(n+1);power[0]=1
        # binomial generalized n choose k
        coef=1
        for k in range(1,n+1):
            coef=F(coef*(exponent-k+1),k)
            # power of (Phi-1) by polynomial mult
            nxt=[F(0)]*(n+1)
            for i in range(1,n+1):
                for j in range(n+1-i):nxt[i+j]+=power[j]*pp[i]
            power=nxt
            z=[z[j]+coef*power[j] for j in range(n+1)]
        ans.append(-z[n]/(2*n-1))
    return ans

def wp_recurrence(nmax):
    a=[F(0)]*(nmax+1);a[0]=1
    for n in range(1,nmax+1):
        a[n]=(6*sum((a[j]*a[n-j] for j in range(1,n)),F(0))-(2 if n==1 else 0))/((4*n+1)*(4*n-6))
    return a

def check_prime(p):
    assert p%4==3 and p>=3
    q=(p*p-1)//4;n0=(p+1)//4;n1=p*n0
    b=comb(2*q,q)
    assert v_p(b,p)==1
    assert v_p(4*q+1,p)==2
    assert residue(p*phi(q),p)==p-1
    assert residue(phi(n0),p)!=0
    # No other non-integral Phi coefficient before resonance.
    def vp_factorial(N):
        total=0
        while N:
            N//=p;total+=N
        return total
    for j in range(n1+1):
        expected=-1 if j==q else 0
        val=vp_factorial(2*j)-2*vp_factorial(j)-v_p(4*j+1,p)
        assert val>=expected,(p,j,val,expected)
        if j==q:assert val==-1
    return {"p":p,"q":q,"n0":n0,"n1":n1,"p_phi_q_mod_p":p-1,"phi_n0_mod_p":residue(phi(n0),p),"unique_nonintegral_phi_upto_n1":True}

def main():
    def prime(n):
        return n>1 and all(n%d for d in range(2,int(n**0.5)+1))
    ps=[p for p in range(3,160) if p%4==3 and prime(p)]
    allres=[check_prime(p) for p in ps]
    # Independent exact reconstruction of wp(z) using inversion vs ODE.
    al=first_lagrange_wp(8);ar=wp_recurrence(8)
    assert al==ar,(al,ar)
    # Test the key exact arithmetical intermediate (p*a_n1 + a_n0 divisible by p).
    from b4_04_verify import m_coefficients
    verified=[]
    for p in [3,7,11,19,23,31]:
        n0=(p+1)//4;n1=p*n0
        a=wp_recurrence(n1)
        assert residue(p*a[n1]+a[n0],p)==0
        r=residue(-a[n0],p)
        assert r!=0
        h=m_coefficients(max(3,n1))
        A=(p+1)*h[n0];B=p*comb(p*p+p,p)*h[n1]
        assert residue(p*A,p)==residue(p*B,p)==r
        verified.append({'p':p,'n0':n0,'n1':n1,'residue':r})
    payload={'status':'ALL-PRIMES PROOF IN PROOF.md; COMPUTATIONS ARE CROSS-CHECKS',
             'n_primes_phi_checked':len(ps),'primes_phi_checked':ps,
             'phi_valuation_records':allres,'lagrange_vs_ode_through_n':8,
             'normalized_resonance_checked':verified,'no_float':True}
    output=Path(__file__).with_name('results.json');output.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
    print('PASS: %d primes p=3 mod 4; first 8 inversion vs ODE; %d full residue tests'%(len(ps),len(verified)))

if __name__=='__main__':main()
