---
description: Compare 2–5 competitions side by side. Shows structural tradeoffs across all 7 dimensions in one view.
argument-hint: <slug-a> <slug-b> [slug-c] [slug-d] [slug-e]
---

Compare the most recent checks of each competition identified by:

$ARGUMENTS

Steps:
1. Look in `./competition-reports/history/` for the most recent JSON sidecar for each slug provided. If any slug has no sidecar, tell the user and list only the valid ones.
2. If fewer than two valid slugs remain, tell the user and stop.
3. Produce a comparison report with these sections:

### Comparison matrix
A single table: 7 dimensions as rows, competitions as columns, scores in cells. Include the headline text for the highest-scoring entry in each row so the key friction is visible at a glance.

```
| Dimension              | {{COMP_A}} | {{COMP_B}} | {{COMP_C}} | Highest friction |
|------------------------|:----------:|:----------:|:----------:|------------------|
| IP & Ownership         |     7?     |     3      |     5      | {{COMP_A}}: ... |
| Equity & Financial     |     7      |     2      |     8      | {{COMP_C}}: ... |
| ...                    |    ...     |    ...     |    ...     | ...              |
```

### Structural divergences
For each dimension where scores differ by ≥2, surface the specific structural difference in neutral terms:
- "Competition A requires perpetual IP license; B's expires after 12 months; C has no IP clause."
- "A and C require equity as a condition of the prize; B does not."

Only list dimensions with meaningful divergence. Do not pad with trivial differences.

### Fit comparison (if founder profile exists)
If `./competition-reports/founder-profile.json` exists, show a fit matrix: competitions as columns, fit factors as rows, status (match/mismatch/partial) in cells.

### ROI comparison (if founder profile exists)
Side-by-side ROI factors: time commitment, financial cost, equity exposure, prize value per competition.

4. **Render the full comparison directly in chat.**
5. Save as `./competition-reports/compare-<slug-a>-vs-<slug-b>[-vs-slug-c]-<date>.md`.
6. Generate PDF via `scripts/generate_pdf.py`.
7. After the in-chat report, add a footer with saved file paths.

Neutrality rules apply: surface structural differences, never rank competitions or say which is "better." The founder decides.
