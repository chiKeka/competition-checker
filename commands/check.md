---
description: Review a startup competition's T&Cs. Accepts URL, PDF path, screenshot, or pasted text. Produces markdown, JSON, and PDF.
argument-hint: <url | pdf-path | pasted-text>
---

Invoke the `competition-checker` skill on the following input:

$ARGUMENTS

Follow the skill's workflow exactly:
1. Ingest the input (URL → WebFetch, PDF → Read, image → vision, text → inline).
2. If the input is a landing page, follow links to the actual T&C document.
3. Check `./competition-reports/history/` for a prior check of the same competition; include a diff section if one exists.
4. Classify clauses across all 7 dimensions per `RUBRIC.md`.
5. Emit the scorecard exactly per `OUTPUT.md` — no extra sections, no summary.
6. Save markdown, JSON sidecar, and run `scripts/generate_pdf.py` to produce the PDF.
7. **Render the full report directly in chat** so the founder reads it immediately. After the report, add a footer with saved file paths.

Neutrality is mandatory: no prescriptive language anywhere in the output.
