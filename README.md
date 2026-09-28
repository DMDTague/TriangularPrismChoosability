# TriangularPrismChoosability

Reproducibility materials for

> **Dylan Tague, _The triangular prism is enumeratively chromatic-choosable_.**

The paper proves that the triangular prism $K_3\square K_2$ is enumeratively chromatic-choosable. Equivalently, for every $k\ge 3$, every assignment of $k$-element lists to the six edges of $K_{2,3}$ has at least

$
k(k-1)(k-2)(k^3-6k^2+14k-13)
$

proper list edge-colourings.

This repository contains the manuscript and a compact set of exact verification programs for the computer-assisted parts of the proof. It intentionally contains only publication-facing mathematical material and reproducibility code.

## Repository layout

- `paper/main.tex` - LaTeX source of the manuscript.
- `checks/certificate_rebuild.py` - independently reconstructs the 71-variable unequal-shoulder certificate from the House Lemma formula and verifies the residual table and fixed-$k$ certificates.
- `checks/paper_checks.py` - exact symbolic and small-case checks for the equal-pair/equal-shoulder arguments, compensation identities, and related polynomial identities used in the paper.
- `checks/house_type_enumeration.cpp` - complete membership-type enumeration used for the House Lemma at $k=4,5$.
- `checks/bruteforce_small_universes.c` - direct small-universe brute-force checks of the prism theorem and House Lemma.
- `outputs/` - recorded outputs for the principal checks.

## Requirements

For the Python checks:

```text
Python 3.10+
sympy
```

For the enumeration programs, a C/C++ compiler is required. The commands below use GCC/Clang-compatible `cc` and `c++`.

To install the Python dependency:

```bash
python -m pip install -r requirements.txt
```

## Reproduce the computer-assisted proof components

Run all commands from the repository root.

### 1. Rebuild the unequal-shoulder certificate

```bash
python checks/certificate_rebuild.py
```

This reconstructs the quadratic polynomial from the shoulder-first formula and checks, exactly:

- 2,430 nonzero quadratic coefficients among the 2,556 possible quadratic monomials;
- the sign split `2348` nonnegative / `82` nonpositive for every integer $k\ge 6$;
- the charged linear coefficients printed in the manuscript;
- all 71 dual residual polynomials;
- the largest real residual root (approximately `8.351`);
- `min r_v(10) = 443/2`;
- the fixed certificates for $k=6,7,8,9$.

The recorded output is `outputs/certificate_rebuild.txt`.

### 2. Check the remaining symbolic identities

```bash
python checks/paper_checks.py
```

This checks the equal-pair and equal-shoulder formulas, the minimal patterns in the equal-shoulder case, the compensation identities, the ordinary colouring count, and related polynomial identities. It also compares several formulas with direct brute-force counts for small $k$.

The recorded output is `outputs/paper_checks.txt`.

### 3. Complete type enumeration for the House Lemma

Compile:

```bash
c++ -O2 -std=c++17 checks/house_type_enumeration.cpp -o house_type_enumeration
```

Run the two values needed by the proof:

```bash
./house_type_enumeration 4
./house_type_enumeration 5
```

Expected headline results:

```text
k=4: type-configs=49394   min(S-target)=-4    deficient outside family=0
k=5: type-configs=519800  min(S-target)=-12   deficient outside family=0
```

Thus the minimum is exactly $-\sigma_k$, and the only configuration below the common-palette target is the extremal configuration $\Delta$.

Recorded outputs are `outputs/house_type_k4.txt` and `outputs/house_type_k5.txt`.

### 4. Direct small-universe brute force

Compile:

```bash
cc -O2 checks/bruteforce_small_universes.c -o bruteforce_small_universes
```

Examples for the full prism theorem:

```bash
./bruteforce_small_universes 1 3 6
./bruteforce_small_universes 1 4 6
./bruteforce_small_universes 1 5 7
```

A direct small-universe House Lemma check is:

```bash
./bruteforce_small_universes 2 4 8
```

The first three commands provide end-to-end checks of the prism theorem for $k=3,4,5$. They respectively examine 3,200,000, 759,375, and 4,084,101 normalized list assignments and attain the ordinary counts $c_3=12$, $c_4=264$, and $c_5=1920$, with no smaller count. The final command checks the House Lemma directly over an eight-colour universe at $k=4$.

Recorded outputs are in `outputs/bruteforce_*.txt`.

## One-command checks

```bash
make verify
```

runs the symbolic certificate rebuild, the paper checks, and the complete type enumerations for $k=4,5$.

```bash
make brute
```

runs the three end-to-end prism brute-force checks above. `make house-brute` runs the separate direct House Lemma check.

```bash
make paper
```

builds `paper/main.pdf` locally with `latexmk` (the generated PDF is not tracked in the repository).

## What is computer-assisted?

The mathematical reduction and assembly of the proof are given in the manuscript. Computation is essential in two places:

1. the exact dual-certificate verification for the unequal-shoulder case; and
2. the complete membership-type enumeration for $k=4,5$.

All arithmetic in the supplied verification programs is exact except for the displayed decimal approximation of the largest real root; the proof uses exact real-root isolation.

## Archival citation

A versioned release of this repository is intended to be archived on Zenodo. The Zenodo DOI and the arXiv identifier will be added here and to the manuscript once minted.


## License

The verification code and build scripts are licensed under the MIT License; see `LICENSE-CODE`. The manuscript and other authored textual material are licensed under Creative Commons Attribution 4.0 International (CC BY 4.0); see `LICENSE-TEXT`. The root `LICENSE` file summarizes this split licensing.
