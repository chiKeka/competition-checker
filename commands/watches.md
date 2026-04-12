---
description: List all active, paused, and archived T&C watches.
---

Read `./competition-reports/watches/watches.json` and render:

```
## Active watches

| Slug | Name | Deadline | Next run | Last material change | URLs |
|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | N URLs |

## Paused
(same columns; omit section if empty)

## Archived
| Slug | Name | Ended | Reason | Retained until |
|---|---|---|---|---|
| ... | ... | ... | expired / stopped | ... |
```

Within each group, list newest first by `created_at` (active/paused) or `stopped_at`/`expired_at` (archived).

If `watches.json` does not exist or has no entries, say so in one sentence.

Do not open any individual scorecard. This command lists only. For the contents of stored checks, use `/list`.
