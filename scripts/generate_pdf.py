#!/usr/bin/env python3
"""Generate a nicely formatted PDF from a markdown investment memo.

Usage:
    python scripts/generate_pdf.py <memo.md> [--output path/to/output.pdf]

If --output is not specified, derives the PDF name from the source markdown
following the convention: YYYY MM DD CompanyName Investment Case.pdf

Style: Clean Notion-like formatting with proper headings, tables, and spacing.

Requires: pip install markdown xhtml2pdf
"""

import sys
import os
import io
import argparse
import re

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

try:
    import markdown
except ImportError:
    print("ERROR: markdown not installed. Run: pip install markdown", file=sys.stderr)
    sys.exit(1)

try:
    from xhtml2pdf import pisa
except ImportError:
    print("ERROR: xhtml2pdf not installed. Run: pip install xhtml2pdf", file=sys.stderr)
    sys.exit(1)


# Notion-inspired CSS
NOTION_CSS = """
@page {
    size: A4;
    margin: 2cm 2.5cm 2.5cm 2.5cm;
}

body {
    font-family: -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif;
    font-size: 10pt;
    line-height: 1.6;
    color: #37352f;
    max-width: 100%;
}

h1 {
    font-size: 22pt;
    font-weight: 700;
    color: #37352f;
    margin-top: 24pt;
    margin-bottom: 8pt;
    padding-bottom: 4pt;
    border-bottom: 1px solid #e0e0e0;
}

h2 {
    font-size: 16pt;
    font-weight: 600;
    color: #37352f;
    margin-top: 20pt;
    margin-bottom: 6pt;
}

h3 {
    font-size: 12pt;
    font-weight: 600;
    color: #37352f;
    margin-top: 14pt;
    margin-bottom: 4pt;
}

h4 {
    font-size: 10pt;
    font-weight: 600;
    color: #37352f;
    margin-top: 10pt;
    margin-bottom: 4pt;
}

p {
    margin-bottom: 6pt;
    margin-top: 2pt;
}

strong {
    font-weight: 600;
    color: #37352f;
}

em {
    font-style: italic;
    color: #6b6b6b;
}

code {
    background-color: #f7f6f3;
    padding: 1pt 4pt;
    border-radius: 3pt;
    font-family: 'SFMono-Regular', 'Consolas', 'Liberation Mono', Menlo, monospace;
    font-size: 9pt;
    color: #eb5757;
}

pre {
    background-color: #f7f6f3;
    padding: 10pt;
    border-radius: 4pt;
    font-family: 'SFMono-Regular', 'Consolas', 'Liberation Mono', Menlo, monospace;
    font-size: 8.5pt;
    line-height: 1.5;
    overflow-x: auto;
    margin: 6pt 0;
}

blockquote {
    border-left: 3pt solid #e0e0e0;
    padding-left: 12pt;
    margin-left: 0;
    color: #6b6b6b;
    font-style: italic;
}

ul, ol {
    margin-top: 2pt;
    margin-bottom: 6pt;
    padding-left: 20pt;
}

li {
    margin-bottom: 2pt;
}

hr {
    border: none;
    border-top: 1px solid #e0e0e0;
    margin: 16pt 0;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin: 8pt 0;
    font-size: 8.5pt;
}

thead {
    background-color: #f7f6f3;
}

th {
    font-weight: 600;
    text-align: left;
    padding: 6pt 8pt;
    border-bottom: 2px solid #e0e0e0;
    color: #37352f;
    white-space: nowrap;
}

td {
    padding: 5pt 8pt;
    border-bottom: 1px solid #ececec;
    vertical-align: top;
}

tr:nth-child(even) {
    background-color: #fafafa;
}

/* Status badge style for conviction ratings */
.status-neutral { color: #d9730d; font-weight: 600; }
.status-buy { color: #0f7b0f; font-weight: 600; }
.status-pass { color: #e03e3e; font-weight: 600; }

/* First page title area */
.memo-header {
    text-align: center;
    padding-bottom: 12pt;
    margin-bottom: 12pt;
    border-bottom: 2px solid #37352f;
}

.memo-header h1 {
    border-bottom: none;
    margin-bottom: 4pt;
}

.memo-meta {
    font-size: 9pt;
    color: #6b6b6b;
    margin: 2pt 0;
}

/* Risk score highlighting */
td:first-child {
    font-weight: 500;
}
"""


def enhance_html(html: str) -> str:
    """Post-process HTML to add Notion-like enhancements."""
    # Wrap the first h1 + metadata lines in a header div
    # Find first h1
    h1_match = re.search(r'<h1>(.*?)</h1>', html)
    if h1_match:
        # Look for the metadata lines right after h1
        after_h1 = html[h1_match.end():]
        meta_lines = []
        # Collect paragraph lines that look like metadata (Date:, Sector:, etc.)
        meta_pattern = re.compile(r'<p><strong>(Date|Sector|Data Freshness|Conviction Rating).*?</p>')
        pos = 0
        for m in meta_pattern.finditer(after_h1):
            if m.start() == pos or after_h1[pos:m.start()].strip() == '':
                meta_lines.append(m.group())
                pos = m.end()
            else:
                break

        if meta_lines:
            header_html = f'<div class="memo-header"><h1>{h1_match.group(1)}</h1>'
            for ml in meta_lines:
                header_html += ml.replace('<p>', '<p class="memo-meta">').replace('<strong>', '').replace('</strong>', '')
            header_html += '</div>'

            # Replace in original html
            end_pos = h1_match.end() + pos
            html = html[:h1_match.start()] + header_html + html[end_pos:]

    return html


def convert_md_to_pdf(md_path: str, pdf_path: str):
    """Convert markdown file to PDF with Notion-like styling."""
    with open(md_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    # Convert markdown to HTML
    html_body = markdown.markdown(
        md_content,
        extensions=["tables", "fenced_code", "nl2br", "sane_lists"],
        output_format="html5"
    )

    # Enhance HTML
    html_body = enhance_html(html_body)

    # Build full HTML document
    html_doc = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
{NOTION_CSS}
</style>
</head>
<body>
{html_body}
</body>
</html>"""

    # Convert to PDF
    with open(pdf_path, "wb") as pdf_file:
        status = pisa.CreatePDF(
            io.BytesIO(html_doc.encode("utf-8")),
            dest=pdf_file,
            encoding="utf-8"
        )

    if status.err:
        print(f"ERROR: PDF generation had {status.err} errors", file=sys.stderr)
        return False

    file_size = os.path.getsize(pdf_path)
    print(f"PDF generated: {pdf_path} ({file_size / 1024:.0f} KB)", file=sys.stderr)
    return True


def main():
    parser = argparse.ArgumentParser(description="Generate PDF from markdown memo")
    parser.add_argument("memo_file", help="Path to markdown memo file")
    parser.add_argument("--output", "-o", help="Output PDF path (default: YYYY MM DD Company Investment Case.pdf)")
    parser.add_argument("--company", "-c", help="Company name for default filename (if not using --output)")
    args = parser.parse_args()

    if not os.path.exists(args.memo_file):
        print(f"ERROR: File not found: {args.memo_file}", file=sys.stderr)
        sys.exit(1)

    if args.output:
        pdf_path = args.output
    else:
        from datetime import date
        today = date.today()
        date_str = today.strftime("%Y %m %d")
        if args.company:
            company = args.company
        else:
            # Try to extract company name from the markdown filename
            basename = os.path.splitext(os.path.basename(args.memo_file))[0]
            # Strip common suffixes like -Analysis-YYYY-MM-DD
            company = re.sub(r'[-_]Analysis[-_]\d{4}[-_]\d{2}[-_]\d{2}', '', basename)
            company = company.replace('-', ' ').replace('_', ' ').strip()
        pdf_path = os.path.join(
            os.path.dirname(args.memo_file) or ".",
            f"{date_str} {company} Investment Case.pdf"
        )

    # Ensure output directory exists
    os.makedirs(os.path.dirname(pdf_path) or ".", exist_ok=True)

    print(f"Converting {args.memo_file} → {pdf_path}", file=sys.stderr)
    success = convert_md_to_pdf(args.memo_file, pdf_path)

    if success:
        print(pdf_path)  # Print path to stdout for piping
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
