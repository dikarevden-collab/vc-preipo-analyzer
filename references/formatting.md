# Formatting Rules

Consistent across all RLC investment documents. Aligned with `legal-dd-memo` skill. **[Low freedom — follow exactly]**

## Table of Contents

- [Fonts](#fonts)
- [Header & Footer](#header--footer)
- [Page Layout](#page-layout)
- [Tables](#tables)
- [Headings](#headings)
- [Color Palette](#color-palette)
- [Flow Diagram](#flow-diagram-if-applicable)
- [Content Rules](#content-rules)
- [Markdown-Specific Rules](#markdown-specific-rules)
- [External Memo Redaction](#external-memo-redaction-if-producing-external-version)

## Fonts

| Element | Font | Size | Color |
|---------|------|------|-------|
| Body text | Gilroy Light | 10pt | Black (default) |
| Headings (H1/H2/H3) | Gilroy SemiBold | Word defaults (~14/13/12pt) | Navy `#1B2A4A` |
| Title "Investment Analysis:" | Gilroy SemiBold | 16pt | Red `#DE213E` |
| Title "{COMPANY} Investment Case" | Gilroy SemiBold | 20pt | Black |
| Date | Gilroy Light | 12pt | Gray `#5D6D7E` |
| Key deal data | Gilroy SemiBold | 16pt | Navy `#1B2A4A` |
| Table cells (key-value) | Gilroy Light | 9.5pt | Black |
| Table cells (structure/comp/risk) | Gilroy Light | 8.5–9pt | Black |
| Table headers | Gilroy Light bold | 8.5–9pt | White on navy `#1B2A4A` |
| Bullet bold prefix | Gilroy Light bold | 10pt | Black |
| Italic notes | Gilroy Light italic | 9pt | Black |

**Fallback fonts (when Gilroy unavailable):** Poppins SemiBold (headings), Poppins Regular (body) — matches Gamma RLC theme `tf15c1vstmnc6z1`. Final fallback: system sans-serif.

## Header & Footer

| Element | Font | Size | Color | Alignment |
|---------|------|------|-------|-----------|
| First-page header | Gilroy Light | 9pt | Black | Right — "Prepared by RLC AltInvest Consultants FZCO" |
| First-page footer | Empty | — | — | — |
| Regular header (confidentiality) | Gilroy Light | 8pt | Gray `#808080` | Center |
| Regular header spacing | — | — | — | 12pt space-after |
| Footer heading "Disclaimer & Risk Warnings" | Gilroy SemiBold bold | 14pt | Gray `#5D6D7E` | Left |
| Footer page number | Gilroy Light | 8pt | Gray `#5D6D7E` | Right (same line as heading, via tab stop) |
| Footer disclaimer body (3 paragraphs) | Gilroy Light italic | 8pt | Gray `#5D6D7E` | Left |
| Footer paragraph spacing | — | — | — | 4–6pt space-after |

**Confidentiality header text (regular pages):**
> CONFIDENTIAL. This document contains analytical material and does not constitute investment advice. {Company} is not affiliated with RLC AltInvest FZCO and has not approved or endorsed this material. This material is intended only for Professional Clients and must not be relied upon or acted upon by any other person.

**`different_first_page_header_footer = True`** — first page has "Prepared by" only; confidentiality + disclaimer appear on pages 2+.

## Page Layout

- **Margins:** 2.0cm top/bottom, 2.5cm left/right
- **`different_first_page_header_footer = True`**

## Tables

- **Style:** Table Grid, center-aligned
- **Header row:** White text on navy `#1B2A4A`
- **Alternating data rows:** `#F0F4F8` shading
- **Key-value tables:** Left column shaded `#F0F4F8`
- **`cantSplit` on all rows** (no row splits mid-cell)
- **`keep_with_next` on header row only** (header stays with first data row; table can break between data rows)
- Financial tables: parentheses for negatives — `(34)` not `-34`
- Use `—` for unavailable data, `N/A` for not applicable

## Headings

- `run.font.name = 'Gilroy SemiBold'` must be set explicitly on every run (Word defaults to Calibri)
- `keep_with_next = True` always (never orphan a heading)
- Section numbering: `## N. Section Title` format. Executive Summary is unnumbered. Verification Report is Section 11.

## Color Palette

| Role | Hex | Usage |
|------|-----|-------|
| Navy (headings, table headers) | `#1B2A4A` | Headings, table header backgrounds, key deal data |
| Primary accent (teal) | `#3DD9D7` | Buttons, positive indicators, "Buy" conviction, bull scenario |
| Secondary accent 1 (light blue) | `#36CAEC` | Chart fills, info callouts, secondary highlights |
| Secondary accent 2 (dark blue) | `#125488` | Gamma table headers, section dividers |
| Risk / negative (red) | `#DE213E` | Title accent, risk flags, "Pass" conviction, bear scenario, warnings |
| Body text | `#262626` | All body text |
| Gray (dates, footers, meta) | `#5D6D7E` | Dates, page numbers, footer text, secondary labels |
| Confidentiality header | `#808080` | Regular page header text |
| Table alt rows | `#F0F4F8` | Alternating row shading |
| Card / page background | `#FFFFFF` | White |
| Links | `#00B0F0` | Hyperlinks |

## Flow Diagram (if applicable)

- Must stay on one page — all elements have `keep_with_next = True`
- Arrow: `↓` character, 12pt bold, navy `#1B2A4A`, `Pt(1)` spacing before/after
- Boxes: single-cell tables, center-aligned, Gilroy Light 9pt bold, `Pt(4)` padding before/after
- Color scheme: endpoints = `#D4E6F1`, investor vehicle = `#1B2A4A`, fund layer = `#2E4057`, aggregator = `#3B5998`, SPV = `#4A6FA5`
- Dark backgrounds → white text; light backgrounds → navy `#1B2A4A` text

## Content Rules

- **Date stamping:** Every external data point must include its access date or reporting period
  - Market data: `$3.8B market cap (Yahoo Finance — April 8, 2026)`
  - Stale data (>6 months): `[STALE — as of YYYY-MM]`
  - Company-sourced claims: `(company claim, not independently verified)`
  - Projections: `(management projection)` or `(analyst estimate)`
- **Key metrics in bold:** In running text, bold all key financial figures: **$292M revenue**, **775K merchants**, **8.5x EV/Rev**
- **Disputed claims:** Flag inline with `[DISPUTED — verifier found: {correction}]`
- **Summary / exit text:** Regular body text (10pt), NOT italic footnotes
- **Performance fee:** State "crystallized and paid at exit" where applicable

## Markdown-Specific Rules

**Confidentiality header:** Every markdown memo must begin with:
```
> **CONFIDENTIAL.** This document contains analytical material and does not constitute investment advice. {Company} is not affiliated with RLC AltInvest FZCO and has not approved or endorsed this material.
```

**Section numbering:** `## N. Section Title` format. Executive Summary unnumbered. Verification Report is Section 11.

**Tables:** Markdown tables with bold header row. When generating PDF via `generate_pdf.py`, the script applies the table styling rules above (navy headers, alternating rows).

**Markdown table rule:** Every table header MUST have a non-empty first cell (e.g., "Term", "Item", "Metric"). Tables with empty first headers (`| |`) render badly in `generate_pdf.py` — column widths collapse and row labels overflow into the next column.

## External Memo Redaction (if producing external version)

- Remove ISIN, Bloomberg ticker, RCS/registration numbers
- Anonymize entity names below investor vehicle (Nevada → "US SPV Entity", etc.)
- Remove sub-Lux key people
- Fee table: use "Underlying Layer" not entity-specific names
