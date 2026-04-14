# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-04-14

### Added
- Initial release.
- `/check` — full T&C review producing a 7-dimension neutral scorecard with verbatim clause quotes and source references.
- `/compare` — side-by-side comparison of 2–5 competitions across all dimensions.
- `/sentiment` — community-signal scan (Reddit, HN, blogs, past-winner interviews) with source counts.
- `/diff` — surfaces material changes between two checks of the same competition.
- `/watch`, `/unwatch`, `/watches` — weekly T&C monitoring with auto-deprecation after deadline.
- `/list`, `/prune` — local report management.
- Founder profile (`PROFILE.md`) for optional Fit Analysis and ROI Factors sections.
- Omission detection — flags expected clauses absent from the T&Cs.
- Investment-term deep dive for SAFE/convertible-note prizes.
- Fetch-fallback chain (browser automation, vision-scroll, web-search corroboration) for bot-blocked sites.
- PDF report generation via WeasyPrint.
