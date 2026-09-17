# Small Counterexamples to the Gaussian Moments Conjecture

Christopher D. Long

[arXiv:2607.18186](https://arxiv.org/abs/2607.18186) · [Paper PDF](gaussian_moments_counterexamples.pdf) · [LaTeX source](gaussian_moments_counterexamples.tex)

[![Build paper and verify identities](https://github.com/long-mathematics/gaussian-moments-counterexamples/actions/workflows/verification.yml/badge.svg)](https://github.com/long-mathematics/gaussian-moments-counterexamples/actions/workflows/verification.yml)

This companion repository contains the manuscript and exact computational checks
for the explicit Gaussian-moment counterexamples and the conservative
Jacobian-reduction bound discussed in the paper.

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
| `CITATION.cff` | Citation metadata and arXiv DOI |

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
route. The finite moment computations are diagnostics; the displayed coefficient
identities in the paper prove the moment formulas for every $m$.

## Citation and license

Cite the paper using [arXiv:2607.18186](https://arxiv.org/abs/2607.18186)
or [doi:10.48550/arXiv.2607.18186](https://doi.org/10.48550/arXiv.2607.18186).
See [CITATION.cff](CITATION.cff). This repository is distributed under the
[MIT License](LICENSE).
