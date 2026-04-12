#!/usr/bin/env python3
"""Convert a competition-checker markdown report to a styled PDF.

Usage: generate_pdf.py <input.md> <output.pdf>

Requires: pip install -r scripts/requirements.txt
macOS also needs pango/cairo: brew install pango
"""
from __future__ import annotations

import sys
from pathlib import Path

INSTALL_HINT = (
    "Missing dependency. Install with:\n"
    "  pip install -r scripts/requirements.txt\n\n"
    "System libraries required:\n"
    "  macOS:  brew install pango\n"
    "  Ubuntu: sudo apt install libpango1.0-dev libgdk-pixbuf2.0-dev libffi-dev\n"
    "  Fedora: sudo dnf install pango-devel\n"
)

try:
    import markdown
    from weasyprint import HTML, CSS
except (ImportError, OSError) as exc:
    sys.stderr.write(INSTALL_HINT)
    if str(exc):
        sys.stderr.write(f"\nUnderlying error: {exc}\n")
    sys.exit(3)


STYLESHEET = """
@page {
    size: A4;
    margin: 2cm 1.8cm 2.2cm 1.8cm;
    @bottom-left {
        content: "Competition Checker";
        font-size: 8.5pt;
        color: #888;
    }
    @bottom-right {
        content: counter(page) " / " counter(pages);
        font-size: 8.5pt;
        color: #888;
    }
}

body {
    font-family: -apple-system, "Helvetica Neue", "Segoe UI", Arial, sans-serif;
    font-size: 10.5pt;
    line-height: 1.55;
    color: #1a1a1a;
}

h1 {
    font-size: 20pt;
    margin: 0 0 0.3em 0;
    padding-bottom: 0.25em;
    border-bottom: 2px solid #1a1a1a;
    letter-spacing: -0.01em;
}

h2 {
    font-size: 13.5pt;
    margin: 1.7em 0 0.5em 0;
    color: #2a2a2a;
    border-bottom: 1px solid #e0e0e0;
    padding-bottom: 0.2em;
}

h3 {
    font-size: 11pt;
    margin: 1.2em 0 0.3em 0;
    color: #333;
}

p { margin: 0.5em 0; }

strong { color: #111; }

table {
    border-collapse: collapse;
    width: 100%;
    margin: 0.9em 0;
    font-size: 9.8pt;
}

th, td {
    border: 1px solid #d0d0d0;
    padding: 6px 9px;
    text-align: left;
    vertical-align: top;
}

th {
    background: #f4f4f4;
    font-weight: 600;
}

td:nth-child(3) {
    text-align: center;
    font-weight: 600;
}

blockquote {
    border-left: 3px solid #888;
    margin: 0.4em 0;
    padding: 0.15em 0 0.15em 0.9em;
    color: #2a2a2a;
    font-style: italic;
    font-size: 10pt;
}

ul { padding-left: 1.2em; }
li { margin: 0.45em 0; }

code {
    background: #f2f2f2;
    padding: 1px 5px;
    border-radius: 3px;
    font-family: "SF Mono", Consolas, monospace;
    font-size: 9pt;
    color: #555;
}

hr {
    border: none;
    border-top: 1px solid #e0e0e0;
    margin: 1.4em 0;
}

em {
    color: #555;
}
"""


def main() -> int:
    if len(sys.argv) != 3:
        sys.stderr.write("Usage: generate_pdf.py <input.md> <output.pdf>\n")
        return 2

    md_path = Path(sys.argv[1])
    pdf_path = Path(sys.argv[2])

    if not md_path.is_file():
        sys.stderr.write(f"Input not found: {md_path}\n")
        return 1

    md_text = md_path.read_text(encoding="utf-8")
    html_body = markdown.markdown(
        md_text,
        extensions=["tables", "fenced_code", "sane_lists"],
    )
    html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{md_path.stem}</title>
</head>
<body>
{html_body}
</body>
</html>"""

    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    HTML(string=html_doc).write_pdf(
        target=str(pdf_path),
        stylesheets=[CSS(string=STYLESHEET)],
    )
    print(str(pdf_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
