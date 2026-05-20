# Setup Guide

Quick setup for Notion integration, PDF generation, and Python dependencies.

## Table of Contents

- [1. Python Dependencies](#1-python-dependencies)
- [2. Notion Integration](#2-notion-integration)
- [3. PDF Generation](#3-pdf-generation)
- [4. Quick Start Checklist](#4-quick-start-checklist)

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

### Important: Internal Integration ≠ claude.ai Notion connector

There are **two completely separate Notion paths**, and only one is durable:

| | Internal Integration (this skill uses) | claude.ai Notion MCP |
|---|---|---|
| Created where | https://www.notion.so/profile/integrations | Anthropic web app → Connectors |
| Token format | `ntn_…` (long-lived, you control it) | OAuth, managed by Anthropic |
| Used by | `push_to_notion.py` + direct `curl` | `mcp__claude_ai_Notion__*` tools |
| Block types supported | All (tables, headings, callouts, code) | paragraph + bulleted_list_item only |
| Stays connected mid-session | Yes — fully local | No — can drop |

**The Internal Integration is the durable path.** The claude.ai MCP connector is fine for lookups but **must not** be used for memo content pushes (it silently drops tables and headings) or for page creation (`notion-create-pages` double-serializes the `parent` field and fails).

### Token setup

**Windows (primary path — PowerShell):**
```powershell
[System.Environment]::SetEnvironmentVariable("NOTION_TOKEN", "ntn_XXXXXXXXX", "User")
```
Then restart Claude Code so the new env var is loaded by child processes.

Verify it's persisted:
```powershell
[System.Environment]::GetEnvironmentVariable("NOTION_TOKEN", "User")
```

**macOS / Linux:**
```bash
export NOTION_TOKEN=ntn_XXXXXXXXX
echo 'export NOTION_TOKEN=ntn_XXXXXXXXX' >> ~/.bashrc   # or ~/.zshrc
```

**Do NOT store the token in `~/.claude.json`** under `mcpServers.notionApi.env.NOTION_TOKEN`. That path was used when the legacy `@notionhq/notion-mcp-server` package was configured, but it is brittle (block-type limitations, plus the file is touched by Claude Code at startup). The env-var path is the canonical storage location.

### Share the database with the integration **[required — easy to miss]**

The token alone gives no access. Each individual page or database the integration touches must be explicitly connected:

1. Open the Companies Cards database: https://www.notion.so/1dfe53671ac88045ab59cd61c9f6d622
2. Top-right `…` menu → **Connections** → **Connect to** → pick the Internal Integration (e.g. `VCAnalyzer`)
3. Confirm. Child pages inherit access automatically.

If you skip this step, the API returns `object_not_found` / 404 and looks like a token problem when it is actually a sharing problem.

### Database

The skill pushes to the **Companies Cards** database:

- **Database ID:** `1dfe5367-1ac8-8045-ab59-cd61c9f6d622`
- **URL:** https://www.notion.so/1dfe53671ac88045ab59cd61c9f6d622

This is configured in `SKILL.md` § Post-analysis pipeline step 8. To change the target database, update those lines and re-share the new DB with the integration.

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

**Step 1 — Create the page via curl** (NOT via `notion-create-pages` MCP — `parent` field double-serializes and fails):
```bash
curl -s -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": {"database_id": "1dfe5367-1ac8-8045-ab59-cd61c9f6d622"},
    "properties": {
      "Company": {"title": [{"text": {"content": "{Company}"}}]},
      "Sector": {"rich_text": [{"text": {"content": "{Sector}"}}]},
      "Comment": {"rich_text": [{"text": {"content": "{1-line headline}"}}]}
    }
  }'
```
Capture `id` from the response as `PAGE_ID`. Scoring columns (Suitability / Tech / Investors / Team / Momentum / Strategic / Legal & Risks / IPO / Secondary / CapTable / Valuation / Repeats) are left empty — those are for the analyst's manual IC scoring.

**Step 2 — Push memo content via the script:**
```bash
python scripts/push_to_notion.py <PAGE_ID> "output/memo.md" --token "$NOTION_TOKEN"
```

The script converts markdown to Notion blocks (headings, tables, bullets, callouts, dividers, code blocks) and appends them in batches of 100 (Notion API per-PATCH limit). Rich-text segments longer than 2000 chars are split automatically.

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

1. Go to https://www.notion.so/profile/integrations
2. **+ New integration** → name it (e.g. `VCAnalyzer`) → Type: **Internal** → workspace: your RLC workspace
3. Capabilities: ✅ Read content, ✅ Update content, ✅ Insert content
4. Save → copy the **Internal Integration Secret** (starts with `ntn_…`)
5. Open the Companies Cards database → `…` menu → **Connections** → connect the integration (workspace access is not enough)
6. Set the token as a Windows User env var (see "Token setup" above)
7. Verify with the script in "Verify Connection" below

### Common Notion errors

| Error | Likely cause | Fix |
|---|---|---|
| `401 unauthorized` | Token wrong, expired, or not set | Re-copy token from integration page; re-set env var; restart shell |
| `404 object_not_found` on the database | Integration not shared with the DB | Open DB → `…` → Connections → add integration |
| `400 validation_error` on `parent` field | Using `notion-create-pages` MCP (double-serializes) | Use curl directly per "Step 1" above |
| Table cells appear blank after push | Used claude.ai MCP `notion-update-page` (paragraph-only) | Use `push_to_notion.py` script instead — full block support |
| `claude.ai Notion` tool dropped mid-pipeline | MCP connector disconnected (harmless) | Script path is independent; Notion push still works |

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
