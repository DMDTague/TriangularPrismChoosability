# Independent audit

This directory is an independent re-implementation of the computer-assisted parts of the proof. It was written from the manuscript, separately from `checks/`, and added in release v1.1.0.

- `REPORT.md`: findings, verdict, discrepancies and their status, and reproduction commands.
- `a1_certificate.py`: rebuilds the Proposition 4.7 dual certificate and compares all 71 appendix rows, parsed from `paper/main.tex`.
- `a2_model_validation.py`: checks the 71-variable model against brute-force house counts.
- `a3_house_census.c`: House Lemma census over all 31 membership types, with base lists of size k−1 and k.
- `a4_identities.py`: the displayed identities, checked symbolically and by brute force.
- `a5_prism_census.c`: direct check of Theorem 1.1 over membership-type count vectors.
- `a6_validate.py`: validates the inclusion–exclusion count, and checks fact (F2) for C4 with m = 2–5.
- `outputs/`: recorded outputs. `outputs/repository_reruns/` holds the reruns of `checks/`.

Run `make audit` (about 2.5 minutes) or `make audit-long` (about 15 minutes) from the repository root.
