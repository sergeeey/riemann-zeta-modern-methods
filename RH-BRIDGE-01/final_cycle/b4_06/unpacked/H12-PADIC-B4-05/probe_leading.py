from fractions import Fraction as F
from math import comb
from collections import defaultdict
import sys, json, argparse
sys.path.insert(0,str(__import__('pathlib').Path(__file__).resolve().parent))
from b4_04_verify import m_coefficients, phase, vp_fraction, test_dwork

def build_lead(ell,degree,c):
 n=(ell+1)//4
 m=m_coefficients(max(n,3))
 a0=m[n]*comb(4*n,ell)
 # leading 2 terms beta=A*(x^ell*y+x*y^ell)
 assert 4*n==ell+1
 out=defaultdict(lambda:[F(),F()])
 r,ii=phase(n,c)
 def Lpower(k):
  arr=[]
  # X -> X + X^(ell^2)/ell + X^(ell^4)/ell²
  for k1 in range(k+1):
   for k2 in range(k-k1+1):
    exp=k+(ell**2-1)*k1+(ell**4-1)*k2
    if exp<=degree:arr.append((exp,F(comb(k,k1)*comb(k-k1,k2),ell**(k1+2*k2))))
  return arr
 for j in range(1,ell):
  q=a0*comb(ell,j)
  for e1,t1 in Lpower(j):
   for e2,t2 in Lpower(ell-j):
    for e3,t3 in Lpower(1):
     if e1+e2+e3>degree: continue
     z=out[(e1,e2,e3)]; z[0]+=r*q*t1*t2*t3;z[1]+=ii*q*t1*t2*t3
 return dict(out),a0
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--ell',type=int,choices=[3,7,11],default=3);ap.add_argument('--degree',type=int,default=100);args=ap.parse_args()
 c={3:(0,-1),7:(-1,-1),11:(0,-1)}[args.ell]
 H,a=build_lead(args.ell,args.degree,c)
 bad,counts=test_dwork(H,args.ell)
 out={'ell':args.ell,'degree':args.degree,'leading_beta_A':str(a),'complex_c':str(c),'terms_H':len(H),'failed_Dwork':len(bad),'first_bad':bad[:10]}
 print(json.dumps(out,ensure_ascii=False,indent=2))
