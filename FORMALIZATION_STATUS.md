# Formalization status

**The paper’s core Gaussian counterexamples and failure of GMC(n) for every n ≥ 3
are formalized in Lean.** Supporting omissions are recorded below; full-paper
coverage is not claimed.
The canonical manuscript and independent finite verifier are unchanged. The ledger
includes every named result, proof-critical display, and substantive supporting
claim; historical narrative and provenance are not mathematical obligations.

“Proved” requires compiled matching declarations and transitive axiom validation.
Partial rows list completed ingredients and exact outstanding obligations. Cited
external results are not axioms. Formal exponential displays are coefficientwise
identities, never unproved assertions of analytic exponential integrability.

### gmc-definition

- Status: proved
- Class: core
- Origin: Paper calculation, original construction, or formal proof dependency.
- Location: §1, definition of GMC
- Obligation: For every complex multivariate P with all positive moments zero, every Q has zero mixed moments eventually
- Lean: GaussianMomentsCounterexamples.GMC
- Dependencies: gaussian-space, integrability
- Remaining: None (definition; counterexample proof tracked separately).

### real-coefficients

- Status: proved
- Class: supporting
- Origin: Paper calculation, original construction, or formal proof dependency.
- Location: §1, real coefficients
- Obligation: Second-moment zero forces the real polynomial to vanish
- Lean: GaussianMomentsCounterexamples.real_polynomial_eq_zero_of_second_moment, GaussianMomentsCounterexamples.real_polynomial_eq_zero_of_complex_second_moment, GaussianMomentsCounterexamples.real_polynomial_eq_zero_of_all_moments
- Dependencies: integrability
- Remaining: None. Full support, integrability, almost-everywhere vanishing, and polynomial extensionality are proved.

### global-logic

- Status: blocked
- Class: supporting
- Origin: Cited background or cited reduction machinery.
- Location: eq:global-logic
- Obligation: Global DVEZ implication and its contrapositive with n≥2
- Lean: none
- Dependencies: gmc-one
- Remaining: Need the cited all-dimensional DVEZ theorem and GMC(1), not just a conditional logical contrapositive. The requisite special-image/inverse-map chain is absent; see FORMALIZATION_AUDIT.md.

### fixed-logic

- Status: blocked
- Class: supporting
- Origin: Cited background or cited reduction machinery.
- Location: eq:fixed-logic
- Obligation: GMC(2r) implies SIC(r), hence invertibility of each cubic homogeneous Keller map
- Lean: none
- Dependencies: none
- Remaining: Missing general differential-evaluation image/kernel theorem, uniform Zariski closed-set threshold argument, and Abhyankar–Gurjar inverse-coefficient formula used by DVEZ/Zhao. No cited axiom is introduced.

### announced-map

- Status: proved
- Class: supporting
- Origin: Paper calculation, original construction, or formal proof dependency.
- Location: §2, announced F
- Obligation: Displayed F has determinant 1 and identifies the two displayed distinct points
- Lean: GaussianMomentsCounterexamples.announcedMap_jacobian_det, GaussianMomentsCounterexamples.collisionPoints_distinct, GaussianMomentsCounterexamples.announcedMap_collision₁, GaussianMomentsCounterexamples.announcedMap_collision₂, GaussianMomentsCounterexamples.announcedMap_not_injective, GaussianMomentsCounterexamples.announcedMap_no_leftInverse
- Dependencies: none
- Remaining: None. Polynomial Jacobian determinant and exact collision are kernel checked.

### normalized-map

- Status: proved
- Class: supporting
- Origin: Paper calculation, original construction, or formal proof dependency.
- Location: §2, normalized G
- Obligation: Target linear automorphism gives displayed G with identity linear part
- Lean: GaussianMomentsCounterexamples.targetNormalization, GaussianMomentsCounterexamples.normalizedAnnouncedMap_eq_target, GaussianMomentsCounterexamples.normalizedAnnouncedMap_eval, GaussianMomentsCounterexamples.normalizedAnnouncedMap_linear_coeff, GaussianMomentsCounterexamples.normalizedAnnouncedMap_constant
- Dependencies: announced-map
- Remaining: None. Target normalization is a genuine linear equivalence; linear coefficient matrix is the identity.

### normalized-support

- Status: proved
- Class: supporting
- Origin: Paper calculation, original construction, or formal proof dependency.
- Location: §2, support of G
- Obligation: Degree ≥4 counts are 3,2,2,1 in degrees 4,5,6,7
- Lean: GaussianMomentsCounterexamples.normalizedAnnouncedMap_support_0, GaussianMomentsCounterexamples.normalizedAnnouncedMap_support_1, GaussianMomentsCounterexamples.normalizedAnnouncedMap_support_2, GaussianMomentsCounterexamples.normalizedAnnouncedDegreeCounts
- Dependencies: normalized-map
- Remaining: None. Exact supports imply degree-filtered monomial counts 3,2,2,1.

### degree-lowering

- Status: blocked
- Class: supporting
- Origin: Cited background or cited reduction machinery.
- Location: prop:route-bound, elementary step
- Obligation: Degree-lowering preserves Keller property and noninvertibility; adds two variables with the listed degrees
- Lean: none
- Dependencies: none
- Remaining: Need explicit two-variable stabilization with inverse elementary automorphisms, preservation of determinant/noninvertibility, and a terminating degree/support invariant. Existing polynomial algebra alone does not prove this construction.

### route-arithmetic

- Status: partial
- Class: supporting
- Origin: Paper calculation, original construction, or formal proof dependency.
- Location: prop:route-bound, recurrence
- Obligation: The balanced recurrence has values 1,2,3,5 and weighted cost 18; interpreting these as actual step bounds gives s=39, r=79, and Gaussian dimension 158.
- Lean: GaussianMomentsCounterexamples.balancedCost, GaussianMomentsCounterexamples.balancedCost_values, GaussianMomentsCounterexamples.balancedCost_weighted, GaussianMomentsCounterexamples.balanced_recurrence_bounds, GaussianMomentsCounterexamples.route_step_bound, GaussianMomentsCounterexamples.route_dimension_counts
- Dependencies: normalized-support, degree-lowering
- Remaining: Balanced recurrence arithmetic and displayed numerals are proved unconditionally for the defined cost function. Remaining: prove that the function bounds actual degree-lowering steps; the recurrence implications alone do not establish BCW transformations.

### nilpotence

- Status: blocked
- Class: supporting
- Origin: Cited background or cited reduction machinery.
- Location: prop:route-bound, U and E_t
- Obligation: U is stably equivalent to K; elementary compositions imply nilpotent JN
- Lean: none
- Dependencies: degree-lowering
- Remaining: Need stable equivalence for U and E_t and the polynomial-matrix implication det(I+tJN)=1 → nilpotence, tied to the actual construction. These are not established by the numerical bounds.

### homogenization

- Status: blocked
- Class: supporting
- Origin: Cited background or cited reduction machinery.
- Location: prop:route-bound, homogenization
- Obligation: Cubic homogenization preserves required properties in r=2s+1=79
- Lean: none
- Dependencies: nilpotence
- Remaining: Need a multivariate cubic homogenization construction, nilpotence/Keller preservation and noninvertibility transfer, including the extra dimension. Univariate library homogenization is insufficient.

### route-bound

- Status: partial
- Class: supporting
- Origin: Paper calculation, original construction, or formal proof dependency.
- Location: prop:route-bound, conclusion
- Obligation: The specified Jacobian reduction route implies ¬GMC(158)
- Lean: GaussianMomentsCounterexamples.not_GMC_158, GaussianMomentsCounterexamples.announcedMap_not_injective, GaussianMomentsCounterexamples.route_dimension_counts
- Dependencies: degree-lowering, route-arithmetic, nilpotence, homogenization, fixed-logic
- Remaining: The conclusion ¬GMC(158) is proved by direct coordinate extension only. The separate announced-map → cubic-homogeneous reduction → DVEZ/Zhao route remains unformalized.

### complex-coordinates

- Status: proved
- Class: core
- Origin: Paper calculation, original construction, or formal proof dependency.
- Location: §3, Gaussian coordinates
- Obligation: Z=(X+iY)/√2, W=(X−iY)/√2 are conjugate and give invertible complex linear coordinates
- Lean: GaussianMomentsCounterexamples.eval_normalizedZ, GaussianMomentsCounterexamples.eval_normalizedW, GaussianMomentsCounterexamples.eval_normalizedW_conj, GaussianMomentsCounterexamples.coordinateEquiv3, GaussianMomentsCounterexamples.coordinateEquiv4
- Dependencies: none
- Remaining: None. Invertible complex algebra substitutions and real-input conjugacy are proved.

### contraction

- Status: proved
- Class: core
- Origin: Paper calculation, original construction, or formal proof dependency.
- Location: eq:contraction
- Obligation: For every a,b≥0, integral W^a Z^b equals δ_ab a!
- Lean: GaussianMomentsCounterexamples.expectation_pair, GaussianMomentsCounterexamples.expectation_pair_mul
- Dependencies: real-gaussian, stein, complex-coordinates
- Remaining: None. Alternate proof uses polynomial Stein identities, derived from real Gaussian integration by parts, instead of rotational invariance.

### coefficient-contraction

- Status: proved
- Class: core
- Origin: Paper calculation, original construction, or formal proof dependency.
- Location: eq:coefficient-contraction
- Obligation: For every complex polynomial R and a≥0, integral W^a R(Z)=a! coeff_a R
- Lean: GaussianMomentsCounterexamples.expectation_coefficient_contraction
- Dependencies: contraction
- Remaining: None. Arbitrary complex polynomial and any distinct coordinate pair.

### real-gaussian

- Status: proved
- Class: core
- Origin: Paper calculation, original construction, or formal proof dependency.
- Location: eq:real-gaussian
- Obligation: For every k≥0, integral T^(2k)=(2k−1)!!=(2k)!/(2^k k!)
- Lean: GaussianMomentsCounterexamples.real_gaussian_even_moment, GaussianMomentsCounterexamples.real_gaussian_even_moment_doubleFactorial, GaussianMomentsCounterexamples.gaussian_doubleFactorial_eq_factorial, GaussianMomentsCounterexamples.complex_gaussian_even_moment
- Dependencies: real-moment-recurrence
- Remaining: None. At k=0, natural 0!!=1 represents the conventional (-1)!!=1.

### central-binomial

- Status: proved
- Class: supporting
- Origin: Paper calculation, original construction, or formal proof dependency.
- Location: eq:central-binomial
- Obligation: Formal binomial series with coefficients (−1)^k choose(2k,k)/4^k is (1+u)^(−1/2)
- Lean: GaussianMomentsCounterexamples.choose_neg_half, GaussianMomentsCounterexamples.binomial_neg_half_subst_mul
- Dependencies: none
- Remaining: None. Coefficients match the formal binomial series; the substituted inverse square root is selected by constant coefficient 1.

### p4

- Status: proved
- Class: core
- Origin: Paper calculation, original construction, or formal proof dependency.
- Location: eq:P4
- Obligation: Genuine complex polynomial P₄=(1+Z₂)(W₁(1−Z₁)+W₂), Q₄=Z₂; six terms, degree 3
- Lean: GaussianMomentsCounterexamples.P4_formula, GaussianMomentsCounterexamples.P4_expansion, GaussianMomentsCounterexamples.naturalP4_support, GaussianMomentsCounterexamples.naturalP4_support_card, GaussianMomentsCounterexamples.P4_totalDegree, GaussianMomentsCounterexamples.P4_ne_zero, GaussianMomentsCounterexamples.Q4_ne_zero
- Dependencies: complex-coordinates
- Remaining: None. Six terms belong to natural coordinates; degree 3 is also proved after invertible real-coordinate substitution.

### master-four

- Status: proved
- Class: core
- Origin: Paper calculation, original construction, or formal proof dependency.
- Location: eq:master-four / prop:four
- Obligation: For arbitrary A∈ℂ[z] and m≥1, integral A(Z₂)P₄^m=m! coeff_m(A(1+z)^(m−1))
- Lean: GaussianMomentsCounterexamples.master_four, GaussianMomentsCounterexamples.naturalMoment4_power_expansion, GaussianMomentsCounterexamples.expectation_normalizedSub4
- Dependencies: p4, integrability, coefficient-contraction, four-coefficient-proof, algebraic-integral-bridge
- Remaining: None. Full arbitrary-A, all-positive-m identity under actual Gaussian integration.

### moments-four

- Status: proved
- Class: core
- Origin: Paper calculation, original construction, or formal proof dependency.
- Location: prop:four, consequences
- Obligation: All positive pure moments zero; all positive Q₄-mixed moments m!≠0
- Lean: GaussianMomentsCounterexamples.P4_moment, GaussianMomentsCounterexamples.Q4_P4_moment, GaussianMomentsCounterexamples.Q4_P4_moment_ne_zero
- Dependencies: master-four
- Remaining: None. Mixed moment is nonzero for every positive exponent.

### egf-four

- Status: proved
- Class: supporting
- Origin: Paper calculation, original construction, or formal proof dependency.
- Location: eq:egf-four
- Obligation: Formal expectation EGFs are 1 and t/(1−t)
- Lean: GaussianMomentsCounterexamples.P4_momentEGF, GaussianMomentsCounterexamples.Q4_P4_mixedMomentEGF
- Dependencies: moments-four, explicit-h
- Remaining: None. Formal series; mixed constant term proved separately. No analytic exponential integrals.

### p3

- Status: proved
- Class: core
- Origin: Paper calculation, original construction, or formal proof dependency.
- Location: eq:P3
- Obligation: Genuine complex polynomial P₃=(1+Z)(W−(2+Z)T²/2), Q₃=Z; five terms, degree 4
- Lean: GaussianMomentsCounterexamples.P3_formula, GaussianMomentsCounterexamples.P3_expansion, GaussianMomentsCounterexamples.naturalP3_support, GaussianMomentsCounterexamples.naturalP3_support_card, GaussianMomentsCounterexamples.P3_totalDegree, GaussianMomentsCounterexamples.P3_ne_zero, GaussianMomentsCounterexamples.Q3_ne_zero
- Dependencies: complex-coordinates
- Remaining: None. Five terms belong to natural coordinates; degree 4 is also proved after invertible real-coordinate substitution.

### master-three

- Status: proved
- Class: core
- Origin: Paper calculation, original construction, or formal proof dependency.
- Location: eq:master-three / thm:three
- Obligation: For arbitrary A∈ℂ[z] and m≥1, integral A(Z)P₃^m=m! coeff_m(A(1+z)^(m−1))
- Lean: GaussianMomentsCounterexamples.master_three, GaussianMomentsCounterexamples.naturalMoment3_power_expansion, GaussianMomentsCounterexamples.expectation_normalizedSub3
- Dependencies: p3, integrability, contraction, real-gaussian, three-coefficient-proof, algebraic-integral-bridge
- Remaining: None. Full arbitrary-A, all-positive-m identity under actual Gaussian integration.

### three-coefficient-proof

- Status: proved
- Class: core
- Origin: Paper calculation, original construction, or formal proof dependency.
- Location: thm:three, coefficient proof
- Obligation: For arbitrary A and m≥1, the full finite central-binomial coefficient sum equals coeff_m(A(1+z)^(m−1)), using 1+z(2+z)=(1+z)² and the normalized formal branch.
- Lean: GaussianMomentsCounterexamples.coefficient_identity_three, GaussianMomentsCounterexamples.coeff_mul_subst_X_mul
- Dependencies: central-binomial
- Remaining: None. The Gaussian expansion itself is covered by master-three.

### moments-three

- Status: proved
- Class: core
- Origin: Paper calculation, original construction, or formal proof dependency.
- Location: eq:counterexample-three
- Obligation: All positive pure moments zero; all positive Q₃-mixed moments m!≠0
- Lean: GaussianMomentsCounterexamples.P3_moment, GaussianMomentsCounterexamples.Q3_P3_moment, GaussianMomentsCounterexamples.Q3_P3_moment_ne_zero
- Dependencies: master-three
- Remaining: None. Mixed moment is nonzero for every positive exponent.

### egf-three

- Status: proved
- Class: supporting
- Origin: Paper calculation, original construction, or formal proof dependency.
- Location: eq:egf-three
- Obligation: Formal expectation EGFs are 1 and t/(1−t)
- Lean: GaussianMomentsCounterexamples.momentEGF, GaussianMomentsCounterexamples.mixedMomentEGF, GaussianMomentsCounterexamples.P3_momentEGF, GaussianMomentsCounterexamples.Q3_P3_mixedMomentEGF
- Dependencies: moments-three, explicit-half-pair
- Remaining: None. Formal series; mixed constant term proved separately. No analytic exponential integrals.

### dimensions

- Status: proved
- Class: core
- Origin: Paper calculation, original construction, or formal proof dependency.
- Location: cor:dimensions
- Obligation: ¬GMC(n) for every n≥3 with actual eventual-vanishing quantifiers
- Lean: GaussianMomentsCounterexamples.not_GMC_three, GaussianMomentsCounterexamples.not_GMC_of_three_le, GaussianMomentsCounterexamples.not_GMC_four, GaussianMomentsCounterexamples.not_GMC_158
- Dependencies: moments-three, moments-four, marginal, gmc-definition
- Remaining: None. The 158-dimensional consequence here is direct coordinate extension, not the separate Jacobian-reduction route.

### gmc-one

- Status: blocked
- Class: supporting
- Origin: Cited background or cited reduction machinery.
- Location: §5, GMC(1)
- Obligation: Known GMC(1) result; only dimension two remains
- Lean: none
- Dependencies: none
- Remaining: Need the cited complex-polynomial Gaussian/Hermite image theorem or the alternate characteristic-p valuation argument. Real-coefficient positivity does not establish GMC(1) for complex polynomials.

### good

- Status: blocked
- Class: supporting
- Origin: Cited background or cited reduction machinery.
- Location: eq:good
- Obligation: General multivariate formal Lagrange–Good identity and unique formal inverse branch
- Lean: none
- Dependencies: contraction
- Remaining: Need general multivariate fixed-point existence/uniqueness and determinant-weighted coefficient identity (or residue change of variables). Explicit Discovery calculations do not imply the arbitrary-H theorem.

### explicit-h

- Status: proved
- Class: supporting
- Origin: Paper calculation, original construction, or formal proof dependency.
- Location: §6, explicit H
- Obligation: Displayed H gives P₄; g=(t,t/(1−t)) solves g=tH(g) and determinant is 1
- Lean: GaussianMomentsCounterexamples.discoveryHPolynomial_eval, GaussianMomentsCounterexamples.discoveryBranch_equation, GaussianMomentsCounterexamples.discoveryBranch_unique, GaussianMomentsCounterexamples.discoveryJacobian_correspondence, GaussianMomentsCounterexamples.discovery_determinant, GaussianMomentsCounterexamples.naturalP4_discovery_correspondence
- Dependencies: p4
- Remaining: None for the explicit formal branch, uniqueness, polynomial Jacobian correspondence, and determinant. General Good inversion remains separate.

### half-pair

- Status: blocked
- Class: supporting
- Origin: Cited background or cited reduction machinery.
- Location: eq:half-pair
- Obligation: General formal half-pair expectation identity
- Lean: none
- Dependencies: real-gaussian, contraction
- Remaining: Need general univariate Lagrange coefficient inversion with the Gaussian-square factor for arbitrary h,v,A. The explicit h=1+z and specified v calculations are proved separately.

### explicit-half-pair

- Status: proved
- Class: supporting
- Origin: Paper calculation, original construction, or formal proof dependency.
- Location: §6, explicit half-pair
- Obligation: ζ=t/(1−t), denominator 1−t, 1−2tv(ζ)=(1−t)^(−2), normalized square root cancels
- Lean: GaussianMomentsCounterexamples.branchZeta_eq, GaussianMomentsCounterexamples.halfPair_branch_equation, GaussianMomentsCounterexamples.halfPair_denominator, GaussianMomentsCounterexamples.halfPair_radicand_inverse, GaussianMomentsCounterexamples.halfPair_inverse_sqrt, GaussianMomentsCounterexamples.halfPair_inverse_sqrt_unique, GaussianMomentsCounterexamples.halfPair_cancellation
- Dependencies: p3
- Remaining: None for explicit formal branch calculations and normalized inverse-square-root cancellation; general half-pair theorem remains separate.

### weights

- Status: proved
- Class: supporting
- Origin: Paper calculation, original construction, or formal proof dependency.
- Location: §7, weights and factorial functional
- Obligation: Expectation kills nonzero weights; integral (ZW)^j=j!
- Lean: GaussianMomentsCounterexamples.pairExpectation_eq_zero_of_weight, GaussianMomentsCounterexamples.factorialFunctional_X_pow, GaussianMomentsCounterexamples.pairExpectation_radial
- Dependencies: contraction
- Remaining: None. The two-coordinate functional is definitionally genuine Gaussian expectation after the normalized substitution.

### one-sided-weights

- Status: proved
- Class: supporting
- Origin: Paper calculation, original construction, or formal proof dependency.
- Location: §7, one-sided weights
- Obligation: Strictly positive or strictly negative weight support implies eventual mixed-moment vanishing
- Lean: GaussianMomentsCounterexamples.one_sided_eventual_vanishing, GaussianMomentsCounterexamples.one_sided_eventual_vanishing_real
- Dependencies: weights
- Remaining: None. sign=1 and sign=-1 cover positive/negative weights; arbitrary original-coordinate multipliers are covered using the inverse substitution.

### homogeneous-exclusion

- Status: blocked
- Class: supporting
- Origin: Cited background or cited reduction machinery.
- Location: §7, homogeneous exclusion
- Obligation: Homogeneous polynomials cannot witness GMC(2) failure
- Lean: none
- Dependencies: one-sided-weights
- Remaining: A checked one-variable Duistermaat–van der Kallen theorem exists in the sibling MathieuProperty project. Remaining: pin/port and audit its 3,745-line dependency closure and licenses, then prove the homogeneous Gaussian-to-Laurent constant-term correspondence with parity cases. Full multivariate DvK is unnecessary here.

### radial-exclusion

- Status: blocked
- Class: supporting
- Origin: Cited background or cited reduction machinery.
- Location: §7, radial exclusion
- Obligation: All moments zero for P∈ℂ[ZW] forces P=0
- Lean: none
- Dependencies: weights
- Remaining: Need one-variable factorial rigidity for arbitrary complex coefficients: all L(f^m)=0 implies f=0. Missing finitely generated coefficient-ring / characteristic-p prime-divisibility argument from VEWZ Theorem 4.9.

### two-weight-moments

- Status: proved
- Class: supporting
- Origin: Paper calculation, original construction, or formal proof dependency.
- Location: §7, odd/even formula
- Obligation: For P=ZA(U)+WB(U), odd moments zero and even moment choose(2r,r) L((UAB)^r)
- Lean: GaussianMomentsCounterexamples.twoWeight_actual_odd_moment, GaussianMomentsCounterexamples.twoWeight_actual_even_moment
- Dependencies: weights
- Remaining: None. All r including zero and arbitrary complex polynomials A,B; no factorial-rigidity theorem assumed.

### two-weight-exclusion

- Status: partial
- Class: supporting
- Origin: Paper calculation, original construction, or formal proof dependency.
- Location: §7, two-weight exclusion
- Obligation: All moments zero forces A=0 or B=0, hence eventual vanishing
- Lean: GaussianMomentsCounterexamples.twoWeight_actual_odd_moment, GaussianMomentsCounterexamples.twoWeight_actual_even_moment, GaussianMomentsCounterexamples.one_sided_eventual_vanishing_real
- Dependencies: two-weight-moments, radial-exclusion
- Remaining: The moment formulas and one-sided conclusion are proved, but deriving A=0 or B=0 from all moments zero still needs the unformalized factorial-rigidity theorem.

### gaussian-space

- Status: proved
- Class: core
- Origin: Paper calculation, original construction, or formal proof dependency.
- Location: §1 / §3 Gaussian semantics
- Obligation: Canonical finite product of genuine standard real Gaussian measures and complex polynomial evaluation
- Lean: GaussianMomentsCounterexamples.gaussianMeasure, GaussianMomentsCounterexamples.realEval
- Dependencies: none
- Remaining: None; definition uses gaussianReal 0 1 and Measure.pi.

### integrability

- Status: proved
- Class: core
- Origin: Paper calculation, original construction, or formal proof dependency.
- Location: All polynomial expectation displays
- Obligation: Every complex polynomial is Bochner-integrable on the canonical product Gaussian space
- Lean: GaussianMomentsCounterexamples.integrable_realEval
- Dependencies: gaussian-space
- Remaining: None; proved by monomial integrability and finite-sum closure.

### product-factorization

- Status: proved
- Class: core
- Origin: Paper calculation, original construction, or formal proof dependency.
- Location: §3, independence
- Obligation: Actual monomial integrals factor into one-coordinate integrals
- Lean: GaussianMomentsCounterexamples.expectation_monomial
- Dependencies: integrability
- Remaining: None; mathlib finite-product integration.

### marginal

- Status: proved
- Class: core
- Origin: Paper calculation, original construction, or formal proof dependency.
- Location: cor:dimensions proof
- Obligation: Any injective coordinate selection preserves the Gaussian law and polynomial integrals; failure propagates to larger dimensions
- Lean: GaussianMomentsCounterexamples.gaussianMeasure_marginal, GaussianMomentsCounterexamples.expectation_rename, GaussianMomentsCounterexamples.not_GMC_of_le
- Dependencies: gaussian-space, integrability
- Remaining: None; application to the explicit witnesses remains in dimensions.

### stein

- Status: proved
- Class: core
- Origin: Paper calculation, original construction, or formal proof dependency.
- Location: Alternative proof of eq:contraction
- Obligation: For every complex polynomial P and coordinate i, expectation(X_i P)=expectation(∂_i P)
- Lean: GaussianMomentsCounterexamples.expectation_X_mul
- Dependencies: product-factorization, real-moment-recurrence
- Remaining: None; alternative to rotational invariance, using one-dimensional Gaussian integration by parts.

### real-moment-recurrence

- Status: proved
- Class: core
- Origin: Paper calculation, original construction, or formal proof dependency.
- Location: eq:real-gaussian, proof dependency
- Obligation: All odd standard real Gaussian moments vanish; moments satisfy μ_(k+1)=k μ_(k−1), including k=0
- Lean: GaussianMomentsCounterexamples.real_gaussian_moment_recurrence, GaussianMomentsCounterexamples.real_gaussian_odd_moment, GaussianMomentsCounterexamples.complex_gaussian_moment_succ
- Dependencies: integrability
- Remaining: None; density integration by parts with integrability of both derivative products.

### four-coefficient-proof

- Status: proved
- Class: core
- Origin: Paper calculation, original construction, or formal proof dependency.
- Location: prop:four proof
- Obligation: For every polynomial A and m≥1, the finite alternating coefficient sum equals coeff_m(A(1+z)^(m−1))
- Lean: GaussianMomentsCounterexamples.coefficient_identity_four
- Dependencies: none
- Remaining: None. Formal geometric-series inversion and exact finite coefficient extraction (equivalent to the manuscript finite alternating proof).

### algebraic-integral-bridge

- Status: proved
- Class: core
- Origin: Paper calculation, original construction, or formal proof dependency.
- Location: Both master identities
- Obligation: Natural-coordinate algebraic moment maps equal actual Gaussian integrals after normalized coordinate substitution
- Lean: GaussianMomentsCounterexamples.expectation_normalizedSub3, GaussianMomentsCounterexamples.expectation_normalizedSub4
- Dependencies: contraction, real-gaussian, integrability
- Remaining: None. Agreement for every complex polynomial, proved on monomials and extended by complex linearity.
