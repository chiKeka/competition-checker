#!/usr/bin/env python3
"""Deterministic fingerprinting for T&C source text and sidecar JSON.

Usage:
  fingerprint.py text <input-file>           -> SHA-256 of normalized text
  fingerprint.py text-stdin                  -> reads stdin, prints SHA-256
  fingerprint.py json <input-file>           -> SHA-256 of canonicalized JSON
  fingerprint.py sidecar <sidecar.json>      -> SHA-256 of the sidecar's JSON,
                                                 excluding fingerprint fields

Normalization rules (text):
  - strip page markers like "Page N of M"
  - strip bare page numbers on their own line
  - collapse all whitespace (including newlines) to a single space
  - lowercase
  - trim leading/trailing whitespace

Canonicalization rules (json):
  - recursive key sort
  - compact separators
  - UTF-8, no ASCII escaping

Stability note: these normalizations are chosen so minor re-paginations,
whitespace-only edits, or key-ordering changes do not produce a different
hash. Actual textual changes (new/removed/reworded clauses) always do.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

PAGE_MARKER_RE = re.compile(r"(?im)^\s*page\s+\d+\s+of\s+\d+\s*$")
BARE_PAGE_NUM_RE = re.compile(r"(?m)^\s*\d{1,4}\s*$")
WHITESPACE_RE = re.compile(r"\s+")

FINGERPRINT_FIELDS = ("source_fingerprint", "sidecar_fingerprint")


def normalize_text(raw: str) -> str:
    t = PAGE_MARKER_RE.sub(" ", raw)
    t = BARE_PAGE_NUM_RE.sub(" ", t)
    t = WHITESPACE_RE.sub(" ", t)
    return t.strip().lower()


def canonicalize_json_str(raw: str) -> str:
    obj = json.loads(raw)
    return canonicalize_obj(obj)


def canonicalize_obj(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_hex(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def fingerprint_sidecar(raw: str) -> str:
    """SHA of the sidecar excluding its own fingerprint fields."""
    obj = json.loads(raw)
    stripped = strip_fingerprint_fields(obj)
    return sha256_hex(canonicalize_obj(stripped))


def strip_fingerprint_fields(obj):
    if isinstance(obj, dict):
        return {
            k: strip_fingerprint_fields(v)
            for k, v in obj.items()
            if k not in FINGERPRINT_FIELDS
        }
    if isinstance(obj, list):
        return [strip_fingerprint_fields(x) for x in obj]
    return obj


def usage() -> int:
    sys.stderr.write(__doc__ or "")
    return 2


def main() -> int:
    args = sys.argv[1:]
    if not args:
        return usage()

    mode = args[0]

    if mode == "text-stdin":
        raw = sys.stdin.read()
        print(sha256_hex(normalize_text(raw)))
        return 0

    if len(args) != 2:
        return usage()

    path = Path(args[1])
    if not path.is_file():
        sys.stderr.write(f"Not found: {path}\n")
        return 1
    raw = path.read_text(encoding="utf-8", errors="replace")

    if mode == "text":
        print(sha256_hex(normalize_text(raw)))
        return 0
    if mode == "json":
        print(sha256_hex(canonicalize_json_str(raw)))
        return 0
    if mode == "sidecar":
        print(fingerprint_sidecar(raw))
        return 0

    return usage()


if __name__ == "__main__":
    raise SystemExit(main())
