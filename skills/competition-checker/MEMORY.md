# Memory model

This plugin has six memory layers with distinct storage, TTLs, and load rules. The discipline that keeps the system fast and cheap is: **load only what the current step needs** and **use fingerprints to short-circuit expensive comparisons**.

Future-Claude: read this before doing anything that touches prior state. Don't load "for context" what the step doesn't require.

## Layers

| # | Layer | Storage | Purpose | Lifetime |
|---|---|---|---|---|
| 1 | Working | Claude conversation context | Current run's reasoning and partial results | Session only |
| 2 | Reports | `./competition-reports/<slug>-<date>.{md,pdf}` | Human-facing scorecard + styled PDF | Until user prunes |
| 3 | Sidecars | `./competition-reports/history/<slug>-<date>.json` | Machine-readable structured output, the substrate for diff | Until user prunes |
| 4 | Watches | `./competition-reports/watches/watches.json` | Index of active / paused / archived watches; points to sidecars by path | Until `/unwatch` or expiry retention |
| 5 | Prefs | `./competition-reports/watches/notifications.json` | Notification channel presets shared across watches | Persistent, user-owned |
| 6 | Fetch cache | `./competition-reports/cache/<sha256-of-url>.json` | Response-body cache keyed by URL hash; avoids re-fetching within TTL | 24h (T&C pages), 7 days (community sources) |
| 7 | User-level | `~/.claude/projects/.../memory/` (managed by Claude Code harness) | Cross-session user signal ("cares about IP dimension", "EU jurisdictions only") | Harness-managed |

Layers 2–6 live under the user's working directory and are local-only. Layer 7 is Claude Code's auto-memory and is managed by the harness — this plugin only *reads* it and *writes user-level signal* to it. It does **not** write per-check artifacts there.

## Load rules per operation

### `/check <input>`
- Load: `SKILL.md`, `RUBRIC.md`, `OUTPUT.md`, current input (fetched content), the **single most recent** sidecar for the same slug if one exists.
- Do not load: any older sidecar, any other competition's sidecar, the full watches registry (not needed for a one-off check).
- Load `COMMUNITY.md` and run the community scan only when recurring-competition cues are detected.
- Load `FETCH.md` only when the first fetch attempt fails.

### `/diff <slug>`
- Load: the two most recent sidecars for the slug. Ignore everything older.
- Do not load: other competitions' data, report markdown files (diff is computed from JSON).

### `/sentiment <name>`
- Load: `SKILL.md`, `COMMUNITY.md`, cached community sources for the slug (layer 6) if fresh. Otherwise search and fetch.
- Do not load: any T&C sidecar. Sentiment runs independently of the legal-surface review.

### Watch tick (scheduled run for slug X)
- Load: the watch record for slug X from `watches.json`, the single most recent sidecar for slug X.
- Fetch the current content for each watched URL (layer 6 cache respected; force fresh if `--fresh` was passed to the schedule or if the user configured no caching for this watch).
- Compute `source_fingerprint` on the newly fetched content.
- **Fast path**: if the new `source_fingerprint` matches the last sidecar's `source_fingerprint` for the same URL set, skip the full clause analysis entirely. Update `last_checked` on the watch record and return. No notification.
- **Slow path**: on fingerprint mismatch, run the full `/check` workflow, produce a new sidecar, compute the structured diff against the prior sidecar, send notifications only if the diff is material (per `WATCH.md`).

### `/watches`, `/list`
- Load: the top-level index file only (`watches.json` or a directory listing). Do not open any individual sidecar or report.

### `/prune <slug> --keep N`
- Load: list of sidecar filenames for the slug (directory listing, no parsing). Sort by date. Show the user what would be deleted. Delete only on confirmation.

## Fingerprints

Every sidecar carries two hashes:

- `source_fingerprint` — SHA-256 of the **normalized** T&C source text. Normalization: lowercase, whitespace collapsed to single spaces, page markers and bare page numbers stripped, trimmed. Computed per URL and as a combined hash over all URLs for multi-URL competitions.
- `sidecar_fingerprint` — SHA-256 of the canonicalized (sorted-keys, compact-separators) structured JSON output, excluding the fingerprint fields themselves.

Both are computed by `scripts/fingerprint.py` for determinism. Never compute hashes ad-hoc in prompt — always call the script.

Purpose:
- `source_fingerprint` is the watch-tick fast path. Matching → no change → skip clause analysis entirely.
- `sidecar_fingerprint` is an integrity check. When diffing, assert the stored sidecar's fingerprint matches its content before trusting it.

## Fetch cache

Responses are cached under `./competition-reports/cache/<sha256-of-url>.json` with this shape:

```json
{
  "url": "https://example.com/terms",
  "fetched_at": "2026-04-12T10:30:00Z",
  "content_type": "application/pdf",
  "content": "...",
  "source_fingerprint": "sha256-hex",
  "via": "webfetch | browser-automation"
}
```

TTLs:
- **T&C fetches** (for `/check` and watch ticks): 24 hours. Competition sites don't update daily; a 24h cache avoids hammering during back-to-back runs.
- **Community sources** (for `/sentiment` and recurring-comp community scans): 7 days. Reddit threads and blog posts rarely change within a week.
- **Manual override**: any command accepting `--fresh` forces a live fetch and overwrites the cache entry. Watches can opt out of caching at setup if the user wants every tick to be live.

Cache invalidation is lazy — entries older than TTL are ignored on read and overwritten on next live fetch. A background cleanup is out of scope for v0.1; the directory is small and user-prunable.

## Pruning

Sidecars accumulate forever by default. Small files, so no urgency. Optional via `/prune <slug> --keep N` (default N=10). The `/prune` command:

- Lists all sidecars + reports + PDFs for the slug, sorted newest-first
- Shows which would be deleted (oldest, beyond the keep count)
- Asks confirmation
- Deletes only after confirmation

Never prune sidecars that are referenced by an active watch's `last_sidecar_path`. Skip those and report to the user.

## Boundary with Claude Code auto-memory (layer 7)

The Claude Code harness maintains an auto-memory system at `~/.claude/projects/.../memory/` (the path is resolved by the harness from the current working directory). This plugin interacts with it under strict rules.

**Write to auto-memory only when you learn user-level signal.** Examples of appropriate writes:
- The user consistently asks about IP or jurisdiction dimensions → save as a user memory ("pays close attention to IP assignment clauses and governing-law provisions")
- The user only applies to competitions in a specific jurisdiction → save as a user memory ("applies only to EU/UK-domiciled competitions")
- The user corrects the skill's framing in a way that should persist → save as a feedback memory with the rule + why
- The user provides a durable preference about report verbosity, notification cadence, or retention defaults → save as a feedback memory

**Never write to auto-memory:**
- Per-check report content or summaries
- Individual competition names or scores (those belong in `./competition-reports/`)
- Watch state (that's `watches.json`)
- T&C clause text of any kind
- Community scan findings
- Anything with a short half-life (e.g., "currently applying to X this week")

**Read auto-memory when:**
- Starting a new `/check` or `/sentiment` run, to know which dimensions to surface more prominently in the "Findings" ordering (user-level signal tailors *presentation*, never *score*)
- The user references something they told you in a past session

**Hard rule:** user-level memory may influence which findings are surfaced first or flagged in the Notes section, but must **never** change a dimension's score. The rubric is objective; user attention is subjective. Keep the two separate.

## Invariants

These must always hold:

1. A sidecar's `sidecar_fingerprint` equals SHA-256 of its canonicalized content (excluding the fingerprint fields). If a sidecar fails this check, treat it as corrupt and flag to the user.
2. A watch's `last_sidecar_path` points to a file that exists and parses as valid JSON. On fail, the watch is marked `needs_attention` and the next scheduled tick re-establishes a baseline.
3. Cached fetch entries older than TTL are never treated as authoritative. The skill recomputes and overwrites.
4. Nothing outside this layer list is allowed to persist state for the plugin. If a new feature needs storage, it must be added here first.
