# Small Counterexamples to the Gaussian Moments Conjecture

Christopher D. Long

[arXiv:2607.18186](https://arxiv.org/abs/2607.18186) · [Paper PDF](gaussian_moments_counterexamples.pdf) · [LaTeX source](gaussian_moments_counterexamples.tex)

[![Build and audit Lean](https://github.com/long-mathematics/gaussian-moments-counterexamples/actions/workflows/lean-ci.yml/badge.svg)](https://github.com/long-mathematics/gaussian-moments-counterexamples/actions/workflows/lean-ci.yml)

[![Build paper and verify identities](https://github.com/long-mathematics/gaussian-moments-counterexamples/actions/workflows/verification.yml/badge.svg)](https://github.com/long-mathematics/gaussian-moments-counterexamples/actions/workflows/verification.yml)

This companion repository contains the manuscript, Lean proofs, and independent
exact computational checks for the explicit Gaussian-moment counterexamples.

**The paper’s core Gaussian counterexamples and failure of GMC(n) for every n ≥ 3
are formalized in Lean.** The following supporting claims remain to be formalized:
the full Bass–Connell–Wright reduction route and DVEZ/Zhao implication; general
Lagrange–Good and half-pair inversion; GMC(1); and the cited rigidity results and
correspondences needed for the homogeneous, radial, and two-weight exclusions in
dimension two. See the [coverage ledger](FORMALIZATION_STATUS.md) and
[audit report](FORMALIZATION_AUDIT.md) for exact statements and dependencies.
Full-paper coverage is not claimed.

## Abstract

We give explicit complex polynomials $P,Q$ in three independent standard real
Gaussian variables such that

$$
\mathbb E(P^m)=0,\qquad \mathbb E(QP^m)=m!\neq0
$$

for every $m\geq1$. In natural complex linear coordinates, $P$ has five terms and
total degree $4$. Hence the Gaussian Moments Conjecture is false in every
dimension $n\geq3$. We also give a six-term cubic example in four variables,
which was found first and already proves failure for every $n\geq4$. Both examples
follow from the same coefficient identity.

The search was prompted by Levent Alpöge's public announcement of an explicit
three-dimensional counterexample to the Jacobian Conjecture. Although the main
theorem of Derksen, van den Essen, and Zhao is stated globally in dimension, its
proof has fixed-dimensional content: a noninvertible cubic-homogeneous Keller map
in $r$ variables forces the failure of $\mathrm{GMC}(2r)$. Tracking a standard
Bass--Connell--Wright reduction of the announced map gives a conservative
cubic-homogeneous counterexample in $79$ variables, and hence a route-based
failure of $\mathrm{GMC}(158)$. That route is nonconstructive at the final Gaussian
step and does not furnish explicit polynomials $P,Q$. The much smaller explicit
failures in dimensions $4$ and $3$ were not derived from the announced Jacobian map.

## Repository contents

| Path | Purpose |
| --- | --- |
| `gaussian_moments_counterexamples.tex` | Canonical manuscript source |
| `gaussian_moments_counterexamples.pdf` | Tracked paper PDF |
| `scripts/verify_gaussian_moments_counterexamples.py` | Exact finite-moment, Jacobian-map, support-count, and dimension-bound checks |
| `scripts/verify_gaussian_moments_counterexamples.txt` | Checked reference output |
| `scripts/check_verification.py` | Reproducibility runner requiring exact output agreement |
| `GaussianMomentsCounterexamples.lean` | Umbrella import for all Lean proofs |
| `FORMALIZATION_STATUS.md` | Statement-level coverage and remaining obligations |
| `FORMALIZATION_AUDIT.md` | Current proof, correspondence, and verification evidence |
| `CITATION.cff` | Citation metadata and arXiv DOI |

## Lean proofs

The root Lake project pins **Lean 4.34.0** and mathlib commit
`5ed2965256430c3649e86755f9576b54eca72435`; transitive dependencies are locked in
`lake-manifest.json`. With [elan](https://github.com/leanprover/elan) installed:

```sh
python3 scripts/fetch_mathlib_cache.py
lake build
python3 scripts/audit_source.py
lake env lean scripts/audit_lean.lean
lake env lean scripts/statement_audit.lean
```

For a clean rebuild of owned proofs, remove only `.lake/build` and repeat the
build and audits, retaining the pinned dependency caches in `.lake/packages`.

The master theorems quantify over every complex polynomial A and every positive
exponent. Their expectations are genuine Bochner integrals under finite products
of standard real Gaussian measures, with integrability proved for every complex
polynomial. An unconditional bridge identifies these integrals with the algebraic
moment functionals. The support counts refer to the displayed complex coordinates;
invertible substitutions also prove the degrees in the original real coordinates.

Supporting proofs include the formal generating functions, explicit inverse
branches, the announced map’s determinant and collision, target normalization and
support counts, recurrence arithmetic, real-coefficient obstruction, and elementary
dimension-two weight and odd/even moment formulas. `not_GMC_158` follows by direct
dimension extension; it does **not** certify the separate Jacobian-reduction route.

The source audit checks all owned Lean files, root imports, ledger references and
acyclic dependencies. The axiom audit checks every declaration by originating
module, including private and generated declarations, and permits only
`propext`, `Classical.choice`, and `Quot.sound`. The statement inspection script
exposes elaborated definitions and theorem types for the separate mathematical
correspondence review; its successful execution alone is not that review.

## Build the paper

With TeX Live and latexmk installed:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error gaussian_moments_counterexamples.tex
```

The PDF is intentionally tracked; LaTeX auxiliary files are ignored.

## Reproduce the exact checks

Python 3 and the pinned SymPy dependency are sufficient:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r scripts/requirements.txt
python scripts/check_verification.py
```

The runner executes the verifier with assertions enabled and requires a successful
exit, empty standard error, and byte-for-byte agreement with the checked-in output.
It checks finite instances of both explicit Gaussian examples, the Jacobian
determinant and point collision of the announced map, its high-degree support, and
the dimension count $s=39$, $r=79$, hence $\neg\mathrm{GMC}(158)$ along the tracked
route. The finite moment computations are diagnostics; the Lean master identities prove
the Gaussian moment formulas for every positive $m$. The Python route arithmetic
is not a formal proof of the reduction transformations.

## Citation and license

Cite the paper using [arXiv:2607.18186](https://arxiv.org/abs/2607.18186)
or [doi:10.48550/arXiv.2607.18186](https://doi.org/10.48550/arXiv.2607.18186).
See [CITATION.cff](CITATION.cff). This repository is distributed under the
[MIT License](LICENSE).
