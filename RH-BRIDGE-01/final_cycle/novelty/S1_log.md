# S1 novelty screening log

Claim: for p = 3 mod 4, n0=(p+1)/4, n1=p*n0, wp = z^-2 + sum a_n z^(4n-2) (y^2=x^3-x): p*a_{n1}, a_{n0} p-integral, a_{n0} a p-unit, p*a_{n1} = -a_{n0} (mod p).
Numeric sanity check of the claim (own script, exact fractions, Hurwitz recursion): p=3,7,11 all hold (v(a_n0)=0, v(p a_n1)=0, v(p a_n1 + a_n0)=1,1,2). [VERIFIED-inline, synthetic of own recursion]

Tool notes: Crossref and Semantic Scholar API hit HTTP 429 after the first call; arXiv MCP rate-limited on 2 of 4 calls; zbMATH worked; OpenAlex/Firecrawl not used.

## Rounds

R1. Query: "Weierstrass p-function lemniscatic case coefficients congruences modulo p supersingular primes p = 3 mod 4" (WebSearch standard)
- OEIS A002770 (Carlitz 1962, Math. Comp. 16, 475-478, "The coefficients of the lemniscate function"): overlap none (p = 1 mod 4 formula); related. fulltext_checked: no
- Guerzhoy, arXiv 2403.02592 "On the p-adic values of the weight two Eisenstein series for supersingular primes" (2024): none. fulltext_checked: yes (arXiv HTML; Thms 1-3 about A^(p)(Lambda), no coefficient-index relation; curve y^2=x^3-x not treated)
- Blakestad-Grant arXiv 1903.02480 (ordinary, p>3): none. fulltext_checked: no (abstract)

R2. Query: "Laurent coefficients of Weierstrass elliptic function y^2=x^3-x p-adic divisibility Hurwitz numbers congruence" (WebSearch)
- Luecke-Peterson, arXiv 2506.07420 (2025) "p-adic congruences in iterated derivatives of the Weierstrass elliptic function": related (Kummer congruences of derivatives of wp via E_infty orientations, Tate-curve/ordinary setting; no supersingular/CM, no n vs pn relation). fulltext_checked: partial (HTML first 100k of 212k chars)
- Bunkova arXiv 1701.00848 (sigma coefficients 2-adic hypothesis): none. fulltext_checked: no

R3. Query: Crossref x3 (Laurent coefficients congruences supersingular; Hurwitz numbers lemniscate; Eisenstein/sigma p-adic lemniscatic) -> only first returned (Landweber 1988, Legendre polynomials; none), others 429.

R4. Query: "Hurwitz numbers congruence p = 3 mod 4 Gaussian integers G_{4n} lemniscate Kummer"; arXiv search "Hurwitz numbers Gaussian integers inert primes"
- Goto, arXiv 2204.04425 (2022): related; Onishi-type congruences with elliptic Gauss sums; split primes (p = 1 mod 4 / 1 mod 3), not inert. fulltext_checked: yes (arXiv PDF intro read)
- Onishi, "Congruence relations connecting Tate-Shafarevich groups with Hurwitz numbers", Interdiscip. Inf. Sci. 16(1) 71-86 (2010) (zbMATH 1253.11065): related, split Gaussian primes (norm prime = 5 mod 8). fulltext_checked: no (description via Goto's intro)
- Zhao arXiv 2510.17939 "On the Bernoulli-Hurwitz periods" (2025): related, p split. fulltext_checked: no (abstract)
- Onishi math/0406096, math/0304377: related (von Staudt/Kummer for generalized BH numbers). fulltext_checked: no

R5. Query: "Carlitz coefficients of the lemniscate function Laurent expansion ... congruences prime p" (WebSearch). Only OEIS A002770 / Carlitz 1962 (not opened). Carlitz 1941, 1949 (Duke) known only via Guerzhoy/Snyder references. fulltext_checked: no.

R6. Query: arXiv "Weierstrass elliptic function lemniscatic Laurent p-adic congruence supersingular formal group height 2": Blakestad-Grant, Luecke-Peterson, Debaisieux 2606.25726 (integrality of height-one formal groups): none/related. fulltext_checked: no.

R7. Hurwitz 1899, Math. Ann. 51, 196-226 "Ueber die Entwicklungscoefficienten der lemniscatischen Functionen" (scan from Zenodo, pp. 196-218 of 31 pages read as images).
- Defines E_n by sum (r+is)^-4n = (2w)^4n/(4n)! E_n; wp (g2=4,g3=0) = 1/u^2 + sum 2^4n E_n u^(4n-2)/(4n (4n-2)!), i.e. exactly the claim's normalization a_n = 2^4n E_n/(4n(4n-2)!) (eq. (7)).
- For q = 3 mod 4 prime: eq. (30) 2^4n (q^4n -1) E_n/(4n) integral; (47')-(48'), (57), (67)-(73): congruences mod q at derivative order q-1 (coefficient at index ~ (q+1)/4 area) in terms of e_{(q-3)/4}. No relation between indices n0 and p*n0. overlap: none; related. fulltext_checked: yes, partial (pp. 196-218; pp. 219-226 and tables not read)

R8. Snyder, "Kummer congruences for the coefficients of Hurwitz series", Acta Arith. 40 (1982) 175-191. Scan read (first 4 pages). Kummer congruence Ke(p): c_{m+r(p-1)} etc. for solutions of (f')^2 = 1+f^4 (lemniscatic type), shift p-1 in Taylor index of f, not wp-Laurent index n -> pn. related. fulltext_checked: partial (pp. 175-181)

R9. zbMATH: "ti:Hurwitz numbers congruence" -> Onishi 2010, Goto. No match for lemniscatic coefficients mod p, p=3 mod 4. WebSearch extended for BH numbers supersingular -> led to Bannai-Kobayashi.

R10. KEY. Bannai-Kobayashi, "Integral structures on p-adic Fourier theory", arXiv 0804.4338 (v3 2015), Ann. Inst. Fourier 60 (2010) [journal data via Numdam link in search; not fetched], Section 5 "Relations to Katz's and Chellali's results" (TeX source read).
Setting verbatim from source: E CM by O_K, model y^2=4x^3-g2 x-g3, p odd, inert in K, good (supersingular) reduction. wp = 1/z^2 + sum_{n>=2} BH(n+2)/(n+2) z^n/n!. epsilon: root of unity with Frobenius (x,y)->(x^{p^2},y^{p^2}) equal to mult by -epsilon*p. gamma in W(F_p-bar): gamma^{p^2-1} = -epsilon^{-1} p^2!/(p^{p+1}(p^2-1)). L(n) = (1-b^{n+2})(1-p^n) / (gamma^n p^{[np/(p^2-1)]}) * BH(n+2)/(n+2).
- Theorem 5.1 (Katz [Ka2, Thm 3.11], J. Fac. Sci. Univ. Tokyo 28 (1982) 667-678): L(n) integral; L(n+p^l(p^2-1)) = L(n) mod p^l.
- Theorem 5.2 (Chellali, J. Number Theory 35 (1990) 157-179, DOI 10.1016/0022-314X(90)90110-D, Thm 1.1): if n != 0 mod p^2-1: L(n+p^l(p^2-1)) = L(n) mod p^(l+1).
Index arithmetic: z-exponent n = 4m-2. m=n0: n=p-1. m=n1=p*n0: n=p^2+p-2 = (p-1)+(p^2-1). So l=0, n=p-1 (not 0 mod p^2-1): L(n1-index) = L(n0-index) mod p.
Derivation [INFERRED, my own algebra, not in any source]: BH(n+2)/(n+2) = n! a_m. n0!=(p-1)! = -1 (Wilson). (p^2+p-2)! = p^2! * (p^2+1)...(p^2+p-2) = p^2! * (p-2)! mod units, v_p = p+1; floor(np/(p^2-1)) = p for n1, 0 for n0. gamma^{-(p^2-1)} * (p^2!/p^{p+1}) = eps*(p^2-1)*(-1)... = eps mod p. b^{p^2-1}=1 mod p. For y^2=x^3-x, p=3 mod 4: a_p=0, Frobenius over F_{p^2} is -p, so epsilon=1. Result: p*a_{n1} = -eps^{-1} a_{n0} = -a_{n0} (mod p), same sign as the claim. Integrality of a_{n0}, p*a_{n1}: from Katz integrality of L(n). NOT obtained from the restatement: that a_{n0} is a p-ADIC UNIT (a congruence does not give it).
Original Katz 1982 and Chellali 1990 full texts NOT obtained (paywalled / 403); only the Bannai-Kobayashi restatement was read. fulltext_checked: yes for BK; no for Katz and Chellali.
Overlap assessment: overlap (criterion (b), conditional on the original theorems matching BK's restatement and on the unit property).

R11. Queries for Katz 1982 and Chellali full text (WebSearch x2): MaRDI record Q917577 (Chellali; zbMATH 0705.11008, reviewer D. Goss: p inert in K, E good reduction, refines Katz's Kubota-Leopoldt-type congruences). No open full text found. Katz 1975 Math. Ann. 216, 1-4 (DOI 10.1007/BF02547966): abstract-level only; eudml 403, Springer paywalled.

Other related: Guerzhoy, Compositio Math. 141 (2005) 583-590 (full text read, 8 pp.): Ramanujan differential operator, curve y^2=x^3-delta (j=0), Taylor expansion of wp at a point a, for p=2 mod 3 (supersingular) b_f(n+r(p-1)) = 0 mod p^r. Different curve, different statement (zero-congruence, step p-1). related.
Seminar note seen only as a title: "Congruences de coefficients de series de Taylor (Application aux nombres de Bernoulli-Hurwitz)", Groupe d'etude d'analyse ultrametrique 1975-76 (numdam GAU_1975-1976__3_1_A11_0): related, not opened.
