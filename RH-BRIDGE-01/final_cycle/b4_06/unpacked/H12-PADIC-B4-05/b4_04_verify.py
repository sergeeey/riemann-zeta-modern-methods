#!/usr/bin/env python3
"""Exact Frobenius/Dwork gate for Rubinstein's *analytic-z* projected model.

ell=3, c=-i, d=2.  Compute H=Delta_1(beta) composed with letterLog
and test 3H - phi(H)(X^3,U^3,Y^3) divisible coefficientwise by 3.

NOT an all-degree proof. Avoids expanding exp(H) and uses Fraction arithmetic.
"""
from fractions import Fraction as F
from math import comb
import json, argparse
from collections import defaultdict
from pathlib import Path


def m_coefficients(nmax):
    """m(u)=log(sigma(z)/t(z)), u=c*z^4, wp=z^-2 f(u)."""
    a=[F(0)]*(nmax+1);a[0]=F(1)
    for n in range(1,nmax+1):
        den=(4*n-2)*(4*n-3)-12
        a[n]=(6*sum((a[j]*a[n-j] for j in range(1,n)),F(0))-(2 if n==1 else 0))/den
    # t/z=f/(f-2u f') ; log(t/z)=log f - log(f-2u f')
    f=a[:];g=[a[n]*(1-2*n) for n in range(nmax+1)]
    def log_series(h):
        # h(0)=1; log(h)'=h'/h ; recurrence for log coefficients
        l=[F(0)]*(nmax+1)
        for n in range(1,nmax+1):
            l[n]=h[n]-sum(F(k,n)*l[k]*h[n-k] for k in range(1,n))
        return l
    lf,lg=log_series(f),log_series(g)
    m=[F(0)]*(nmax+1)
    for n in range(1,nmax+1):
        m[n]=-a[n]/(4*n*(4*n-1))-lf[n]+lg[n]
    assert m[1]==-F(5,12) and m[2]==-F(3,56) and m[3]==-F(13,990)
    return m


def phase(n, c):
    # Exact Gaussian integer c^n, returned as two integer components.
    a,b=1,0
    for _ in range(n):a,b=a*c[0]-b*c[1],a*c[1]+b*c[0]
    return a,b


def build_H(limit,ell=3,c=(0,-1)):
    # 3-variable H(X,U,Y)=Delta_1(beta)(L(X),L(U),L(Y))
    # beta=project(m(z+w)-m(z)-m(w))
    m=m_coefficients(limit//4)
    out=defaultdict(lambda:[F(0),F(0)])
    corrections={}
    for a in range(limit+1):
        # L(T)= sum_{e>=0} T^(ell^(2e))/ell^e. Choose counts k1,k2.
        # e>=3 has first degree ell^6; refuse if the degree limit needs it.
        opt=[]
        if ell**6<=limit:raise ValueError('Extend letterLog expansion to e>=3')
        for k1 in range(0,a+1):
            for k2 in range(0,a-k1+1):
                exp=a+(ell**2-1)*k1+(ell**4-1)*k2
                if exp>limit:continue
                multin=comb(a,k1)*comb(a-k1,k2)
                opt.append((exp,F(multin,ell**(k1+2*k2))))
        corrections[a]=opt
    for n in range(1,limit//4+1):
        N=4*n
        for a in range(1,N):
            b=N-a
            if (a-ell*b)%(ell**2-1):continue
            coeff=m[n]*comb(N,a)
            if coeff==0:continue
            r,ii=phase(n,c)
            for j in range(1,a):
                # X^j U^(a-j) Y^b
                cc=coeff*comb(a,j)
                for d1,t1 in corrections[j]:
                    for d2,t2 in corrections[a-j]:
                        if d1+d2+b>limit:continue
                        for d3,t3 in corrections[b]:
                            if d1+d2+d3>limit:continue
                            q=cc*t1*t2*t3
                            z=out[(d1,d2,d3)]
                            z[0]+=r*q; z[1]+=ii*q
    return dict(out),m


def vp_fraction(q,p=3):
    if not q:return 99999
    def val(n):
        n=abs(int(n));v=0
        while n%p==0:v+=1;n//=p
        return v
    return val(q.numerator)-val(q.denominator)


def test_dwork(H,ell=3):
    bad=[]; counts=defaultdict(lambda:[0,0])
    for mon in sorted(set(H) | {tuple(ell*k for k in t) for t in H if ell*sum(t)<=max(map(sum,H))}, key=lambda z:(sum(z),z)):
        c=H.get(mon,[F(0),F(0)])
        # 3H - conjugate(H(X^3)), with conjugation i->-i
        pre=H.get(tuple(k//ell for k in mon),[0,0]) if all(k%ell==0 for k in mon) else [0,0]
        test=(ell*c[0]-pre[0],ell*c[1]+pre[1])
        v=min(vp_fraction(test[0],ell),vp_fraction(test[1],ell))
        d=sum(mon)
        counts[d][0]+=1
        if v<1:
            counts[d][1]+=1
            bad.append({'monomial':list(mon),'value_re':str(test[0]),'value_im':str(test[1]),'vp':v})
    return bad,counts


def fmt(a):return str(a[0])+' + ('+str(a[1])+')i'

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--degree',type=int,default=32);ap.add_argument('--ell',type=int,choices=[3,7,11],default=3);args=ap.parse_args()
    d=args.degree
    ell=args.ell
    c={3:(0,-1),7:(-1,-1),11:(0,-1)}[ell]
    H,m=build_H(d,ell,c)
    # [X^10 U Y] H_z at degree12 = 8i/5 (exp has same for this monomial)
    # β analytic-z H includes coefficient -26 c^3/15 - 10c/3 = 8i/5
    if ell==3 and d>=12:assert H[(10,1,1)]==[0,F(8,5)],H[(10,1,1)]
    bad,counts=test_dwork(H,ell)
    res={'source':'Rubinstein III.5 z,w-model + Lean letterLog d=2','degree':d,'ell':ell,'c':str(c),
         'number_nonzero_H_monomials':len(H),'m_coeffs_u_n':{str(i):str(v) for i,v in enumerate(m) if v},
         'dwork_bad_count':len(bad),'bad_examples':bad[:30],
         'degree_counts':{str(i):{'nonzero_H':v[0],'failed_dwork':v[1]} for i,v in sorted(counts.items())},
         'reference_X10_U_Y':fmt(H.get((10,1,1),[0,0]))}
    root=Path(__file__).parent;out=root/('results-ell'+str(ell)+'-degree'+str(d)+'.json');out.write_text(json.dumps(res,indent=2,ensure_ascii=False)+'\n')
    print('ell:',ell,'degree:',d,'nonzero_H:',len(H),'Dwork failed:',len(bad))
    for i,v in sorted(counts.items()): print('degree',i,'monomials',v[0],'fail',v[1])
    for x in bad[:10]:print('BAD',x)
    print('Saved',out)

if __name__=='__main__':main()
