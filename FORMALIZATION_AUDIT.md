# Formalization audit

## Verified scope

The paper’s core Gaussian counterexamples and failure of GMC(n) for every n ≥ 3
are formalized in Lean. This is **core-complete, not full-paper coverage**.
The [coverage ledger](FORMALIZATION_STATUS.md) records exact statements,
declarations, dependencies, supporting omissions, and partial results.

The proof uses Lean **4.34.0** and mathlib commit
`5ed2965256430c3649e86755f9576b54eca72435`, with all transitive revisions in
`lake-manifest.json`. It follows the root Lake organization and integrity
conventions of the missing-mass, Poisson-binomial, and rank-two companions.

## Mathematical correspondence

The implementation and a separate adversarial review inspected source proofs and
actual elaborated declarations, using `scripts/statement_audit.lean` to expose
final types and unfolded definitions. The following points were checked:

- `gaussianMeasure n` is the finite product of `gaussianReal 0 1` on `Fin n → ℝ`.
  `realEval` evaluates genuine complex-coefficient multivariate polynomials on
  real coordinates, and `expectation` is the Bochner integral. Every polynomial
  evaluation is integrable by `integrable_realEval`, including all mixed powers.
- Real Gaussian moments follow from integration by parts with integrability of
  the derivative products. Complex contractions follow from the resulting
  polynomial Stein identities. This is an alternative to invoking rotational
  invariance; no contraction rule or distributional equivalence is postulated.
- Normalization is `(√2)⁻¹`, with Z using `+iY` and W using `−iY`.
  Evaluation formulas, real-input conjugacy, two-sided coordinate algebra
  equivalences, and degree preservation are proved. The counts five and six
  concern `naturalP3` and `naturalP4`, not their real-coordinate expansions.
- `expectation_normalizedSub3` and `expectation_normalizedSub4` identify the
  algebraic moment maps with actual integration for **every** polynomial.
  Residual-derivative conditions in the generic contraction lemma are discharged
  explicitly in these proofs. The bridges have no contraction assumptions.
- `master_three` and `master_four` quantify over arbitrary `A : Polynomial ℂ`
  and every natural `m` with `1 ≤ m`, with precisely the coefficient of
  `A * (1 + X)^(m−1)`. Both derive from finite coefficient extraction. The
  three-variable proof checks the inverse-square-root branch by its constant
  coefficient one; it does not assume an analytic generating function.
- `GMC` quantifies universally over P and Q, assumes all positive pure moments
  vanish, and requires `∃ N, ∀ m ≥ N` mixed vanishing. The witnesses contradict
  this at `max N 1`. Higher dimensions use a proved measure-preserving Gaussian
  marginal for injective coordinate selection, not a witness-specific definition.
- Formal EGF definitions divide each polynomial moment by its factorial. The
  mixed constant terms are checked. Explicit discovery calculations include
  polynomial-Jacobian correspondence and normalized square-root uniqueness;
  they do not assert general Lagrange inversion or analytic exponential integrals.

The supporting development also verifies the announced polynomial map's actual
partial-derivative determinant, distinct collision points, noninjectivity,
target linear equivalence, identity linear part, and exact high-degree support.
Dimension-two support bounds prove eventual vanishing for arbitrary multipliers;
the factorial-functional and odd/even formulas use actual Gaussian integration.
The real-coefficient obstruction uses full support and integrability, not a
positivity argument for complex coefficients.

## Automated integrity checks

- `scripts/audit_source.py` scans all owned Lean sources, checks the complete root
  import closure, validates every manuscript equation/result label in the ledger,
  rejects missing/circular dependency references, and elaborates every listed
  declaration reference. Proved entries cannot depend on incomplete entries.
- `scripts/audit_lean.lean` selects every declaration by its **originating module**,
  including private/generated declarations and names outside the public namespace.
  It traverses their axiom dependencies and permits only `propext`,
  `Classical.choice`, and `Quot.sound`. Source scans are not a substitute for this.
- The separate statement inspection exposes definitions and theorem types for
  mathematical review. A successful build or inspection-script exit does not
  mechanically prove correspondence with the manuscript.
- `.github/workflows/lean-ci.yml` uses commit-pinned actions, read-only permissions,
  the locked toolchain/dependencies, dependency-only caches, builds of owned proofs,
  both audits, and statement inspection. Existing paper/verifier CI is preserved.

Local release validation on September 17, 2026 passed after moving all owned build
artifacts out of the active build directory and rebuilding from source, retaining
only the dependency caches in the build search path:

| Check | Result |
| --- | --- |
| Clean `lake build` | All 21 project modules passed; no warnings |
| Source/import audit | 23 owned Lean files; complete root closure |
| Ledger/reference audit | 46 entries: 33 proved, 3 partial, 10 blocked; 109 checked declaration references; all 19 result/equation labels covered |
| Transitive axiom audit | 432 declarations, including 376 theorem constants; only the three permitted logical axioms |
| Elaborated statement inspection | Passed; separate core and supporting correspondence reviews found no mathematical mismatch |
| Independent Python verifier | Exact byte-for-byte reference-output match |
| Protected source comparison | Manuscript, PDF, verifier, reference output, citation metadata, and license unchanged |

Run-specific remote results are available in the
[Lean CI history](https://github.com/long-mathematics/gaussian-moments-counterexamples/actions/workflows/lean-ci.yml)
and [paper/verifier CI history](https://github.com/long-mathematics/gaussian-moments-counterexamples/actions/workflows/verification.yml).
The original Python verifier and checked output are unchanged and remain
independent finite diagnostics. The canonical manuscript, tracked PDF, citation
metadata, license, authorship, and provenance disclosures are unchanged.

## Supporting omissions and investigated proof routes

These omissions do not affect any core theorem. No cited result is added as an
axiom, and conditional arithmetic is not counted as a reduction construction.

- **BCW degree lowering, stable equivalence, nilpotence, and homogenization:**
  available polynomial composition, partial derivatives, homogeneous components,
  and matrix algebra do not supply the dimension-changing construction. Needed
  are explicit inverse elementary automorphisms for each stabilization,
  preservation of the Keller property and noninvertibility, a terminating
  degree/support bound, the construction-specific polynomial-matrix nilpotence
  argument, and noninvertibility transfer through cubic homogenization. The
  balanced recurrence and numbers 18, 39, 79, 158 are verified separately.
- **DVEZ/Zhao fixed-dimensional chain and the global implication:** the missing
  interfaces are the general differential-evaluation image/kernel theorem for
  ξ−∂, the uniform-threshold argument using countably many Zariski-closed sets,
  and the Abhyankar–Gurjar inverse-coefficient formula giving a polynomial inverse.
  The explicit two-pair Gaussian bridge does not prove this all-dimensional chain.
  See [DVEZ Propositions 3.1–3.2](https://arxiv.org/html/1506.05192v1) and
  [Zhao Theorem 3.7](https://arxiv.org/html/0902.0210v2).
- **General Lagrange–Good and half-pair identities:** the pinned library has
  scalar compositional inverse and formal substitution infrastructure. A general
  vector fixed-point construction and determinant-weighted coefficient theorem
  (or a residue change-of-variables theorem) are still needed. Multiplicative
  inversion of multivariate series is not inversion of a polynomial map. The
  verified explicit branches and cancellation identities do not establish the
  arbitrary-H or arbitrary-h,v statements.
- **GMC(1) and factorial rigidity:** the cited proofs require complex-coefficient
  Hermite/image or characteristic-p arguments. For radial rigidity, the missing
  bridge controls prime divisibility in finitely generated coefficient rings for
  arbitrary complex coefficients. Existing prime, valuation, and number-field
  infrastructure does not itself prove this theorem. See
  [VEWZ Theorem 4.9](https://arxiv.org/html/1008.3962v1). The two-weight exclusion
  depends on this same rigidity result; its odd/even moment formulas are proved.
- **Homogeneous GMC(2) exclusion:** a checked one-variable Duistermaat–van der
  Kallen result exists in the
  [MathieuProperty companion](https://github.com/long-mathematics/mathieu-property-compact-connected-lie-groups),
  with a six-module, approximately 3,745-line dependency closure involving
  valuation extensions, annulus series, and partial fractions. Reuse would require
  a pinned dependency or attributed port and transitive audit, followed by the
  homogeneous Gaussian-to-Laurent constant-term correspondence, including parity
  cases. This development does not import it or claim the exclusion. The stronger
  full multivariate DvK theorem is not needed for this particular step.

`not_GMC_158` is an unconditional consequence of the three-variable witness and
coordinate extension. The manuscript's separate Jacobian-to-GMC(158) route remains
partial, even though its input map and arithmetic have been checked. Unrestricted
GMC(2) is neither claimed nor attempted.
