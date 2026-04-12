# Fetch strategy

Many competition sites block AI user agents — Cloudflare challenges, JavaScript walls, 403s on missing browser headers, cookie gates. This file describes the fallback chain the skill uses so it can reach real T&C content without fabricating when the standard fetch fails.

## Chain

Try in order. Move to the next step only when the current one fails per the triggers below.

1. **WebFetch** — Claude Code's built-in HTTP fetch. Fast, cheap, no browser overhead. Works for most static T&C pages and public PDFs.

2. **Browser automation** — if WebFetch trips a fail trigger, use whichever browser skill is available in the user's environment:
   - `browse` (gstack) — headless Chromium with anti-bot stealth
   - `gstack` — fast headless browser
   - `open-gstack-browser` — visible Chromium window (useful when the founder wants to watch)
   - Anthropic Computer Use API — if the user has it wired up
   These render JavaScript, carry realistic headers, and handle Cloudflare challenges that block plain HTTP clients.

3. **Vision-scroll extraction** — when browser automation loads the page visually but DOM text is inaccessible (empty `innerText`, sandboxed iframe, cross-origin embed), extract content from what is rendered on screen:
   - Screenshot the current viewport.
   - Scroll one viewport height (click inside content area first if scrolling doesn't propagate, try Tab → Space/PageDown for sandboxed frames).
   - Screenshot again. Repeat until content stops changing or the page footer is reached.
   - Use vision to extract text from the collected screenshots.
   - Concatenate the extracted text in scroll order, deduplicating overlapping sections.
   This produces lower-fidelity text (no section numbers, possible OCR drift). Mark all findings with `coverage_partial: true` and note the extraction method in `fetch_notes`.

4. **Web-search corroboration** — run in parallel with steps 2–3 whenever the primary source is access-restricted. Search the web for third-party reporting (news articles, blog posts) that quote the competition's T&Cs verbatim. Extract only direct quotes with attribution. Mark all findings with `"source_type": "secondary"` and cite as `[T&C, §X, via <source-name>]`. This path supplements but does not replace the primary fetch — if step 1, 2, or 3 succeeds, primary-source quotes take priority.

5. **User-assisted** — if no other step reaches the T&Cs, stop and ask the user to either:
   - Paste the T&C text directly into chat, or
   - Save the page as PDF (Chrome / Safari → File → Export as PDF) and pass the path.

## What counts as "fetch failed"

Any of:
- HTTP **401**, **403**, **429**, **503**
- Response body contains phrases like `"Just a moment"`, `"Checking your browser"`, `"Please enable JavaScript"`, `"Access Denied"`, `"Attention Required"`, or includes a Cloudflare ray-ID banner
- Response body is empty or under ~500 characters for a page that should contain substantial T&C text
- The returned content is obviously a login wall, signup wall, cookie consent page, or error page — not the T&Cs themselves
- The returned content is a landing page that clearly links to a T&C PDF but the PDF itself was not fetched
- **DOM text empty despite visible content** — `document.body.innerText` returns empty or only boilerplate (Cloudflare script, navigation text) while the viewport screenshot shows substantial rendered content. This indicates a sandboxed iframe or cross-origin embed — proceed to step 3 (vision-scroll extraction)

## Execution rules

- Try the next step silently — don't narrate each intermediate failure to the user. One concise note at the end is enough if fallbacks were used (e.g., *"T&Cs fetched via browser automation after WebFetch was blocked."*)
- If the final step also fails, surface all failed steps and suggest the user-assisted options.
- **Iframe/SPA handling**: when the page loads inside a sandboxed embed (e.g., Perplexity Computer, Notion embed, Webflow app): try navigating to the iframe's `src` URL directly. Try appending `#terms` or `#tc` fragment to trigger in-page anchor navigation. Try focusing into the content area with Tab, then scrolling with Space or PageDown. If none of these expose the DOM text, fall through to vision-scroll extraction.
- **Never fabricate content.** If no step in the chain reaches real T&C text, the skill halts and reports which steps were tried. Partial or suspicious content is acceptable for analysis only if the skill clearly marks coverage as partial in the report's Notes section.

## Fetch cache

Every successful fetch is cached at `./competition-reports/cache/<sha256-of-url>.json` with this shape:

```json
{
  "url": "https://example.com/terms",
  "fetched_at": "ISO 8601 datetime",
  "content_type": "text/html | application/pdf | ...",
  "content": "fetched text or base64 for binary",
  "source_fingerprint": "sha256-hex of normalized text",
  "via": "webfetch | browser-automation | vision-extraction | web-search-secondary"
}
```

**TTL for T&C fetches: 24 hours.** On any fetch request, first check the cache; if an entry exists and `fetched_at` is within TTL, return it. Otherwise refetch and overwrite.

**Respect `--fresh` flags.** Any caller passing `--fresh` (or a watch configured without caching) forces a live fetch.

**Computing the cache key**: SHA-256 of the full URL string including query params. Do not strip query params; they often affect content (e.g., `?v=2`, `?lang=en`).

**Invalidation on error**: if a fetch returns an obvious error page (per the fail triggers above), do not cache it. The cache should only hold verified good content.

Cache pruning is out of scope for v0.1 — the directory is small and user-prunable. Community-source caches (per `COMMUNITY.md`) use the same convention with a 7-day TTL.

## Computer-use scope

Browser automation accesses sites the same way the founder would if they opened the link themselves. It does **not**:
- Bypass authentication the user lacks credentials for
- Evade paywalls
- Scrape content behind TOS-protected login flows without user involvement

Its purpose is solely to work around bot-detection heuristics that block legitimate review tooling. When login is required, the skill stops and asks the user.
