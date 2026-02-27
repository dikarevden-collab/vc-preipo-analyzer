
## What It Does

Given a company name, pitch deck, or financial data, the skill produces a **standalone investment memo** following a consistent 10-section framework:

| # | Section | Covers |
|---|---------|--------|
| 1 | Company Overview | Identity, funding history, cap table |
| 2 | Financial Deep Dive | Revenue, unit economics, margins, burn rate |
| 3 | Comparable Public Multiples | Peer set, TTM multiples, implied valuation range |
| 4 | Market Context | TAM/SAM/SOM, competitive landscape, moat assessment |
| 5 | Growth & Momentum | Operating metrics, sales efficiency, catalysts |
| 6 | Investor & Governance | Round history, board composition, signal quality |
| 7 | Risk Assessment | Weighted 8-dimension scoring matrix |
| 8 | Valuation & Return | Bull/base/bear scenarios, IRR, MOIC, exit pathways |
| 9 | Investment Thesis | Conviction rating, for/against arguments, key questions |
| 10 | Supporting Materials | Data room links, pitch deck notes, articles |
# VC / Pre-IPO Investment Analyzer

A [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skill that generates institutional-grade investment memos for private company due diligence. It produces structured, 10-section analyses covering financials, compa
Every data point is sourced and cited. Missing information is explicitly marked `[NO INFO]` or `[ESTIMATED — basis: ...]` with materiality ratings — the memo never guesses.

## Sector Specialization

The skill detects the company's sector and applies a tailored overlay with sector-specific metrics, DD questions, and risk weight adjustments:

- **SaaS / Cloud Software** — NRR, Magic Number, Rule of 40, CAC payback
- **Fintech** — Take rate, default rates, regulatory capital, money transmission licenses
- **Medtech / Biotech** — Clinical pipeline, rNPV, FDA pathway, reimbursement strategy
- **AI / ML** — Compute costs, inference economics, model defensibility, data moat
- **Cross-Border Payments** — TPV, revenue yield (bps), corridor economics, cohort retention
- **Semiconductors / Chips** — Design wins, ASP trends, foundry dependencies, export controls
- **Marketplace / Platform** — GMV, take rate, supply/demand unit economics, multi-homing risk
- **Infrastructure / Industrials** — Backlog, book-to-bill, CapEx intensity, contract types
- **Consumer / D2C** — Repeat purchase rate, CLV by cohort, channel mix, CAC trajectory

## Project Structure

```
vc-preipo-analyzer/
├── SKILL.md                           # Skill definition (Claude Code entry point)
├── FAQ.md                             # How the skill works
│
├── references/                        # Knowledge base
│   ├── analysis-framework.md          # 10-section checklist with required fields
│   ├── sector-overlays.md             # 9 sector specializations
│   ├── comparable-multiples.md        # Comp methodology & discount framework
│   ├── due-diligence-checklist.md     # DD tracking (64 items across 8 categories)
│   ├── faq.md                         # Internal reference FAQ
│   └── setup-guide.md                 # Python deps & Notion configuration
│
├── assets/
│   └── analysis-template.md           # Output memo structure template
│
├── scripts/                           # Python utilities
│   ├── fetch_yahoo_finance.py         # Public comp multiples from Yahoo Finance
│   ├── extract_pdf.py                 # PDF text extraction (pitch decks, reports)
│   ├── extract_excel.py               # Excel data extraction (models, cap tables)
│   ├── generate_pdf.py                # Markdown → Notion-styled PDF
│   └── push_to_notion.py             # Export memo to Notion database
│
└── output/                            # Generated memos (gitignored)
```

## Setup

### Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) CLI
- Python 3.9+

### Install

1. Clone this repository into your Claude Code skills directory:
   ```bash
   git clone https://github.com/YOUR_USERNAME/vc-preipo-analyzer.git \
     ~/.claude/skills/vc-preipo-analyzer
   ```

2. Install Python dependencies:
   ```bash
   pip install yfinance PyPDF2 openpyxl markdown reportlab requests
   ```
   For richer PDF output (optional):
   ```bash
   pip install xhtml2pdf
   ```

3. *(Optional)* Configure Notion integration:
   ```bash
   export NOTION_TOKEN=your_notion_integration_token
   ```
   See [references/setup-guide.md](references/setup-guide.md) for full Notion database setup.

## Usage

Open Claude Code and prompt naturally:

```
Analyze SpaceX as a pre-IPO investment opportunity.
Focus on Starlink segment economics.
```

```
I have the Series C pitch deck for [Company].
Evaluate at a $2B valuation, benchmark against public SaaS comps growing 40%+ YoY.
```

```
Compare secondary market pricing of Stripe, Databricks,
and Canva against their public comp sets.
```

```
Run a bear/base/bull scenario analysis for Anduril at $14B valuation.
```

The skill activates when it detects investment analysis intent — keywords like *"analyze"*, *"evaluate"*, *"investment memo"*, *"due diligence"*, *"comp table"*, or *"investment case"*.

### Input Formats

| Format | Use Case |
|--------|----------|
| Plain text | Company description, key metrics, conversational input |
| PDF | Pitch decks, financial statements, data room documents |
| Excel (.xlsx) | Financial models, cap tables, operating data |
| Ticker symbols | Public comparable companies for benchmarking |

### Output

The skill produces three artifacts:

1. **Markdown memo** — `output/YYYY MM DD CompanyName Investment Case.md`
2. **PDF** — Notion-styled, presentation-ready
3. **Notion page** — Pushed to a configured database (if `NOTION_TOKEN` is set)

## Bundled Scripts

Each script works standalone from the command line:

### Fetch Public Comps
```bash
python scripts/fetch_yahoo_finance.py WISE.L RELY DLO FLYW WU --format table
```
Returns market cap, EV, EV/Revenue, EV/EBITDA, margins, growth, Rule of 40, with internal consistency checks and outlier detection.

### Extract PDF Text
```bash
python scripts/extract_pdf.py "pitch-deck.pdf" --pages 1-10 --max-chars 50000
```

### Extract Excel Data
```bash
python scripts/extract_excel.py "model.xlsx" --sheets "P&L,Cap Table" --max-rows 200
```

### Generate PDF
```bash
python scripts/generate_pdf.py "output/memo.md" --output "output/memo.pdf"
```
Dual-backend: tries xhtml2pdf first (richer CSS), falls back to reportlab (always works).

### Push to Notion
```bash
python scripts/push_to_notion.py PAGE_ID "output/memo.md" --token $NOTION_TOKEN
```
Parses markdown into Notion blocks (headings, tables, lists, inline formatting) and pushes via the Notion API.

## Key Design Principles

| Principle | How |
|-----------|-----|
| **Consistency** | Every memo follows the same 10-section template — enables side-by-side deal comparison |
| **Transparency** | Every gap is marked `[NO INFO]` with materiality; estimates show their basis |
| **Rigor** | Sector overlays add domain-specific metrics; 8-dimension risk matrix enforces scoring discipline |
| **Source discipline** | Every external number is cited with URL and access date; stale data (>6 mo) flagged |
| **Actionability** | Conviction rating + key milestones + remaining questions — decision support, not just analysis |
| **Context efficiency** | Reference files loaded selectively (e.g., only the relevant sector overlay) to minimize token usage |

## Methodology Highlights

### Private Company Discount Framework

Public comp multiples are adjusted with a 20–40% base discount, refined by:
- IPO timeline proximity
- Revenue scale relative to comps
- Profitability profile
- Market conditions
- Data transparency and governance quality
- Secondary market liquidity
- Growth rate premium/discount

### Risk Assessment Matrix

Eight dimensions, each scored 1–10 with configurable weights (sector overlays adjust defaults):

| Dimension | Default Weight |
|-----------|---------------|
| Market | 15% |
| Competition | 15% |
| Execution | 15% |
| Financial | 15% |
| Valuation | 15% |
| Regulatory | 15% |
| Technology | 5% |
| Key Person | 5% |

Sector overlays shift weights (e.g., Regulatory → 25% for Medtech, Technology → 20% for AI/ML).

### Conviction Scale

| Rating | Meaning |
|--------|---------|
| Strong Buy | High conviction, favorable risk/reward |
| Buy | Positive, with manageable risks |
| Neutral | Balanced risk/reward, needs more data |
| Pass | Unfavorable risk/reward at current terms |
| Strong Pass | Fundamental concerns, avoid |

## Quality Checks

Before finalizing, the skill validates:

- Financial metrics are internally consistent (e.g., ARR = MRR × 12)
- Comparables are genuinely comparable (sector, scale, growth profile)
- Implied valuation ranges are reasonable for stage
- Risk scores align with qualitative descriptions
- Scenario probabilities sum to 100%
- IRR calculations use consistent entry valuation and time horizons
- Investment thesis is supported by the preceding analysis
- Public multiples are cross-referenced against recent data

## Limitations

- **Not investment advice** — for informational and educational purposes only
- Private company data may be unaudited or incomplete
- Public multiples are point-in-time snapshots
- No access to Bloomberg, Capital IQ, or PitchBook unless the user provides data
- Projections and scenarios are inherently uncertain

## License

This project is provided as-is for personal and educational use.
