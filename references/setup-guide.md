# Setup Guide

Quick setup for Notion integration, PDF generation, and Python dependencies.

---

## 1. Python Dependencies

The skill requires Python 3.9+ with a few pip packages. Install the **minimum set** that covers all scripts:

```bash
pip install markdown reportlab requests yfinance PyPDF2 openpyxl
```

**What each package does:**

| Package | Used by | Purpose |
|---------|---------|---------|
| `markdown` | `generate_pdf.py` | Convert markdown to HTML |
| `reportlab` | `generate_pdf.py` | PDF generation (lightweight backend, no native deps) |
| `requests` | `push_to_notion.py` | Notion API calls |
| `yfinance` | `fetch_yahoo_finance.py` | Public comp market data |
| `PyPDF2` | `extract_pdf.py` | Extract text from pitch deck PDFs |
| `openpyxl` | `extract_excel.py` | Extract data from Excel files |

**Optional (richer PDF rendering):**
```bash
pip install xhtml2pdf
```
`generate_pdf.py` tries `xhtml2pdf` first, then falls back to `reportlab` automatically. `xhtml2pdf` produces nicer output (full CSS support) but has heavy native dependencies (`pycairo`, `pyhanko`) that may fail on minimal Linux environments (WSL, Docker, CI). `reportlab` always works.

**Troubleshooting pip on WSL/minimal Linux:**
```bash
# If pip is not available
python3 -m ensurepip --upgrade
# or
curl -sS https://bootstrap.pypa.io/get-pip.py | python3 - --user --break-system-packages

# Then install
python3 -m pip install --user --break-system-packages markdown reportlab requests
```

---

## 2. Notion Integration

### Token

Set the `NOTION_TOKEN` environment variable before starting Claude Code:

```bash
export NOTION_TOKEN=ntn_XXXXXXXXX
```

To persist across sessions, add to `~/.bashrc` or `~/.zshrc`:
```bash
echo 'export NOTION_TOKEN=ntn_XXXXXXXXX' >> ~/.bashrc
```

### Database

The skill pushes to the **Companies Cards** database:

- **Database ID:** `1dfe5367-1ac8-8045-ab59-cd61c9f6d622`
- **URL:** https://www.notion.so/1dfe53671ac88045ab59cd61c9f6d622

This is configured in `SKILL.md` lines 157–158. To change the target database, update those lines.

### Database Schema

The Companies Cards database expects these properties:

| Property | Type | Description |
|----------|------|-------------|
| Company | title | Company name |
| Sector | rich_text | e.g. "Fintech / SME Merchant Acquiring" |
| Comment | rich_text | Short investment summary |
| Decision | select | Options: Postpone, Strong Pass, Reject, Tentative Pass |
| # | rich_text | Internal reference number |
| Suitability | number | Score |
| Tech | number | Score |
| Investors | number | Score |
| Repeats | number | Score |
| Legal & Risks | number | Score |
| Strategic | number | Score |
| IPO | number | Score |
| Momentum | number | Score |
| Team | number | Score |
| CapTable | number | Score |
| Secondary | number | Score |
| Valuation | number | Score |
| Weighted Score | formula | Auto-calculated |
| Total / 48 | formula | Auto-calculated |
| Logo | files | Company logo |

### How It Works (2 steps)

**Step 1 — Create page** via Notion API:
```python
POST https://api.notion.com/v1/pages
# Body: parent database_id + properties (Company, Sector, Comment, Decision)
```

**Step 2 — Push memo content** via bundled script:
```bash
python scripts/push_to_notion.py <PAGE_ID> "output/memo.md" --token $NOTION_TOKEN
```

The script converts markdown to Notion blocks (headings, tables, bullets, dividers) and appends them in batches of 100 (Notion API limit).

### Verify Connection

```bash
python3 -c "
import requests, os
token = os.environ.get('NOTION_TOKEN', '')
if not token:
    print('ERROR: NOTION_TOKEN not set')
    exit(1)
r = requests.get(
    'https://api.notion.com/v1/databases/1dfe53671ac88045ab59cd61c9f6d622',
    headers={'Authorization': f'Bearer {token}', 'Notion-Version': '2022-06-28'}
)
if r.status_code == 200:
    print('OK — connected to Companies Cards database')
else:
    print(f'ERROR {r.status_code}: {r.text[:200]}')
"
```

### Notion Integration Setup (if not already done)

1. Go to https://www.notion.so/my-integrations
2. Create a new integration (or use existing)
3. Copy the token (starts with `ntn_`)
4. In your Companies Cards database, click **...** > **Connections** > add your integration
5. Set the token as `NOTION_TOKEN` env var

---

## 3. PDF Generation

```bash
python scripts/generate_pdf.py "output/YYYY MM DD Company Investment Case.md" \
    --output "output/YYYY MM DD Company Investment Case.pdf"
```

The script auto-selects the best available backend:
1. **xhtml2pdf** (preferred) — full CSS, Notion-like styling
2. **reportlab** (fallback) — lighter output, always works

Both produce clean, readable PDFs with tables, headings, and formatting.

---

## 4. Quick Start Checklist

```
[ ] Python 3.9+ available
[ ] pip install markdown reportlab requests
[ ] export NOTION_TOKEN=ntn_...
[ ] Verify: python3 -c "import markdown, reportlab, requests; print('OK')"
[ ] Verify Notion: run the connection test above
[ ] Test PDF: python scripts/generate_pdf.py <any_memo.md> --output /tmp/test.pdf
```
