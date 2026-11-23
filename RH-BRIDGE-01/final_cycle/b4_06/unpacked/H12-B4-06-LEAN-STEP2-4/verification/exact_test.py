"""Independent, exact checks of the arithmetic in H12 B4-06.

Finite cross-checks, not a substitute for an all-primes proof.
"""
from fractions import Fraction
from math import comb

def primes(limit):
    return [p for p in range(3, limit + 1, 4) if all(p % q for q in range(2, int(p**.5)+1))]

def vp_integer(n, p):
    if n == 0: return 10**9
    z=0
    while n % p == 0:
        n//=p; z+=1
    return z

def vp_rational(x, p):
    return vp_integer(x.numerator,p)-vp_integer(x.denominator,p)

def residue(x,p):
    x=Fraction(x)
    assert x.denominator%p
    return (x.numerator*pow(x.denominator,-1,p))%p

def phi(n):
    return Fraction(comb(2*n,n),4**n*(4*n+1))

def a_coeff(nmax):
    a=[Fraction(1)]
    for n in range(1,nmax+1):
        a.append((6*sum((a[j]*a[n-j] for j in range(1,n)),Fraction(0))-(2 if n==1 else 0))/((4*n+1)*(4*n-6)))
    return a

def run():
    ps=primes(103)
    for p in ps:
        r=(p-3)//4
        q=(p*p-1)//4
        n0=(p+1)//4
        n1=p*n0
        assert q==4*r*r+6*r+2
        assert n1==q+n0 and n0<p and n1<2*q
        for j in range(n1+1):
            v=vp_rational(phi(j),p)
            if j==q: assert v==-1,(p,j,v)
            else: assert v>=0,(p,j,v)
        assert residue(p*phi(q),p)==p-1,p
        assert residue(phi(n0),p)!=0
    print('PASS: valuation uniqueness and p*phi[q]=-1 for',len(ps),'primes p<=103')
    for p in [3,7,11,19,23,31]:
        n0=(p+1)//4;n1=p*n0
        a=a_coeff(n1)
        assert residue(p*a[n1]+a[n0],p)==0,p
        assert residue(a[n0],p)!=0
        print('PASS: p*a[n1]=-a[n0] mod p for',p,'residue',residue(-a[n0],p))
if __name__=='__main__':run()
