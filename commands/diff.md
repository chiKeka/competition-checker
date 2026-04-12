---
description: Compare the two most recent checks of a given competition. Surfaces what changed in the T&Cs between versions.
argument-hint: <competition-slug>
---

Produce a standalone diff report between the two most recent checks of the competition identified by:

$ARGUMENTS

Steps:
1. Look in `./competition-reports/history/` for JSON sidecars matching `<slug>-*.json`.
2. If fewer than two exist, tell the user and stop. Do not fabricate a diff.
3. Load the two most recent sidecars by date.
4. Produce a diff report with these sections (use the same markdown formatting as `OUTPUT.md`):
   - Header: competition name, compared dates, two source references
   - **Score changes**: dimensions whose score changed, old → new
   - **New clauses**: verbatim text + location for clauses that appeared
   - **Removed clauses**: verbatim text + location for clauses that disappeared
   - **Reworded clauses**: old verbatim → new verbatim with both locations
5. Save as `./competition-reports/<slug>-diff-<old-date>-to-<new-date>.md`.
6. Generate a PDF via `scripts/generate_pdf.py`.
7. **Render the full diff report directly in chat.** After the report, add a footer with saved file paths.

Neutrality rules apply: describe changes structurally, do not characterize whether a change is good or bad for the founder.
