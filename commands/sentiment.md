---
description: Scan online community sentiment about a recurring startup competition. Themes with sources, no score.
argument-hint: <competition-name-or-url>
---

Run only the community signal scan (no T&C analysis) for:

$ARGUMENTS

Follow `skills/competition-checker/COMMUNITY.md` exactly.

If the input is a URL, first determine the competition name from the page, then proceed. If the competition appears first-run (no prior editions detectable), stop and tell the user — do not run a sentiment scan on a first-run competition.

Save outputs:
- `./competition-reports/<slug>-sentiment-<YYYY-MM-DD>.md`
- `./competition-reports/<slug>-sentiment-<YYYY-MM-DD>.pdf` (via `scripts/generate_pdf.py`)

Report file paths only. Do not summarize the findings.

Neutrality rules apply: no sentiment score, no characterization of organizer intent, no "apply / don't apply" implication.
