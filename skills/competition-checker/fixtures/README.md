# Fixtures

Annotated real-world T&Cs used to calibrate the rubric. Each fixture is a markdown file with:

1. The source (URL, retrieval date)
2. The raw T&C text (or a representative excerpt)
3. The expected scorecard — per dimension, what the skill *should* flag, with verbatim quotes and locations
4. A short note on why this competition is useful for calibration (what clauses are unusual or typical)

Fixtures serve three purposes:
- **Calibration reference** — when the skill sees a new T&C, it can compare clause patterns against annotated ones
- **Regression check** — re-running the skill on fixtures should produce outputs close to the annotations
- **Community contribution surface** — founders who get tripped up by a specific clause can add the competition as a fixture

## Contributing a fixture

1. Save the raw T&Cs as `<competition-slug>.md` in this folder
2. Retrieve the text yourself (don't paraphrase); include a `source` line with URL + date
3. Annotate the expected scorecard at the bottom under `## Expected scorecard`
4. Include your reasoning in a `## Notes` section — especially if a clause is genuinely ambiguous

Fixtures should be chosen to span the friction spectrum — include founder-friendly comps as well as ones with heavy clauses, so the rubric doesn't skew toward always-flagging-something.
