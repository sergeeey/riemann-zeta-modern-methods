#!/usr/bin/env python3
"""Exact first-resonance certificate for Rubinstein III.5 analytic-z elliptic model.

No numerical approximation, no general all-degree B4 claim.
For ell=3 mod 4 the coefficient H[X U^(ell-1) Y^(ell^2)] has two sources.
"""
from fractions import Fraction
from math import comb
from pathlib import Path
import json
from b4_04_verify import m_coefficients, phase, vp_fraction, build_H
from probe_leading import build_lead


def unit_residue(q,p):
    q=Fraction(q)
    if q.denominator%p==0:
        raise ValueError('nonunit denominator')
    return (q.numerator%p)*pow(q.denominator%p,-1,p)%p


def gm(a,b,p):
    return ((a[0]*b[0]-a[1]*b[1])%p,(a[0]*b[1]+a[1]*b[0])%p)


def gpow(x,n,p):
    z=(1,0)
    while n:
        if n&1:z=gm(z,x,p)
        x=gm(x,x,p);n>>=1
    return z


def certificate(p):
    n0=(p+1)//4
    n1=p*(p+1)//4
    M=m_coefficients(max(3,n1))
    A=(p+1)*M[n0]
    B=p*comb(p*p+p,p)*M[n1]
    assert vp_fraction(A,p)==-1 and vp_fraction(B,p)==-1
    pa=unit_residue(p*A,p)
    pb=unit_residue(p*B,p)
    assert pa==pb and pa!=0
    c=next(((a,b) for a in range(-3,4) for b in range(-3,4) if gpow((a%p,b%p),(p*p-1)//4,p)==(p-1,0)),None)
    assert c is not None
    r0,i0=phase(n0,c);r1,i1=phase(n1,c)
    coeff=(A*r0+B*r1,A*i0+B*i1)
    v=min(vp_fraction(coeff[0],p),vp_fraction(coeff[1],p))
    assert v>=0
    # contrast: c=1 violates condition, and coefficient is nonintegral
    assert vp_fraction(A+B,p)==-1
    return {'ell':p,'n0':n0,'n1':n1,'twist_exponent':n1-n0,
      'A':str(A),'B':str(B), 'v_p_A':-1,'v_p_B':-1,
      'residue_pA':pa,'residue_pB':pb,'residue_nonzero':True,
      'c_example':list(c),'c_power_is_minus_one_mod_p':True,
      'v_p_H_resonance_for_example':v,'v_p_H_resonance_for_c_equals_1':-1}


def main():
    records=[certificate(p) for p in (3,7,11,19,23,31)]
    # Full-series vs leading-only check at first resonance for ell=3.
    hfull,_=build_H(12,3,(0,-1))
    hlead,_=build_lead(3,12,(0,-1))
    mon=(1,2,9)
    assert hfull[mon]==[Fraction(0),Fraction(-7)]
    assert hlead[mon]==[Fraction(0),Fraction(5,3)]
    # Exact Honda identity for representative exponents:
    # ell L(T) - L(T^(ell²)) = ell T.
    # Checked algebraically from coefficient formula for all e (index shift).
    proof_honda='index shift in sum_{e>=0} T^(p^(2e))/p^e'
    output={'status':'FINITE PROVED FORMULA + EXACT COMPUTED CONGRUENCES; ALL-DEGREE B4 OPEN',
      'resonance_monomial':'X U^(ell-1) Y^(ell^2)',
      'formula':'H_res=A*c^n0+B*c^n1; A=(ell+1)*m[n0], B=ell*binom(ell^2+ell,ell)*m[n1]',
      'n0':'(ell+1)/4','n1':'ell*(ell+1)/4',
      'condition':'If residues ell*A ≡ ell*B !=0 mod ell then H_res is integral iff c^((ell^2-1)/4)=-1 mod ell',
      'records':records,
      'ell3_full_H_1_2_9':str(hfull[mon][1])+'i',
      'ell3_lead_only_H_1_2_9':str(hlead[mon][1])+'i',
      'ell3_resonance_formula':'-(5*c+26*c^3)/3',
      'honda_identity':proof_honda}
    path=Path(__file__).with_name('results.json');path.write_text(json.dumps(output,indent=2,ensure_ascii=False)+'\n')
    print('6 exact residue certificates PASS, lead-only failure PASS, ell=3 full cancellation PASS')
    for q in records:print(q['ell'],q['residue_pA'],q['residue_pB'],q['v_p_H_resonance_for_example'])

if __name__=='__main__':main()
