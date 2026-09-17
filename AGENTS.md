# Repository instructions

## Manuscript and integrity

- The canonical source is `gaussian_moments_counterexamples.tex`; its PDF is tracked.
- Preserve mathematical statements, hypotheses, proof content, authorship, notation,
  and stable labels unless explicitly instructed to change them.
- Flag suspected mathematical errors; do not silently repair or weaken claims.
- Keep mathematical changes separate from migration and editorial changes.
- Compile with `latexmk -pdf -interaction=nonstopmode -halt-on-error gaussian_moments_counterexamples.tex`.
  Check undefined citations/references and layout warnings before committing a new PDF.
- Do not commit LaTeX auxiliary files or build caches.

## Exact verification

- Auxiliary verification scripts and checked outputs belong in `scripts/`.
- Install `scripts/requirements.txt` and run `python scripts/check_verification.py`.
- Do not silently regenerate expected outputs to make checks pass.
- Changes to the verifier or its reference output must be explicit and reviewed.
- Finite computational checks are diagnostics, not proofs of the manuscript's
  all-moment coefficient identities or a full formalization of the paper.

## Future Lean formalization

- Use a root Lake project and a `GaussianMomentsCounterexamples/` module directory;
  do not create a separate `formalization/` subtree.
- Put the umbrella module at `GaussianMomentsCounterexamples.lean`, auxiliary Lean
  audits in `scripts/`, and the coverage ledger at `FORMALIZATION_STATUS.md`.
- Never introduce `sorry`, `admit`, custom axioms, or hypotheses that assume the
  conclusion. Audit transitive dependencies as well as source text.
- Distinguish proved, partial, unverified, and missing claims. Do not claim full-paper
  coverage before statement correspondence and transitive-axiom audits are complete.

## Git workflow

Use a feature branch, pull request, successful applicable CI, and squash merge.
Never bypass protections, force-push main, or overwrite unique source material.

## Documentation

Keep this tree a current paper companion, not a development archive. The README
covers the abstract, paper links, reproducible checks, citation, and license. Do
not add local source paths, migration narratives, old drafts, redundant historical
documents, or obsolete build logs.

