# Watch lifecycle

Competition T&Cs change silently between editions and sometimes *within* an application window. The watch feature keeps a founder informed without requiring manual re-checks. This file defines the data model, scheduling cadence, change-detection rules, notification dispatch, and retention.

## Primary flow: competition-centric

The default `/watch` flow takes a **competition name + deadline**. The system watches the associated T&C URL(s) weekly until the day after the deadline, then auto-deprecates per the user's retention choice.

```
/watch "TechCrunch Disrupt 2026" --deadline 2026-10-15
```

If no prior `/check` exists for that competition, the skill asks the user for the T&C URL(s) before creating the watch. Multiple URLs are supported (rules page + PDF + FAQ page are a common combination).

## Fallback flow: URL-only

For cases without a fixed deadline (rolling grants, always-open programs), a URL-only form is supported:

```
/watch https://example.com/competition --interval weekly
```

No auto-deprecation; the watch runs until the user issues `/unwatch`.

## Data model

Stored at `./competition-reports/watches/watches.json`:

```json
{
  "watches": [
    {
      "slug": "techcrunch-disrupt-2026",
      "name": "TechCrunch Disrupt 2026",
      "urls": [
        "https://techcrunch.com/disrupt/rules",
        "https://techcrunch.com/disrupt/terms.pdf"
      ],
      "deadline": "2026-10-15",
      "interval": "weekly",
      "status": "active",
      "created_at": "2026-04-12",
      "last_checked": "2026-04-12",
      "last_sidecar_path": "./competition-reports/history/techcrunch-disrupt-2026-2026-04-12.json",
      "notification_config_ref": "default",
      "retention": {
        "policy": "archive_for_days",
        "days": 365
      }
    }
  ],
  "archived": []
}
```

`status` values: `active`, `paused`, `expired`, `stopped`.
`retention.policy` values: `keep_indefinitely`, `archive_for_days` (with `days`), `delete_on_expiry`.

Notification config lives separately at `./competition-reports/watches/notifications.json` so multiple watches can share a preset without duplication. A watch's `notification_config_ref` points to a named preset (default: `"default"`).

```json
{
  "presets": {
    "default": {
      "stdout": true,
      "slack": { "enabled": false, "webhook_url": null },
      "desktop": { "enabled": true },
      "email": { "enabled": false, "via": null, "address": null }
    }
  }
}
```

`email.via` values: `gmail_mcp` (use the Gmail MCP server if the user has it connected) or `smtp` (out of scope for v0.1 — document as future).

## Cadence

- **Default interval**: `weekly`, same cadence throughout the watch lifetime (no ramping near the deadline). The user asked for consistency over urgency.
- Other accepted intervals: `daily`, `fortnightly`, `monthly`, or a raw cron expression for power users.
- The first run happens immediately on watch creation (establishes the baseline).
- Subsequent runs are scheduled via the `schedule` skill if available in the user's environment, or via system cron as a fallback.
- The final run fires on the day after the deadline and marks the watch `expired`.

## Change detection

On each scheduled tick, the watch runner executes these steps:

1. **Fetch current content** for every URL in the watch record (follow `FETCH.md` chain; respect the fetch cache per `MEMORY.md` unless the watch opted out of caching).
2. **Compute `source_fingerprint`** on the combined normalized text across all URLs, using `scripts/fingerprint.py text-stdin`.
3. **Fast path**: compare the new `source_fingerprint` against the `source_fingerprint` in the sidecar at `last_sidecar_path`. **If either fingerprint is an empty string** (e.g., because the source was fetched via vision-extraction or web-search and the raw text was not available for hashing), **skip the fast path entirely** and proceed to step 4 (slow path). Otherwise, if the fingerprints match:
   - Update `last_checked` on the watch record.
   - Do **not** generate a new sidecar or report. The text is functionally identical to the last snapshot.
   - Do **not** notify.
   - Return.
4. **Slow path** (fingerprint mismatch): run the full `/check` workflow to produce a fresh sidecar + markdown + PDF.
5. **Diff** the new sidecar against the one at `last_sidecar_path`.
6. **Classify** the diff as **material** or **cosmetic**.
7. If material: dispatch notification, update `last_sidecar_path` to the new sidecar, update `last_checked`. If cosmetic only (possible when fingerprints mismatch due to page renumbering but no real clause change): do not notify, but still advance `last_sidecar_path` so the next tick compares against the latest snapshot.

### Material change — definition

Any of:
- Any of the 7 dimension scores shifts by **≥1**
- A clause is **added** (present in new sidecar, absent in old — verbatim text comparison)
- A clause is **removed** (present in old, absent in new)
- A clause's verbatim text is **reworded** (normalized-whitespace comparison to exclude layout noise)
- An unusual-clause entry is added or removed
- A new URL in the competition page starts linking to a previously unseen legal document

### Cosmetic change — definition

- Whitespace-only differences
- Re-pagination without text changes
- Header/footer boilerplate changes
- Date-stamp or "last updated" line changes without clause changes

When only cosmetic changes are detected, log one line to a silent audit trail (`./competition-reports/watches/audit.log`) but do not notify.

## Notification dispatch

On material change, Claude (or the cron runner) generates a short, neutral alert and invokes `scripts/notify.py` with the configured channels. Alert body structure:

```
Title: "[Competition Checker] {{NAME}} T&Cs changed"

Body:
  Detected {{N}} material change(s) on {{ISO_DATE}}.
  - Dimension score shifts: {{LIST}}
  - New clauses: {{COUNT}}
  - Removed clauses: {{COUNT}}
  - Reworded clauses: {{COUNT}}

  Full diff: {{PATH_TO_DIFF_MARKDOWN}}
  Full new scorecard: {{PATH_TO_SCORECARD_MARKDOWN}}

  Watch continues. Next run: {{ISO_DATE}}. Deadline: {{DEADLINE}}.
```

**Neutrality rules still apply.** Do not characterize whether changes are good or bad for the founder. Quote what changed, point to the diff, stop.

Channels invoked per notification config preset:
- `stdout` — printed to the Claude Code session, always on by default
- `slack` — POST to webhook URL via `notify.py`
- `desktop` — `osascript` (macOS) or `notify-send` (Linux) via `notify.py`
- `email` via `gmail_mcp` — Claude drafts an email using the Gmail MCP server's `gmail_create_draft` tool; the user reviews and sends. *Skill does not send autonomously — drafts only.*

## Expiry and retention

On any tick, if `today > deadline`:

1. Status flips to `expired`.
2. One final notification is sent: *"Watch for {{NAME}} expired. Deadline passed on {{DEADLINE}}."*
3. The watch is unregistered from the scheduler.
4. Retention is applied per the watch's `retention.policy`:
   - `keep_indefinitely`: move the record to `archived` array in `watches.json`, keep all sidecars and reports on disk.
   - `archive_for_days`: move to `archived` array; schedule a one-off cleanup job for `deadline + days` that deletes the record and optionally the associated sidecars (see below).
   - `delete_on_expiry`: remove the record immediately; sidecars and reports are preserved on disk unless the user also opts into file deletion.

**File deletion opt-in** — when a user chooses `archive_for_days` or `delete_on_expiry`, the `/watch` setup prompt asks a second question: *"When the watch ends, also delete stored reports and sidecars for this competition? (default: no — keep for your records.)"*

## Pause and stop

- `/watch pause <slug>` — sets status to `paused`, keeps the record and last sidecar, halts scheduled runs.
- `/watch resume <slug>` — flips back to `active`, schedules the next tick.
- `/unwatch <slug>` — sets status to `stopped`, applies the same retention policy as expiry.

## Integration points

- The scheduler is whatever is available in the user's environment:
  - **`schedule` skill** (preferred, present in most gstack-style setups)
  - **system `cron`** as a fallback — `/watch` writes a crontab entry under `~/.competition-checker/cron.d/` and asks the user to install it, or installs it itself if permission is granted
  - If neither is available, `/watch` creates the watch record but tells the user scheduling is manual and they'll need to invoke `/check` themselves on cadence. The record still drives diffing.
- The runner on each tick is Claude Code itself, invoked by the scheduler with a prompt like: `"Run the Competition Checker watch tick for slug <slug>."` Claude reads this WATCH.md, the watch record, executes the fetch → check → diff → notify flow, and updates the record.

## Non-goals (v0.1)

- Real-time / webhook-driven detection of T&C changes. Weekly polling is sufficient and avoids infrastructure overhead.
- Autonomous email sending. Gmail MCP drafts only; the founder sends.
- Bulk watch import/export. One watch at a time via `/watch`.
- Multi-user / shared-team watches. Single-user, local-first.
