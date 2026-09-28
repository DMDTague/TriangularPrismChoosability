# Triangular Prism Choosability

Publication and reproducibility materials for the paper

> **The triangular prism is enumeratively chromatic-choosable**

by Dylan Tague.

This repository contains the manuscript and a compact, self-contained verification package for the computer-assisted parts of the proof. The repository is intentionally limited to the mathematics, source code, recorded outputs, and reproducibility metadata needed for publication and review.

## Main result

For every positive integer (m), the triangular prism (K_3\square K_2) satisfies

[
P_\ell(K_3\square K_2,m)=P(K_3\square K_2,m).
]

Equivalently, because (K_3\square K_2=L(K_{2,3})), every assignment of (k)-element lists to the six edges of (K_{2,3}) has at least

[
k(k-1)(k-2)(k^3-6k^2+14k-13)
]

proper list edge-colourings.

## Repository layout

- `paper/main.tex` — manuscript source.
- `paper/main.pdf` — compiled manuscript.
- `checks/certificate_rebuild.py` — exact symbolic rebuild of the 71-variable dual certificate used for unequal shoulder lists.
- `checks/house_type_enumeration.cpp` — complete membership-type enumeration used for (k=4,5).
- `checks/paper_checks.py` — exact symbolic and small brute-force checks of the remaining displayed identities.
- `checks/bruteforce_small_universes.c` — end-to-end brute-force checks over small colour universes.
- `outputs/` — recorded outputs for the verification programs.
- `Makefile` — convenience targets for reproduction.
- `requirements.txt` — Python dependency information.
- `CITATION.cff` — citation metadata.

## Reproducing the checks

Requirements:

- Python 3
- SymPy
- a C++17 compiler
- a C compiler

Install the Python dependency:

```bash
python3 -m pip install -r requirements.txt
```

Then run:

```bash
make verify
```

The complete (k=4,5) membership-type census can also be run separately:

```bash
make census
```

The expected key census values are:

| (k) | type configurations | minimum (h-\mathrm{target}) | deficient configurations |
|---:|---:|---:|---:|
| 4 | 49,394 | -4 | 1 |
| 5 | 519,800 | -12 | 1 |

In both cases the unique deficient type configuration is the extremal configuration (Delta) described in the manuscript.

The exact symbolic certificate rebuild verifies the 71 linear residual inequalities in Appendix A, including the (2,348/82) quadratic sign split and minimum residual (443/2) at (k=10).

## Reproducibility scope

The computer-assisted parts of the argument are isolated in the manuscript. The verification package uses exact integer or rational arithmetic for the certificate and enumeration steps. Recorded outputs are included so that a referee can compare a fresh run directly against the archived results.

## Archival release

A DOI will be added here after the publication snapshot is released through Zenodo.
