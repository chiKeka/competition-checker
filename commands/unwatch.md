---
description: Stop a T&C watch before its deadline. Applies the watch's retention policy.
argument-hint: <competition-slug>
---

Stop the watch identified by:

$ARGUMENTS

Steps:

1. Load `./competition-reports/watches/watches.json`.
2. Find the active watch whose `slug` matches the argument. If not found, list all active watches and ask the user to pick one.
3. Confirm with the user: *"Stop watching {{NAME}}? Retention policy is {{POLICY}}."*
4. On confirmation:
   - Unregister the scheduled job (via the `schedule` skill, or remove the crontab entry).
   - Set the watch's `status` to `stopped` and set `stopped_at` to today's ISO date.
   - Apply the retention policy exactly as if the watch had expired (see WATCH.md).
5. Report what was stopped and what, if anything, was deleted.

Do not delete any stored scorecards, sidecars, or PDFs unless the user's retention config explicitly opted into file deletion. The watch record and the historical reports are distinct — removing a watch does not by default remove the research the founder has gathered.
