from fractions import Fraction
from math import comb
from b4_04_verify import build_H,phase,m_coefficients,test_dwork
from probe_leading import build_lead
from resonance import certificate

for p,c in [(3,(0,-1)),(7,(-1,-1)),(11,(0,-1))]:
 n0=(p+1)//4;n1=p*(p+1)//4;degree=p*p+p
 H,m=build_H(degree,p,c)
 A=(p+1)*m[n0]
 B=p*comb(degree,p)*m[n1]
 r,im=phase(n0,c);s,j=phase(n1,c)
 expected=[A*r+B*s,A*im+B*j]
 assert H[(1,p-1,p*p)]==expected
 Hlead,_=build_lead(p,degree,c)
 failures,_=test_dwork(Hlead,p)
 assert failures and sum(failures[0]['monomial'])==degree,(p,failures[:1])
 assert not test_dwork(H,p)[0],f'full Dwork failed ell {p}'
 print(f'PASS ell={p}: exact two-source resonance; lead-only fails at degree={degree}; full model passes to degree={degree}')
for p in (3,7,11,19,23,31):
 assert certificate(p)['residue_pA']==certificate(p)['residue_pB']
print('PASS 6 primes: normalized residue congruence and twist dependence')
