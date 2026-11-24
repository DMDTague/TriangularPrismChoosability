# Independent certificate audit: *The triangular prism is enumeratively chromatic-choosable*

Auditor: Claude (Anthropic), 23 November 2026.
Manuscript audited: `paper/main.tex` at tag `v1.0.0`, commit `87bd5d4880be9a6241d011693d44401e055a184d` (28 September 2026). Release `v1.1.0` revises citations and §7 only, with no change to the mathematics. All audit scripts were re-run against the v1.1.0 manuscript and give identical output.
All audit code in this folder was written from the manuscript, not adapted from the repository's `checks/`. All arithmetic is exact (integers, `sympy` rationals, exact real-root isolation).

## Verdict

**The central theorem is rigorously supported, on two conditions.**
1. **One external result has not been audited here.** Fact (F2) says every cycle is m-monophilic for every m ≥ 2. Its primary source is Kirov–Naimi, Theorem 1 (arXiv:1004.5183), which v1.1.0 cites. This audit checks it computationally only for C4 with m = 2–5.
2. **The computer-assisted steps must be correct.** They have now been reproduced from the public repository and independently re-implemented. Every result matches the manuscript.

No mathematical error was found. The issues listed in the Discrepancies section concern reproducibility claims, citations and release metadata. None affects the truth of the theorem.

## Proof dependency map

| k | Route in the manuscript | Status after audit |
|---|---|---|
| 3 | Cor. 3.3(i): cycle bound (F2) with d₃ = o₃ | Analytic; identity checked. Also confirmed by an exhaustive census over all colour universes (2,406,208 count vectors, min N = 12 = c₃). |
| 4, 5 | Reduction (§3) → House Lemma by complete type census (§5) → localisation and compensation (§5) → assembly (§6) | House Lemma independently re-enumerated, covering base lists of size k−1 **and** k, so the Lemma 4.2 size reduction is checked as well. |
| ≥ 6 | Same reduction → House Lemma via Prop. 4.5 (equal pairs), Prop. 4.6 (equal shoulders), Prop. 4.7 (LP dual certificate) → assembly | Certificate rebuilt independently. Model validated against brute force. All displayed identities re-derived. House Lemma census at k = 6 run as an extra cross-check. |

## A. Reproduction of the repository's own checks

All recorded outputs reproduce **byte-for-byte**. The reruns are in `rerun/`.

| Program | Result |
|---|---|
| `checks/certificate_rebuild.py` | identical to `outputs/certificate_rebuild.txt` |
| `checks/paper_checks.py` | identical to `outputs/paper_checks.txt` |
| `house_type_enumeration 4`, `5` | identical; 49,394 and 519,800 configurations, min −4 and −12 |
| `bruteforce_small_universes` (all four recorded runs) | identical (k = 3, U = 6; k = 4, U = 6; k = 5, U = 7; house k = 4, U = 8) |

## B. Independent re-implementation

### B1. Proposition 4.7 (unequal shoulders): `a1_certificate.py`
F₀ = h♯ − target was rebuilt symbolically in the 71 variables, with formula (4) derived independently: a sum over colour classes of U with a same-colour correction. Everything below agrees exactly with the manuscript.

- **Constant term:** c₀ = −2(k−1)(2k²−10k+13).
- **Quadratic monomials:** 2,430 nonzero of 2,556. For every integer k ≥ 6, **2,348 are nonnegative and 82 are nonpositive, with none mixed**. This was proved at k = 6–9 by evaluation and on [10, ∞) by a shift or by exact root isolation.
- **Constraint matrix:** all three "miss" rows of M were re-derived from |U| = k + b and |X| = k − 1, and match the appendix column formulas.
- **The 71-row appendix table** (parsed from `main.tex`): **0 mismatches** in ℓ′ᵥ, 0 in 10·rᵥ, 0 in rᵥ(10).
- **Polynomial multipliers:** y ≥ 0 and all 71 residuals ≥ 0 for every real k ≥ 9.
  - The largest real root of any residual is 8.3511.
  - The minimum residual is 1113/10 at k = 9 and 443/2 at k = 10.
  - c₀ + Σy = k(3k²+1)/10.
- **Fixed-k certificates (k = 6, 7, 8):** c₀, c₀ + Σy, the minimum residual (0) and the exact zero-residual sets all match Table 4.

**Soundness of the certificate chain.** I checked each step of F₀ ≥ c₀ + ℓ′·v ≥ c₀ + y·Mv ≥ c₀ + Σy:
1. The charging c·vᵢvⱼ ≥ c·k·vⱼ needs 0 ≤ vᵢ ≤ k. This holds because D₁₁₁ = k − ΣD − ΣZ ≥ 0.
2. Mv ≥ 1 holds because b ≥ 1 (L₂ ≠ L₄) and |U \ X| ≥ b + 1.
3. The multipliers y are nonnegative.

### B2. Model validation against brute force: `a2_model_validation.py`
I generated 5,928 random unequal-shoulder house assignments, at k = 6 and k = 7. For each one:
- brute-force h equals formula (4);
- h − target ≥ F₀(v) > 0 for the 71-variable encoding v.

The minimum of F₀(v) observed was 120 at k = 6 and 319 at k = 7. This tests that the symbolic model faithfully represents actual colourings, independently of the algebra.

### B3. House Lemma census: `a3_house_census.c`
This is a different parametrisation from the repository's: all 31 membership types in (L₂, L₄, A₁, A₃, R), including colours outside U, with base sizes in {k−1, k}.

| k | count vectors | min(h − target) | −σₖ | below target | below target and not Δ |
|---|---|---|---|---|---|
| 4 | 671,702 | −4 | −4 | 1 | 0 |
| 5 | 8,165,271 | −12 | −12 | 1 | 0 |
| 6 (cross-check) | 77,262,863 | −24 | −24 | 1 | 0 |

In each case the only configuration below the target is Δ, with |A₁| = |A₃| = k − 1. The count vectors differ from the manuscript's 49,394 and 519,800 only because the parametrisation differs; the conclusions are identical. The general-size counting formula used here was checked against brute force in `a4_identities.py`.

### B4. Displayed identities: `a4_identities.py`
All 27 checks pass. They cover:
- Lemma 2.1 (c_k);
- o_k − d_k = σ_k and d_k = P(C₄, k−1);
- Lemma 3.1 (gluing) and Lemma 3.4 (rows are house counts), on random instances;
- Cor. 3.3(ii);
- Prop. 4.5: f_C, f_V and f_O by brute force; D(r) with all four bullet facts; Δ attaining target − σ_k;
- Prop. 4.6: the equality example;
- Lemma 5.2: δ_x, δ_γ and δ_c by brute force for k = 4–7, and both sums;
- the q = 1 inequality in §6.

### B5. Direct checks of Theorem 1.1: `a5_prism_census.c`, `a6_validate.py`
These enumerate all membership-type count vectors for the six edge lists. The count is by inclusion–exclusion over the 9 prism edges, which `a6_validate.py` checks against brute force.

| k | colours allowed | count vectors | min N | c_k |
|---|---|---|---|---|
| 3 | unrestricted (complete) | 2,406,208 | 12 | 12 |
| 4 | ≤ 10 | 36,832,541 | 264 | 264 |
| 5 | ≤ 8 | 1,000,904 | 1,920 | 1,920 |

**For k = 3 this is a complete computer proof, independent of the paper's argument.** For k = 4 and 5 it covers larger colour universes than the repository's checks (U = 6 and U = 7).

**Fact (F2) for C₄:** every m-assignment has at least (m−1)⁴ + (m−1) colourings, for m = 2–5, over all colour universes.

## C. Proof-logic review (by hand)

- **Prop. 4.6, Case A.** The three hitting conditions are: some type in {010, 110}; some type in {000, 001, 100, 101}; some type in {000, 001, 010, 011}. Their minimal transversals are exactly the eight sets in the manuscript.
- **Prop. 4.6, Case B.** The constraint n₀₀₀ + n₁₀₀ ≥ 2 follows from |A₁ \ V| = n₀₀₀ + n₁₀₀ − 1 ≥ j ≥ 1. I accepted the monotonicity and the three minimal values from the repository's symbolic check and did not re-derive them independently. The House census at k = 4, 5, 6 independently confirms the conclusion in that range.
- **Prop. 4.5.** f_C − f_V at r = k − 1 equals σ_k. So a roof without γ gives h ≥ target, with equality allowed, and the uniqueness of Δ holds.
- **Lemmas 5.1–5.2 and §6.** Localisation forces x ∈ L(e₁) ∩ L(e₃) and x ∉ C. In the case q ≥ 2, every other inside row lies in B and is negative by compensation. The case analysis is complete.

## Discrepancies found, and their status

Resolved in release v1.1.0:
1. **Release tag.** `v1.0.0` now exists on commit `87bd5d4` and is kept unchanged as the historical snapshot.
2. **Claims the public package could not reproduce.** §7 cited census results for k = 6–9 and unpublished implementations. Those claims are gone; §7 now cites only the public checks and this `audit/` directory.
3. **(F2) citation.** It now cites the primary source, Kirov–Naimi Theorem 1. An attribution in §1 that credited Allred–Mudrock with the cycle result is corrected.
4. **Companion-paper reference.** The Zenodo DOI 10.5281/zenodo.23018085 has been added. Allred–Mudrock now cites the journal version.

Still open:
5. **Zenodo DOI for v1.1.0.** Insert it in the data-availability statement (marked TODO in `paper/main.tex`) and in the root README.
6. **Two manuscript versions.** The author's archive copy (27 September) is older than the repository version; update it.
7. **Check:** "Question 11.4" in the deposited Zenodo PDF of the companion paper; the Kirov–Naimi theorem number in the Ars Combin. version; the Allred–Mudrock DOI; ZD26, ZD26np, CLMNW and the Kirov Lean commit.
8. **Not verified, and not used in the proof:** the §7 remark that the dual LP is infeasible for k = 4, 5.

## Reproduce

Run everything from the repository root. You need Python 3.10+ with `sympy`, and a C compiler. Compiled binaries are built as hidden files, deleted afterwards, and not tracked.

```bash
make audit        # about 2.5 minutes: everything except the long runs
make audit-long   # about 15 minutes: House census at k = 6 and the larger prism universes
```

Individual commands, equivalent to the Makefile:

```bash
python3 audit/a1_certificate.py paper/main.tex audit/outputs/a1_certificate_output.txt .F0.pkl
python3 audit/a2_model_validation.py .F0.pkl > audit/outputs/a2_model_validation_output.txt
cc -O2 audit/a3_house_census.c -o .a3_house_census
./.a3_house_census 4 > audit/outputs/a3_house_census_k4.txt     # also 5; 6 for the cross-check
python3 audit/a4_identities.py > audit/outputs/a4_identities_output.txt
cc -O2 audit/a5_prism_census.c -o .a5_prism_census
./.a5_prism_census 3 > audit/outputs/a5_prism_k3.txt           # complete: every colour universe
./.a5_prism_census 4 10 > audit/outputs/a5_prism_k4_U10.txt    # second argument = maximum number of colours
python3 audit/a6_validate.py > audit/outputs/a6_validate_output.txt
```

`a1_certificate.py` parses the 71-row appendix table directly from `paper/main.tex`. `audit/outputs/repository_reruns/` holds the reruns of the repository's own `checks/` programs, each byte-identical to the corresponding file in `outputs/`.
