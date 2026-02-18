---
name: vc-preipo-analyzer
description: Comprehensive due diligence and investment analysis for VC-backed and Pre-IPO companies, including financial modeling, comparable public multiples benchmarking, risk scoring, and investment thesis generation
---

# VC / Pre-IPO Investment Analyzer

Structured due diligence framework for evaluating private company investments across financials, market positioning, valuation, comparable public multiples, and risk assessment.

## Sector Detection & Specialization

Automatically detect the company's sector and apply the relevant sector overlay from `references/sector-overlays.md`. **Read only the matching sector section** from that file — do not load all overlays into context. If the sector is ambiguous, ask the user to confirm before proceeding.

**Supported sectors:**
- **SaaS / Cloud Software** — NRR-driven, subscription metrics, Magic Number
- **Fintech** — Regulatory capital, loss rates, take rates, interchange economics
- **Medtech / Biotech** — Clinical pipeline, FDA pathway, reimbursement, IP cliff
- **AI / ML** — Model defensibility, compute costs, data moat, inference economics
- **Infrastructure / Industrials** — CapEx intensity, contract backlog, utilization rates
- **Semiconductors / Chips** — Fab economics, design wins, ASP trends, inventory cycles
- **Cross-Border Payments / Remittance** — TPV, revenue yield, buy rate, corridors, scheme incentives, settlement infrastructure
- **Marketplace / Platform** — GMV, take rate, liquidity, supply/demand balance
- **Consumer / D2C** — Brand equity, repeat rates, CAC channels, retail distribution

After identifying the sector, **append the sector-specific questions and metrics** from `references/sector-overlays.md` to each relevant section of the analysis. Sector-specific items are additive — they do not replace the core framework, they extend it.

## Missing Data Protocol

**Every field in the analysis must have an explicit value.** When information is not available, not disclosed, or cannot be verified:

1. **Mark the field**: `[NO INFO]`
2. **Note the impact**: After each section, include a "Data Gaps" summary listing all [NO INFO] items and their materiality:
   - **Critical** — This gap materially affects the investment decision. Flag for follow-up.
   - **Important** — Weakens analysis confidence but does not block a preliminary assessment.
   - **Minor** — Nice-to-have; does not affect the core thesis.
3. **Aggregate at the end**: In the Investment Thesis section, include a "Data Completeness Score" — the percentage of framework fields that have actual data vs. [NO INFO].
4. **Never guess or fabricate**: If a number is an estimate, label it `[ESTIMATED — basis: ...]`. If it's truly unknown, use `[NO INFO]`. Never present an assumption as a fact.

This ensures every analysis is transparent about what we know, what we don't, and what matters.

## Source Requirements & Citations

**All external data must come from verifiable, authoritative sources.** No unverified web snippets or AI-generated estimates.

### Preferred Data Sources (in priority order)
1. **Yahoo Finance** (finance.yahoo.com) — primary source for public company market data (market cap, P/E, EV/EBITDA, EV/Revenue, revenue, margins). Use the `key-statistics` and `financials` pages. If a Yahoo Finance API or MCP tool is available, use it.
2. **Company IR / SEC filings** — for verified revenue, growth rates, margin data
3. **Capital IQ / Bloomberg / PitchBook** — if the user provides access or data exports
4. **StockAnalysis.com** — secondary source for quick statistics and valuation multiples
5. **CompaniesMarketCap.com / MacroTrends** — for market cap and revenue trends
6. **Industry reports** — FXC Intelligence, McKinsey Global Payments, Nilson Report, etc. for TAM/market data

### Citation Protocol
- **Every section that uses external data must include a `Sources:` block** at the end of that section listing the specific URLs or references used
- Format: `Source: [Description](URL) — accessed [date]`
- For public comp tables: cite the data source for each column header (e.g., "Market cap: Yahoo Finance; Revenue: Company 10-K")
- For TAM/market estimates: cite the originating report, author, and year
- For company-provided data: mark as `Source: Company data room — [filename]`
- **Never present a number without attribution.** If you cannot find a verifiable source, mark it `[UNVERIFIED — source: ...]` and flag it

### What is NOT acceptable
- Pulling numbers from random blog posts, SEO content farms, or AI summary sites
- Using outdated data (>6 months old for trading multiples) without flagging staleness
- Mixing TTM and NTM multiples without labeling each explicitly
- Presenting estimated/consensus numbers as actual reported figures

## Core Capabilities

### Company Profiling
- Consolidated company overview with funding history and cap table context
- Secondary market price tracking and implied valuation
- Founding team and organizational maturity assessment
- Corporate structure and jurisdiction analysis

### Financial Analysis
- Revenue decomposition (ARR, MRR, NRR, GRR, GMV, bookings vs. recognized)
- Unit economics deep-dive (CAC, LTV, LTV/CAC ratio, payback period, contribution margin)
- Burn rate analysis with implied runway and path-to-profitability modeling
- Margin progression (gross, operating, EBITDA, free cash flow)
- Working capital and cash conversion cycle assessment
- Revenue quality scoring (recurring vs. one-time, concentration, cohort retention)

### Comparable Public Multiples Benchmarking
- Identify relevant public company comparables by sector, business model, and growth profile
- Pull and benchmark against key trading multiples:
  - EV/Revenue (NTM and LTM)
  - EV/EBITDA
  - EV/Gross Profit
  - P/E and P/FCF (where applicable)
  - Price/Sales
- Apply appropriate discounts for illiquidity, scale, and private-company risk
- Calculate implied valuation range from public comps
- Rule of 40 scoring (revenue growth % + FCF margin %)
- Growth-adjusted multiples (EV/Revenue / Growth Rate)
- Median, mean, and percentile positioning vs. peer set

### Market & Competitive Analysis
- TAM/SAM/SOM sizing with methodology transparency (top-down vs. bottom-up)
- Market growth trajectory and secular tailwinds/headwinds
- Competitive landscape mapping (direct, adjacent, potential entrants)
- Moat classification (network effects, switching costs, data advantage, brand, regulatory, scale)
- Category maturity assessment and timing risk

### Risk Scoring
- Quantified risk matrix across 8 dimensions (1-10 scale with weighted composite)
- Scenario analysis: base, bull, and bear case with probability weighting
- Key-person dependency and organizational risk
- Regulatory and geopolitical exposure mapping
- Customer and revenue concentration analysis (Herfindahl index where applicable)

### Investment Thesis & Valuation
- DCF-based valuation with sensitivity on WACC, growth, and terminal multiple
- Comparable transaction analysis (recent private rounds, M&A precedents)
- Return analysis: implied IRR at various exit valuations and timelines
- Entry price assessment vs. last round, secondary pricing, and intrinsic value
- Exit pathway analysis (IPO, strategic M&A, secondary sale, continuation fund)

## Analysis Framework

When analyzing a company, follow this structured sequence:

### 1. Company Overview
- Full legal name and DBA
- Business description (what they do, for whom, how they monetize)
- Sector and sub-sector classification
- Headquarters and key operating geographies
- Year founded and current employee count
- Complete funding history: each round (date, amount, valuation, lead investor)
- Total capital raised to date
- Current secondary market price and implied valuation (if available)
- Last primary round valuation and date
- Cap table structure: share classes (Ordinary, Preferred, Growth, Series), CLN/convertible instruments (pre- and post-conversion scenarios), ESOP pool and vesting, warrants, deferred shares, media-for-equity arrangements; fully diluted vs. basic ownership percentages

### 2. Financial Deep Dive
- Revenue metrics: ARR/MRR, growth rate (YoY and QoQ), revenue run-rate
- Net Revenue Retention (NRR) and Gross Revenue Retention (GRR)
- Unit economics: CAC by channel, LTV, LTV/CAC, payback period in months
- Gross margin and gross margin trend (expanding/contracting)
- Operating expenses breakdown (R&D, S&M, G&A as % of revenue)
- EBITDA and EBITDA margin (or adjusted EBITDA if reported)
- Free cash flow and FCF margin
- Monthly burn rate and implied runway at current burn
- Cash on balance sheet and any debt/credit facilities
- Revenue quality: % recurring, customer count, top-10 customer concentration
- Cohort analysis (if available): acquisition cohorts, retention curves, revenue per cohort
- Sub-segment decomposition: break revenue and margins into the finest available segments

### 3. Comparable Public Multiples Analysis
- Select 5-10 public company comparables based on:
  - Same or adjacent sector
  - Similar business model (SaaS, marketplace, fintech, etc.)
  - Comparable growth rate range
  - Similar margin profile
- For each comparable, capture:
  - Company name, ticker, market cap
  - EV/Revenue (NTM), EV/EBITDA, EV/Gross Profit
  - Revenue growth rate (YoY)
  - Gross margin, EBITDA margin, FCF margin
  - Rule of 40 score
  - NRR (if SaaS)
- Calculate peer set statistics (median, mean, 25th/75th percentile)
- Apply private company discount (typically 20-40%, justify the specific discount used)
- Calculate implied valuation range for the target company
- Assess whether current private valuation is at premium or discount to public comps
- Reference file: see `references/comparable-multiples.md` for detailed methodology

### 4. Market Context & Competitive Position
- TAM estimate with source and methodology
- SAM and SOM with clear assumptions
- Market growth rate (historical and projected CAGR)
- Tailwinds: macro trends supporting growth
- Headwinds: structural or cyclical challenges
- Category maturity: early / growth / scaling / mature / consolidating
- Competitive landscape: key competitors, market share estimates
- Moat assessment with specific evidence for each moat type claimed
- Competitive intensity and threat of new entrants

### 5. Growth & Momentum
- Key operating metrics (ARR, users, GMV, transactions, etc.) with trend
- Customer count and growth trajectory
- Net dollar retention and logo retention
- Recent strategic achievements (partnerships, product launches, geographic expansion)
- Sales efficiency metrics (Magic Number, CAC Ratio)
- Hiring velocity and key talent acquisition
- Product roadmap and upcoming catalysts

### 6. Investor & Governance Quality
- Lead investors by round with track record assessment
- Repeat participation across rounds (signal of insider conviction)
- Strategic investors and their operational value-add
- Board composition and governance quality
- Investor rights and protective provisions (if known)
- Pro-rata and follow-on capacity of existing investors

### 7. Risk Assessment Matrix

Score each dimension 1-10 (1 = minimal risk, 10 = critical risk):

| Risk Dimension       | Score | Weight | Weighted Score | Key Factors |
|----------------------|-------|--------|----------------|-------------|
| Market Risk          |       | 15%    |                |             |
| Competition Risk     |       | 15%    |                |             |
| Execution Risk       |       | 15%    |                |             |
| Financial Risk       |       | 15%    |                |             |
| Valuation Risk       |       | 10%    |                |             |
| Regulatory Risk      |       | 10%    |                |             |
| Technology Risk      |       | 10%    |                |             |
| Key-Person Risk      |       | 10%    |                |             |
| **Composite Score**  |       | 100%   |                |             |

- For each risk dimension, provide 2-3 specific supporting factors
- Flag any dimension scoring 7+ as requiring mitigation plan
- Overall risk classification: Low (1-3) / Moderate (4-5) / Elevated (6-7) / High (8-10)

### 8. Valuation & Return Analysis
- Current valuation (last round and/or secondary) vs. fundamental value
- Implied multiples at current valuation (EV/Revenue, EV/Gross Profit, etc.)
- Comparison to public comp implied range (from Section 3)
- Scenario-based return analysis:

| Scenario   | Probability | Exit Multiple | Exit Valuation | IRR (3yr) | IRR (5yr) | MOIC |
|------------|-------------|---------------|----------------|-----------|-----------|------|
| Bull Case  |             |               |                |           |           |      |
| Base Case  |             |               |                |           |           |      |
| Bear Case  |             |               |                |           |           |      |
| **Expected**|            |               |                |           |           |      |

- Probability-weighted expected return
- Sensitivity table: IRR at various entry prices and exit multiples
- Exit pathway assessment (IPO timeline, likely acquirers, secondary liquidity)

### 9. Investment Thesis
- **Conviction rating**: Strong Pass / Pass / Neutral / Buy / Strong Buy
- **Top 3-5 reasons to invest** (with specific supporting evidence)
- **Top 3-5 reasons NOT to invest** (with specific counter-arguments)
- **Key catalysts** that could inflect the investment positively
- **Key de-risking milestones** to monitor
- **Position sizing recommendation** (relative to portfolio context)
- **Follow-up diligence questions** that remain unanswered

### 10. Supporting Materials & Data Room
- Links to data room (if available)
- Key articles, press coverage, and analyst reports
- Pitch deck assessment (quality, consistency with financials)
- Management references and background checks
- Prior research notes and internal memos

## Bundled Scripts

Use these scripts for deterministic, repeatable data extraction and fetching.

### `scripts/fetch_yahoo_finance.py`
Fetch structured public comp data from Yahoo Finance. Run this for Section 3 (Comparable Public Multiples).
```bash
python scripts/fetch_yahoo_finance.py WISE.L RELY DLO FLYW PAYONEER WU --format table
```
Output: markdown table with market cap, EV/Revenue, EV/EBITDA, EV/GP, margins, Rule of 40, median row. Source attribution is printed to stderr automatically.

Requires: `pip install yfinance`

### `scripts/extract_pdf.py`
Extract text from data room PDFs. Use for pitch decks, executive summaries, financial reports.
```bash
python scripts/extract_pdf.py "path/to/file.pdf" --pages 1-10 --max-chars 50000
```
Handles Windows Unicode issues automatically.

Requires: `pip install PyPDF2`

### `scripts/extract_excel.py`
Extract data from Excel files. Use for financial models, cap tables, OPEX breakdowns.
```bash
python scripts/extract_excel.py "path/to/model.xlsx" --sheets "Income Statement,Cap Table" --max-rows 200
```
Reads formula results (not formulas) by default.

Requires: `pip install openpyxl`

### `scripts/push_to_notion.py`
Push a completed memo to an existing Notion page as formatted blocks (headings, tables, bullets, bold/italic, dividers, checkboxes).
```bash
python scripts/push_to_notion.py PAGE_ID "path/to/memo.md" --token $NOTION_TOKEN
```
Batches blocks in groups of 100 (Notion API limit). Falls back to block-by-block on errors.

Requires: `pip install requests`

### `scripts/generate_pdf.py`
Generate a Notion-styled PDF from a markdown memo. Used as the final output step — saves PDF to the user's project folder.
```bash
python scripts/generate_pdf.py "path/to/memo.md" --output "path/to/output.pdf"
```
Notion-like CSS: clean typography, formatted tables, alternating row colors, proper heading hierarchy. If `--output` is omitted, saves PDF next to the source `.md` file.

Requires: `pip install markdown xhtml2pdf`

## Context Efficiency

Load supporting files **selectively** to avoid prompt-too-long errors:
- `references/sector-overlays.md` — read **only** the detected sector section, not the entire file
- `references/comparable-multiples.md` — read when building the comp table (Section 3)
- `assets/analysis-template.md` — reference for output structure; load at output time
- `references/due-diligence-checklist.md` — load only if the user requests a DD status check
- Do NOT load all supporting files upfront. Read each only when its section is being worked on.

## Input Requirements

- **Company name or description**: Required. Provide as argument or in conversation
- **Financial data**: Pitch deck, financial statements, data room contents, or key metrics
- **Market data**: Industry reports, competitor information, or market sizing sources
- **Accepted formats**: PDF, CSV, JSON, plain text, Excel references, or conversational input
- **Public comps**: Optionally provide a specific peer set; otherwise one will be constructed

## Output Format: Investment Memo

The final deliverable is a **standalone investment memo** saved as a markdown file. The memo must be:
- **Self-contained** — readable by someone who has not seen the data room or conversation
- **Ready for human review** — the analyst generates it, a human reviews, edits, and finalizes
- **Dual save** — written to local project folder AND pushed to Notion (see below)

### Local Save Convention
- If user provides a `--folder` path (e.g., `C:\Users\denis\OneDrive\Work\Paysend`), save the memo there as `[Company]-Analysis-[YYYY-MM-DD].md`
- If no folder specified, save to the skill's `output/` directory as fallback
- The user's convention: create a local folder for each project, put data room files in it, provide the path when invoking the skill. The skill reads from there and saves the memo there.

### Post-Analysis Output Pipeline
After the memo markdown is written, execute these steps automatically:
1. **Generate PDF** — `python scripts/generate_pdf.py memo.md --output "folder/Company-Analysis-YYYY-MM-DD.pdf"` (saves to the user's project folder)
2. **Push to Notion** — create page in Companies Cards database, then run `python scripts/push_to_notion.py PAGE_ID memo.md --token $NOTION_TOKEN`
3. **Confirm to user** — report local file paths (md + pdf) and Notion page URL

### Memo Structure (mandatory, in this order)
1. **Header** — Company name, date, sector, data freshness, conviction rating
2. **Executive Summary** — 2-3 paragraphs at the TOP: what the company does, key financials, valuation vs comps, recommendation. Must be readable as a standalone brief for quick decision-making
3. **Sections 1-10** — Full analysis following the framework above
4. **Sources appendix** — Consolidated list of all external sources used, with URLs and access dates

### Source Attribution Rules (within the memo)
- Each section that references external data must end with a `**Sources:**` block
- Public comp data: cite Yahoo Finance or equivalent with access date
- TAM / market data: cite the report name, publisher, and year
- Company data: cite as `Company data room — [filename]`
- All trading multiples must state whether they are TTM or NTM
- If data is older than 6 months, flag it as `[STALE — as of YYYY-MM]`

### Reference file
See `assets/analysis-template.md` for the full standardized output structure with all tables and sections.

## Example Usage

> "Analyze SpaceX as a pre-IPO investment opportunity. Focus on the Starlink segment economics, use satellite/telecom and aerospace/defense public comps for the multiples analysis."

> "I have the Series C pitch deck for [Company]. Evaluate the investment at a $2B valuation, benchmark against public SaaS comps growing 40%+ YoY, and score the risks."

> "Compare the secondary market pricing of Stripe, Databricks, and Canva against their respective public comp sets. Which offers the best risk-adjusted entry point?"

> "Run a bear/base/bull scenario analysis for Anduril at its last reported $14B valuation. Focus on defense sector multiples and contract backlog analysis."

> "Here are the financials for a Series B fintech company. Build the comp table, calculate implied valuation, and tell me if the $500M ask is reasonable."

## Post-Analysis: Notion Export

After completing the analysis and saving the memo locally, push it to the Notion database.

### Configuration
- **Database ID:** `1dfe5367-1ac8-8045-ab59-cd61c9f6d622` (Companies Cards)
- **Token env var:** `NOTION_TOKEN` (configured in Notion MCP server)

### Export Steps
1. Create a page in the database via Notion API:
   ```bash
   curl -s -X POST "https://api.notion.com/v1/pages" \
     -H "Authorization: Bearer $NOTION_TOKEN" \
     -H "Notion-Version: 2022-06-28" \
     -H "Content-Type: application/json" \
     -d '{"parent": {"database_id": "1dfe5367-1ac8-8045-ab59-cd61c9f6d622"}, "properties": {"Company": {"title": [{"type": "text", "text": {"content": "COMPANY_NAME"}}]}, "Sector": {"rich_text": [{"type": "text", "text": {"content": "SECTOR"}}]}}}'
   ```
2. Push the formatted memo using the bundled script:
   ```bash
   python scripts/push_to_notion.py PAGE_ID memo_file.md --token $NOTION_TOKEN
   ```
   This converts markdown headings, tables, bullets, bold/italic, dividers, and checkboxes into native Notion blocks.

### Database Properties (Companies Cards)
The database uses a scoring system. Populate `Company` (title) and `Sector` (rich_text) at page creation. Other properties (scoring columns, Decision) are filled manually by the user after review.

**If Notion MCP is unavailable or the database is not shared with the integration, skip the export step and inform the user.**

## Best Practices Applied

### Analytical Standards
- Always triangulate valuation using multiple methodologies (comps, DCF, precedent transactions)
- Distinguish between reported metrics and adjusted/normalized metrics
- Verify growth rates are calculated consistently (ARR vs. revenue, annualized vs. trailing)
- Apply appropriate private company discounts with explicit justification
- Use NTM (next-twelve-months) multiples as primary, LTM as secondary reference

### Investment Rigor
- Separate factual observations from subjective assessments
- Present both bull and bear cases with equal analytical rigor
- Quantify risks where possible rather than using qualitative descriptors alone
- Benchmark all key metrics against sector medians, not just cherry-picked comps
- Flag data gaps and their impact on analysis confidence

### Intellectual Honesty
- Explicitly state data freshness and source reliability
- Acknowledge where estimates are used vs. verified figures
- Highlight areas where additional diligence would materially change conclusions
- Avoid anchoring bias from last-round valuation or management projections

## Limitations and Disclaimers

- This analysis is for informational and educational purposes only and does not constitute investment advice
- Private company financial data may be unaudited, self-reported, or incomplete
- Public comparable multiples change daily; analysis reflects a point-in-time snapshot
- Private company discounts are estimates and vary by market conditions and deal specifics
- Projections and scenario analyses are inherently uncertain
- TAM estimates are directional and should be stress-tested against bottom-up models
- This skill does not have access to paid financial data terminals (Bloomberg, PitchBook, etc.) unless provided by the user

## Quality Checks

1. Verify all financial metrics are internally consistent (e.g., ARR = MRR x 12)
2. Confirm comparable companies are genuinely comparable (similar sector, scale, growth profile)
3. Validate that implied valuation ranges are reasonable given the company's stage
4. Check that risk scores align with the qualitative risk descriptions
5. Ensure scenario probabilities sum to 100%
6. Verify IRR calculations use consistent entry valuation and time horizons
7. Confirm that the investment thesis is supported by the preceding analysis
8. Cross-reference public multiples against recent data (flag if data may be stale)
