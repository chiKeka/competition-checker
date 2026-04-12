---
description: Watch a competition's T&Cs for changes until its deadline. Supports multiple URLs per competition and auto-deprecates when the deadline passes.
argument-hint: <competition-name> [--deadline YYYY-MM-DD] [--urls url1,url2] [--interval weekly] | <url> --interval weekly
---

Set up a T&C watch. Follow `skills/competition-checker/WATCH.md` for full lifecycle rules.

Input:

$ARGUMENTS

## Primary flow (competition-centric)

If the first argument looks like a competition name (not a URL):

1. Parse `--deadline`, `--urls`, `--interval` flags. Defaults: `interval=weekly`, `urls=prompt the user`, `deadline=required` (prompt if missing).
2. Check `./competition-reports/history/` for an existing check of this competition by slug.
   - If found: offer to reuse the URL(s) from that check. Ask if there are additional T&C URLs to watch (rules PDF + FAQ page + announcements, etc.).
   - If not found: ask the user for the T&C URL(s) — accept multiple, comma-separated.
3. Present the watch config for confirmation:
   ```
   Watch config:
     Name:      {{NAME}}
     Slug:      {{SLUG}}
     URLs:      {{LIST}}
     Interval:  weekly
     Deadline:  {{DATE}}  (watch auto-expires on {{DATE+1}})
     Notifications: {{CURRENT_PRESET}}
     Retention: {{NOT_YET_SELECTED}}
   ```
4. Ask the retention question: *"When the watch expires, how long should the archived record be kept? (a) indefinitely, (b) N days, (c) delete on expiry"* — and, if (b) or (c): *"Also delete stored reports and sidecars at that time? (default: no)"*
5. If notifications preset doesn't exist yet (first-ever watch), walk through the setup:
   - stdout: on (non-toggleable)
   - desktop notifications: enable? (default: yes on macOS/Linux)
   - Slack webhook: enable? If yes, ask for webhook URL
   - Email drafts via Gmail MCP: enable? Only if Gmail MCP is connected in this environment — check for `mcp__claude_ai_Gmail__*` tools. If yes, ask which address.
   Save to `./competition-reports/watches/notifications.json` as the `default` preset.
6. On final confirmation:
   - Create `./competition-reports/watches/` if needed
   - Append the watch record to `watches.json` (see WATCH.md schema)
   - Register the recurring run with the `schedule` skill if available. Fall back to writing a crontab entry. If neither works, tell the user the record exists but scheduling is manual.
   - Immediately run an initial `/check` to establish the baseline sidecar; store its path in `last_sidecar_path`.
7. Tell the user the watch is active, next scheduled run date, and how to stop it (`/unwatch <slug>`).

## URL-only flow

If the first argument is a URL:

1. Parse `--interval` (default weekly). No deadline. No auto-deprecation.
2. Attempt to derive a name from the page title; confirm with the user.
3. Same confirmation → notification setup → registration flow as above, minus the deadline.
4. Watch runs until `/unwatch` is invoked.

## Guardrails

- Do not schedule anything without explicit user confirmation.
- Do not silently overwrite an existing watch for the same slug — if one exists, ask whether to replace, update, or cancel.
- Never enable a notification channel the user hasn't opted into.
- If the user hasn't configured notifications and skips the setup, fall back to `stdout` only.
