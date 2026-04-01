#!/usr/bin/env python3
"""Generate a nicely formatted PDF from a markdown investment memo.

Usage:
    python scripts/generate_pdf.py <memo.md> [--output path/to/output.pdf]

If --output is not specified, derives the PDF name from the source markdown
following the convention: YYYY MM DD CompanyName Investment Case.pdf

Style: Clean Notion-like formatting with proper headings, tables, and spacing.

Requires (one of):
    pip install markdown reportlab          (lightweight, always works)
    pip install markdown xhtml2pdf          (richer HTML/CSS rendering)

The script tries xhtml2pdf first, then falls back to reportlab.
"""

import sys
import os
import io
import argparse
import re
import html as html_module

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# --- Dependency checks ---
try:
    import markdown
except ImportError:
    print("ERROR: markdown not installed. Run: pip install markdown", file=sys.stderr)
    sys.exit(1)

XHTML2PDF_AVAILABLE = False
try:
    from xhtml2pdf import pisa
    XHTML2PDF_AVAILABLE = True
except ImportError:
    pass

REPORTLAB_AVAILABLE = False
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
    )
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib import colors
    from reportlab.lib.units import cm
    REPORTLAB_AVAILABLE = True
except ImportError:
    pass

if not XHTML2PDF_AVAILABLE and not REPORTLAB_AVAILABLE:
    print("ERROR: No PDF backend available.", file=sys.stderr)
    print("  Install one of:", file=sys.stderr)
    print("    pip install markdown reportlab          (lightweight)", file=sys.stderr)
    print("    pip install markdown xhtml2pdf          (richer rendering)", file=sys.stderr)
    sys.exit(1)


# ============================================================
# Backend 1: xhtml2pdf (preferred — richer CSS support)
# ============================================================

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

.status-neutral { color: #d9730d; font-weight: 600; }
.status-buy { color: #0f7b0f; font-weight: 600; }
.status-pass { color: #e03e3e; font-weight: 600; }

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

td:first-child {
    font-weight: 500;
}
"""


def enhance_html(html: str) -> str:
    """Post-process HTML to add Notion-like enhancements."""
    h1_match = re.search(r'<h1>(.*?)</h1>', html)
    if h1_match:
        after_h1 = html[h1_match.end():]
        meta_lines = []
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
            end_pos = h1_match.end() + pos
            html = html[:h1_match.start()] + header_html + html[end_pos:]

    return html


def convert_xhtml2pdf(md_path: str, pdf_path: str) -> bool:
    """Convert using xhtml2pdf (richer CSS rendering)."""
    with open(md_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    html_body = markdown.markdown(
        md_content,
        extensions=["tables", "fenced_code", "nl2br", "sane_lists"],
        output_format="html5"
    )
    html_body = enhance_html(html_body)

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

    with open(pdf_path, "wb") as pdf_file:
        status = pisa.CreatePDF(
            io.BytesIO(html_doc.encode("utf-8")),
            dest=pdf_file,
            encoding="utf-8"
        )

    if status.err:
        print(f"ERROR: xhtml2pdf had {status.err} errors", file=sys.stderr)
        return False

    file_size = os.path.getsize(pdf_path)
    print(f"PDF generated (xhtml2pdf): {pdf_path} ({file_size / 1024:.0f} KB)", file=sys.stderr)
    return True


# ============================================================
# Backend 2: reportlab (lightweight fallback — no native deps)
# ============================================================

def _rl_make_para(text, styles, style_name='Body'):
    """Create a reportlab Paragraph with basic markdown formatting."""
    text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
    try:
        return Paragraph(text, styles[style_name])
    except Exception:
        return Paragraph(text.encode('ascii', 'replace').decode(), styles[style_name])


def _rl_parse_table(lines, styles):
    """Parse markdown table lines into a reportlab Table."""
    rows = []
    for i, line in enumerate(lines):
        cells = [c.strip() for c in line.strip('|').split('|')]
        if i == 1 and all(set(c.strip()) <= set('-: ') for c in cells):
            continue
        row = []
        style_name = 'TableHeader' if i == 0 else 'TableCell'
        for cell in cells:
            cell_clean = cell.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            cell_clean = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', cell_clean)
            cell_clean = re.sub(r'\*(.+?)\*', r'<i>\1</i>', cell_clean)
            try:
                row.append(Paragraph(cell_clean, styles[style_name]))
            except Exception:
                row.append(Paragraph(cell_clean.encode('ascii', 'replace').decode(), styles[style_name]))
        rows.append(row)

    if not rows:
        return None

    max_cols = max(len(r) for r in rows)
    for r in rows:
        while len(r) < max_cols:
            r.append(Paragraph('', styles['TableCell']))

    col_width = (A4[0] - 4 * cm) / max_cols
    t = Table(rows, colWidths=[col_width] * max_cols, repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f7f6f3')),
        ('FONTSIZE', (0, 0), (-1, -1), 7.5),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e0e0e0')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))
    return t


def convert_reportlab(md_path: str, pdf_path: str) -> bool:
    """Convert using reportlab (lightweight, no native dependencies)."""
    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        leftMargin=2 * cm, rightMargin=2 * cm,
        topMargin=2 * cm, bottomMargin=2 * cm
    )

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle('MemoTitle', parent=styles['Title'], fontSize=20, spaceAfter=6,
                              textColor=colors.HexColor('#37352f')))
    styles.add(ParagraphStyle('MemoMeta', parent=styles['Normal'], fontSize=9,
                              textColor=colors.HexColor('#6b6b6b'), spaceAfter=2))
    styles.add(ParagraphStyle('H2', parent=styles['Heading2'], fontSize=14, spaceBefore=16,
                              spaceAfter=6, textColor=colors.HexColor('#37352f')))
    styles.add(ParagraphStyle('H3', parent=styles['Heading3'], fontSize=11, spaceBefore=10,
                              spaceAfter=4, textColor=colors.HexColor('#37352f')))
    styles.add(ParagraphStyle('Body', parent=styles['Normal'], fontSize=9, leading=13,
                              spaceAfter=4, textColor=colors.HexColor('#37352f')))
    styles.add(ParagraphStyle('BulletItem', parent=styles['Normal'], fontSize=9, leading=13,
                              leftIndent=18, bulletIndent=6, spaceAfter=2,
                              textColor=colors.HexColor('#37352f')))
    styles.add(ParagraphStyle('TableCell', parent=styles['Normal'], fontSize=7.5, leading=10,
                              textColor=colors.HexColor('#37352f')))
    styles.add(ParagraphStyle('TableHeader', parent=styles['Normal'], fontSize=7.5, leading=10,
                              textColor=colors.HexColor('#37352f'), fontName='Helvetica-Bold'))
    styles.add(ParagraphStyle('Source', parent=styles['Normal'], fontSize=7.5, leading=10,
                              textColor=colors.HexColor('#6b6b6b'), leftIndent=6))

    story = []
    lines = md_text.split('\n')
    i = 0
    table_lines = []
    in_table = False

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Horizontal rule
        if stripped == '---':
            if in_table and table_lines:
                t = _rl_parse_table(table_lines, styles)
                if t:
                    story.append(t)
                story.append(Spacer(1, 6))
                table_lines = []
                in_table = False
            story.append(HRFlowable(width="100%", thickness=0.5,
                                    color=colors.HexColor('#e0e0e0'),
                                    spaceBefore=6, spaceAfter=6))
            i += 1
            continue

        # Table rows
        if stripped.startswith('|') and '|' in stripped[1:]:
            if not in_table:
                in_table = True
                table_lines = []
            table_lines.append(stripped)
            i += 1
            continue
        elif in_table:
            t = _rl_parse_table(table_lines, styles)
            if t:
                story.append(t)
            story.append(Spacer(1, 6))
            table_lines = []
            in_table = False

        # H1
        if stripped.startswith('# ') and not stripped.startswith('## '):
            story.append(_rl_make_para(stripped[2:], styles, 'MemoTitle'))
            i += 1
            continue

        # H2
        if stripped.startswith('## ') and not stripped.startswith('### '):
            story.append(_rl_make_para(stripped[3:], styles, 'H2'))
            i += 1
            continue

        # H3
        if stripped.startswith('### '):
            story.append(_rl_make_para(stripped[4:], styles, 'H3'))
            i += 1
            continue

        # Bullet list
        if stripped.startswith('- ') or stripped.startswith('* '):
            text = stripped[2:]
            story.append(_rl_make_para('\u2022 ' + text, styles, 'BulletItem'))
            i += 1
            continue

        # Numbered list
        m = re.match(r'^(\d+)\.\s+(.*)', stripped)
        if m:
            story.append(_rl_make_para(m.group(1) + '. ' + m.group(2), styles, 'BulletItem'))
            i += 1
            continue

        # Checkbox
        if stripped.startswith('- [ ] ') or stripped.startswith('- [x] '):
            text = stripped[6:]
            prefix = '\u2610 ' if '[ ]' in stripped[:6] else '\u2611 '
            story.append(_rl_make_para(prefix + text, styles, 'BulletItem'))
            i += 1
            continue

        # Source lines
        if stripped.startswith('Source:') or stripped.startswith('- Source:'):
            text = stripped.lstrip('- ')
            text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
            story.append(_rl_make_para(text, styles, 'Source'))
            i += 1
            continue

        # Empty line
        if stripped == '':
            story.append(Spacer(1, 4))
            i += 1
            continue

        # Regular paragraph
        story.append(_rl_make_para(stripped, styles, 'Body'))
        i += 1

    # Flush remaining table
    if in_table and table_lines:
        t = _rl_parse_table(table_lines, styles)
        if t:
            story.append(t)

    doc.build(story)
    file_size = os.path.getsize(pdf_path)
    print(f"PDF generated (reportlab): {pdf_path} ({file_size / 1024:.0f} KB)", file=sys.stderr)
    return True


# ============================================================
# Main
# ============================================================

def convert_md_to_pdf(md_path: str, pdf_path: str) -> bool:
    """Convert markdown to PDF, trying xhtml2pdf first, then reportlab."""
    if XHTML2PDF_AVAILABLE:
        try:
            return convert_xhtml2pdf(md_path, pdf_path)
        except Exception as e:
            print(f"WARNING: xhtml2pdf failed ({e}), falling back to reportlab", file=sys.stderr)

    if REPORTLAB_AVAILABLE:
        return convert_reportlab(md_path, pdf_path)

    print("ERROR: No PDF backend available.", file=sys.stderr)
    return False


def main():
    parser = argparse.ArgumentParser(description="Generate PDF from markdown memo")
    parser.add_argument("memo_file", help="Path to markdown memo file")
    parser.add_argument("--output", "-o", help="Output PDF path")
    parser.add_argument("--company", "-c", help="Company name for default filename")
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
            basename = os.path.splitext(os.path.basename(args.memo_file))[0]
            company = re.sub(r'[-_]Analysis[-_]\d{4}[-_]\d{2}[-_]\d{2}', '', basename)
            company = company.replace('-', ' ').replace('_', ' ').strip()
        pdf_path = os.path.join(
            os.path.dirname(args.memo_file) or ".",
            f"{date_str} {company} Investment Case.pdf"
        )

    os.makedirs(os.path.dirname(pdf_path) or ".", exist_ok=True)

    print(f"Converting {args.memo_file} -> {pdf_path}", file=sys.stderr)
    success = convert_md_to_pdf(args.memo_file, pdf_path)

    if success:
        print(pdf_path)  # Print path to stdout for piping
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
