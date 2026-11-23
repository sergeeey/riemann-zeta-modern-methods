# S2 novelty log (2026-11-23)

Claim: for p = 3 mod 4, n0=(p+1)/4, n1=p*n0, a_n = (4n-1)16^n H_n/(4n)!: p*a_{n1} ≡ -a_{n0} (mod p).
Frozen criterion (a)/(b)/(c) as in the task. fulltext_checked refers to the specific candidate.

## R1  WebSearch: "Hurwitz numbers congruence prime p = 3 mod 4 Eisenstein series Gaussian integers Kummer congruences"
- Goto, "Congruence Relations Connecting Tate-Shafarevich Groups with Bernoulli-Hurwitz Numbers by Elliptic Gauss Sums in Eisenstein Case", arXiv 2204.04425 (2022): congruences for Eisenstein-integer case, primes l = 1 mod 3 (degree one); cites Onishi [O] for Gaussian case (primes of norm = 1 mod 4). Hurwitz class number congruence h(-p) = -2B_{(p+1)/2} (mod p). -> related. fulltext_checked: yes (pdftotext, intro + Thm 2.5).
- Kalinin, Zottor, arXiv 2602.00206: finite Gaussian power sums mod p^6, p = 3 mod 4, B_{p-3}. -> related (finite sums, not lattice sums/Hurwitz numbers). fulltext_checked: yes (grep: no Hurwitz/lemniscate/(p+1)/4).
- overlap: none.

## R2  WebSearch: "Laurent coefficients Weierstrass p-function lemniscatic supersingular prime congruence formal group height 2 Honda"
- Guerzhoy, "On the p-adic values of the weight two Eisenstein series for supersingular primes", arXiv 2403.02592 (2024): E2 / Ramanujan P-series values, Honda-type Theorem 2, formal group log integrality. No congruence with indices (p+1)/4, p(p+1)/4. -> related. fulltext_checked: yes (partial: intro, Theorems A, 1, 2, 3).
- Katz-type Kummer for Hurwitz ("Ramanujan differential operator, a certain CM elliptic curve and Kummer congruences", Compositio, Cambridge PDF) appears in results; not opened. fulltext_checked: no.
- overlap: none at this round.

## R3  arXiv MCP: "Hurwitz numbers" AND (congruence OR supersingular OR formal group)
- Onishi, arXiv math/0406096 (Generalized Bernoulli-Hurwitz numbers ... universal Bernoulli numbers), math/0304377; Goto 2204.04425; Bannai-Kobayashi 0804.4338. -> see R6, R9.

## R4  Crossref (cr.py): "Bernoulli-Hurwitz numbers congruences", "Eisenstein-Kronecker numbers p-adic congruences", "lemniscate sine Taylor coefficients congruences" (other queries hit HTTP 429)
- Katz, "The congruences of Clausen-von Staudt and Kummer for Bernoulli-Hurwitz numbers", Math. Ann. 216 (1975) 1-4, doi 10.1007/bf02547966 (paywalled; zbMATH Zbl 0303.10028 review: mod p congruences for Hurwitz numbers = Laurent coefficients of wp via q-expansion principle + Clausen-von Staudt; Lang 1969 got sharper results). -> related (ordinary/general p, not the supersingular shift). fulltext_checked: no (paywall); zbMATH review read.
- Onishi, Russian Math. Surveys 66 (2011) 871-932, doi 10.1070/rm2011v066n05abeh004763. related. fulltext: arXiv version read, see R6.
- Carlitz, "The coefficients of the lemniscate function", Math. Comp. 16 (1962) 475, doi 10.2307/2003138. not opened. fulltext_checked: no. -> [UNVERIFIED relevance]
- Bannai-Kobayashi 2010 Duke, doi 10.1215/00127094-2010-024; Bannai-Furusho-Kobayashi Nagoya 2015; not opened (background). fulltext_checked: no.

## R5  WebFetch Springer for Katz 1975 / WebSearch on it
- Springer page redirects to idp/cookie wall; PDF endpoint returned HTML. eudml 403. -> fulltext not obtained.
- zbMATH API (api.zbmath.org) works: Katz review quoted above.

## R6  Onishi arXiv math/0406096 (read via pdftotext, sections 7.1, 7.2, intro)
- Theorem 7.2.1: Kummer-type congruence for y^2 = x^{2g+1} - x for primes p = 1 mod 4g, (p-1)|4gn, indices C_{4gn + r(p-1)}. Cites Hurwitz 1897/1899, Lang 1969 ("Kummersche Kongruenzen fuer die normierten Entwicklungskoeffizienten der Weierstrasschen wp-Funktion", Abh. Math. Sem. Hamburg 33 (1969) 183-196, doi 10.1007/bf02992933), Carlitz 1949/1952, Katz 1975, Gunji 1976, Honda 1970. Only primes p = 1 mod 4 (split). Section 13 uses Honda's theorem for formal groups. -> related (split primes only; not the inert/supersingular shift). fulltext_checked: yes.

## R7  WebSearch + Crossref: Lang 1969
- Lang 1969 located (Crossref doi 10.1007/bf02992933); zbMATH Zbl 0183.31304 content hidden (license). Not opened. -> related (unknown content for p inert). fulltext_checked: no.

## R8  WebSearch: lemniscate sine/cosine Taylor coefficients congruences, p = 3 mod 4, supersingular
- Krattenthaler-Mueller, "The congruence properties of Romik's sequence of Taylor coefficients of Jacobi's theta function theta_3", arXiv 2304.11471: Taylor coefficients of theta_3 at q=e^{-pi} (CM point i), vanishing/periodicity mod p depends on p mod 4. fulltext_checked: yes (grep: no (p+1)/4, no Hurwitz, no lemniscatic). -> related (different object).
- Onishi-Sairaiji, "Arithmetic over the Gaussian Number Field on a Certain Family of Elliptic Curves with CM", arXiv 2108.09013 (2021): Kummer-type congruences (Thm 7.1) for lemniscate cos/sin coefficients, Gaussian primes of degree one (norm = 1 mod 4). fulltext_checked: yes (partial; layout garbled). -> related.

## R9  WebSearch: Eisenstein series G_{p+1}, Gaussian lattice sum, Hurwitz series mod p
- Ahlgren-Hanson-Raum-Richter, "Eisenstein series modulo p^2", arXiv 2502.16917 (2025): SL2(Z) forms, congruence G2 = G_{2+p(p-1)} + p*G_{p+1}^p (mod p^2) (their (1.4)); no Z[i] lattice, no Hurwitz numbers. fulltext_checked: yes (grep). -> related (structural echo only).
- Hu-Kim-Sha, arXiv 1805.09225 (Eisenstein series with polynomial indexes): SL2(Z); not opened beyond abstract. fulltext_checked: no.

## R10  WebSearch: formal group logarithm coefficients, supersingular, height 2, recursion, index (p+1)/4
- Nothing with indices (p+1)/4, p(p+1)/4. Larson-conjecture paper arXiv 2509.16175 (supersingular congruences for Delta^t, chromatic): fetched: no Hurwitz/CM/y^2=x^3-x content. -> none/related. fulltext_checked: partial (HTML summary).

## R11  zbMATH Open API: "Hurwitz numbers Weierstrass congruences supersingular"; "Katz Divisibilities congruences Cartier duality"
- ** Chellali, M., "Congruences entre nombres de Bernoulli-Hurwitz dans le cas supersingulier", J. Number Theory 35 (1990) 157-179, doi 10.1016/0022-314X(90)90110-D, Zbl 0705.11008. Review (Goss): K imaginary quadratic, p odd prime inert in K, E with CM by O_K good reduction at p; Bernoulli-Hurwitz numbers defined from wp; refines Katz's Kubota-Leopoldt-type congruences. fulltext_checked: no (ScienceDirect 403/paywall).
- ** Katz, "Divisibilities, congruences, and Cartier duality", J. Fac. Sci. Univ. Tokyo Sect. IA 28 (1981; cited by Bannai-Kobayashi as 1982), 667-678, Zbl 0559.14032: p inert, formal group Lubin-Tate [p](X)=pX+alpha X^{p^2}; congruences mod powers of p for BH(n). fulltext_checked: no (not found open).
- ** Bannai-Kobayashi, "Integral structures on p-adic Fourier theory", arXiv 0804.4338 (v3), section 5 (Theorems 5.1, 5.2, 5.8) restating Katz [Ka2, Thm 3.11] and Chellali [Ch, Thm 1.1]. fulltext_checked: yes (page 21-26, image of p.21 read). Statement (their notation): E CM by O_K, p odd inert in K, good supersingular reduction; wp = z^-2 + sum_{n>=2} BH(n+2)/(n+2) z^n/n!; epsilon root of unity with -epsilon*p = Frobenius (x,y)->(x^{p^2},y^{p^2}); gamma^{p^2-1} = -epsilon^{-1} (p^2)!/(p^{p+1}(p^2-1)); L(n) = (1-b^{n+2})(1-p^n)/(gamma^n p^{[np/(p^2-1)]}) * BH(n+2)/(n+2). Thm 5.1 (Katz): L(n) integral, L(n+p^l(p^2-1)) = L(n) mod p^l. Thm 5.2 (Chellali): if n != 0 mod p^2-1 then L(n+p^l(p^2-1)) = L(n) mod p^{l+1}.
  -> OVERLAP (criterion (b), see check below).

## Own check of reduction to Chellali Thm 5.2, l = 0 (my computation, not from a source)
Weights k = n+2: k0 = p+1 -> n = p-1 (not 0 mod p^2-1); k1 = p(p+1) = k0 + (p^2-1) -> n+(p^2-1) = p^2+p-2. So the claim is the case l=0 of the congruence. Bookkeeping: coefficient of z^{k-2} in wp is BH(k)/(k (k-2)!); floor(np/(p^2-1)) = 0 for n=p-1 and = p for n=p^2+p-2; (k0-2)! = (p-1)! = -1 mod p; (k1-2)! = p^{p+1} * (p-2)! * unit = p^{p+1} (mod p^{p+2}) up to Wilson-type digits (p-2)! = 1; b^{k1}=b^{k0} and gamma^{p^2-1} = 1 mod p for y^2=x^3-x (epsilon = 1 since Frobenius over F_{p^2} is -p; (p^2)!/p^{p+1} = 1 mod p; (p^2-1) = -1), so Chellali gives p*C_{k1} = -C_{k0} mod p for the Laurent coefficients C_k of wp. Numerical check (exact rationals, g2=4, g3=0): p = 3, 7, 11, 19: v_p(C_{k0}) = 0, v_p(p*C_{k1}) = 0, unit(C_{k0}) + unit(p*C_{k1}) = 0 mod p in all four cases; ((k1-2)! C_{k1}/p^p)/((k0-2)! C_{k0}) = 1 mod p in all four cases. [VERIFIED-inline, 4 primes, not a proof]
Not covered by the restated theorems: that a_{n0} is a p-adic UNIT (L(n) is only asserted integral); the unit property was checked numerically for p = 3, 7, 11, 19 only. The scaling a_n vs C_k (16^n, lattice normalisation) changes values by lambda^{p^2-1} = 1 mod p for a p-unit lambda.

## R12  WebSearch (Chellali title) + numdam
- Barsky, "Congruences de coefficients de series de Taylor (Application aux nombres de Bernoulli-Hurwitz)", Groupe d'etude d'analyse ultrametrique, 3e annee 1975/76, no. 17: ordinary case (Hasse invariant nonzero mod p); recovers Katz and Lang. fulltext_checked: yes (abstract/intro). -> related (ordinary, not supersingular).

## Summary
rounds: 12. overlapping_found: 1 chain (Katz 1981/82 Thm 3.11 + Chellali 1990 Thm 1.1, read only via Bannai-Kobayashi Thm 5.1/5.2). decision_S2: not_novel (criterion (b)), with the limit that primary texts of Katz and Chellali were not accessible.
