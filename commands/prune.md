---
description: Remove older stored reports for a competition, keeping the N most recent. Never deletes sidecars referenced by active watches.
argument-hint: <competition-slug> [--keep N] [--also-pdfs]
---

Prune old stored reports for the slug:

$ARGUMENTS

Steps:

1. Parse `--keep N` (default: 10) and optional `--also-pdfs` flag.
2. Look up all stored artifacts for the slug in `./competition-reports/`:
   - Markdown reports matching `<slug>-<date>.md`
   - JSON sidecars matching `history/<slug>-<date>.json`
   - PDFs matching `<slug>-<date>.pdf`
   - Diff reports matching `<slug>-diff-*.md`
   - Sentiment reports matching `<slug>-sentiment-*.{md,pdf}`
3. Sort all groups newest-first by the date in the filename.
4. For each group, identify which files fall outside the keep window (beyond position N).
5. **Safety check**: load `./competition-reports/watches/watches.json` and find any active / paused watch for this slug. If its `last_sidecar_path` is in the to-delete set, remove that sidecar (and its matching report + PDF) from the delete list and tell the user which files were spared.
6. Present the plan to the user:
   ```
   Pruning {{SLUG}} — keeping {{N}} most recent of each type.

   Will DELETE:
     {{COUNT}} markdown reports (oldest: {{DATE}}, newest of deleted: {{DATE}})
     {{COUNT}} JSON sidecars
     {{COUNT}} PDFs                         [skipped unless --also-pdfs]
     {{COUNT}} diff reports
     {{COUNT}} sentiment reports

   Will KEEP:
     {{COUNT}} most recent of each type
     {{N}} sidecar(s) referenced by active watches  [if any]

   Total space freed: ~{{BYTES_HUMAN}}
   ```
7. Ask for explicit confirmation (`yes` / `no`). Do not accept implicit confirmation.
8. On confirmation, delete. On anything else, abort.
9. Report what was removed and what was spared.

## Guardrails

- Never delete `notifications.json`, `watches.json`, or anything in `./competition-reports/cache/` — those aren't reports.
- Never delete PDFs by default. Founders may have shared the PDF with cofounders or advisors. Require `--also-pdfs` to include them.
- Never delete across competitions. One slug per prune run.
- Refuse if `--keep 0` is passed. Keep at least 1 to preserve diff capability. Suggest `/unwatch` + manual deletion if the user really wants to remove all history.
