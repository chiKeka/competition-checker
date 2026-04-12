---
description: List all stored competition checks and their dates.
---

Read `./competition-reports/history/` and list every stored check grouped by competition slug.

Output format:

```
## Stored competition checks

### <competition-slug>
- <date>  →  <relative markdown path>
- <date>  →  <relative markdown path>

### <another-slug>
- <date>  →  <relative markdown path>
```

Within each slug group, list newest to oldest. If `./competition-reports/history/` does not exist or is empty, say so in one sentence.

Do not open or summarize any report. This command lists only.
