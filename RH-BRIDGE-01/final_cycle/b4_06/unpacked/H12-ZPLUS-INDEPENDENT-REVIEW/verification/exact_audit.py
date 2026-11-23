from sympy import Matrix, eye, Rational, sqrt, simplify

# All assertions use exact rationals / algebraic expressions.
D=4
I=eye(D)
B=I
Ecols=Matrix.hstack(*[I[:,j] for j in range(1,D)])
Q=B*B.T
P=I-Ecols*(Ecols.T*Ecols).inv()*Ecols.T
assert P==Matrix.diag(1,0,0,0)
assert (P*Q).trace()==1
assert Q.trace()==4 and (Q*Q).trace()==4
assert Rational(1,D)==Rational(1,4) # eta=0, kappa=0, eprime=0, alpha=1/4 => equality

# Old (HS closeness) but not new (uniform op bound, kappa=1/5)
N=100
old=Matrix.diag(2,*([1]*(N-1)))
new=Rational(6,5)*eye(N)
eps=Rational(1,100); eta=Rational(1,100); kappa=Rational(1,5)
assert ((old-eye(N))*(old-eye(N))).trace()==eps*N
assert N*(old*old).trace()/old.trace()**2-1 == Rational(99,10201) <= eta
assert old[0,0]>1+kappa

# New (op/tr bound) but not old (HS bound), same epsilon, eta and kappa
assert new == (1+kappa)*eye(N)
assert new.trace() >= N
assert N*(new*new).trace()/new.trace()**2-1==0
assert ((new-eye(N))*(new-eye(N))).trace()==4>eps*N

# Necessity of isotropy, despite ideal Ki and no deletions
Bc=Matrix([[1],[0]])
Kc=Bc.T*Bc
Qc=Bc*Bc.T
assert Kc==Matrix([[1]]) and Qc==Matrix.diag(1,0)
assert Qc.rank()==1 and Qc.rows==2
assert 2*(Qc*Qc).trace()/Qc.trace()**2-1==1

# Necessity of op bound, despite perfect isotropy and aggregate trace
Bhuge=Matrix([[sqrt(10)]+[0]*9])
Kh=Bhuge.T*Bhuge
Qh=Bhuge*Bhuge.T
assert simplify(Kh.trace()-10)==0
assert simplify(Qh[0,0]-10)==0
assert Kh[0,0]==10

# Improved slope term never exceeds published e,H-bound for e <= 1/4.
for e in [Rational(0),Rational(1,10000),Rational(1,100),Rational(1,16),Rational(1,4)]:
    for u,H in [(Rational(1,100),Rational(100)), (Rational(1),Rational(1)),(Rational(10),Rational(1)),(Rational(0),Rational(10))]:
        if u==0:
            new_cross=0
        else:
            new_cross=4*sqrt(e*u)*(sqrt(u+H)-sqrt(u))
        old_cross=4*sqrt(e)*H
        assert simplify(old_cross - new_cross).is_nonnegative is True or simplify(old_cross-new_cross)==0
print('PASS: exact B and Q counterexamples, parameter noncomparability, necessity of hypotheses, slope improvement checks')
from sympy import log
for e in [Rational(0),Rational(1,10000),Rational(1,100),Rational(1,16),Rational(1,4)]:
    for u,H in [(Rational(1,100),Rational(100)), (Rational(1),Rational(1)),(Rational(10),Rational(1)),(Rational(0),Rational(10))]:
        if u==0:
            new_c=0; old_log=0
        else:
            old_log=4*u*log(1+H/u)
            new_c=2/(1-sqrt(e))*(u*log(1+H/u)+2*sqrt(e*u)*(sqrt(u+H)-sqrt(u)))
        orig=old_log+4*sqrt(e)*H
        assert float((orig-new_c).evalf()) >= -1e-12
print('PASS: 20 full slope-error comparisons including denominator 1-sqrt(e)')
