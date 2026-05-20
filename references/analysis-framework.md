# Analysis Framework — Sections 1-10

When analyzing a company, follow this structured sequence. Each section builds on the previous.

## Table of Contents

- [1. Company Overview](#1-company-overview)
- [2. Financial Deep Dive](#2-financial-deep-dive)
- [3. Comparable Public Multiples Analysis](#3-comparable-public-multiples-analysis)
- [3.5 Secondary Market Pricing](#35-secondary-market-pricing)
- [4. Market Context & Competitive Position](#4-market-context--competitive-position)
- [5. Growth & Momentum](#5-growth--momentum)
- [6. Investor & Governance Quality](#6-investor--governance-quality)
- [7. Risk Assessment Matrix](#7-risk-assessment-matrix)
- [8. Valuation & Return Analysis](#8-valuation--return-analysis) — incl. 8.1 Deal Mechanics for multi-tranche deals
- [9. Investment Thesis](#9-investment-thesis)
- [10. Supporting Materials & Data Room](#10-supporting-materials--data-room)
- [11. Verification Report (auto-generated)](#11-verification-report-auto-generated)
- [12. Appendix (optional)](#12-appendix-optional)

## 1. Company Overview
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

## 2. Financial Deep Dive
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

## 3. Comparable Public Multiples Analysis
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

## 3.5 Secondary Market Pricing

- Run `scripts/fetch_secondary_prices.sh "Company Name"` to scrape live prices
- Requires: `agent-browser` CLI connected to Chrome debug profile (port 9222)
- Record prices from each platform:
  - **Forge Global** — public, no login needed
  - **Caplight** — requires authenticated session
  - **Hiive** — requires authenticated session
- Calculate cross-platform average and price spread (max - min)
- Compare secondary-implied valuation vs last primary round valuation
- If agent-browser is unavailable or company not found on any platform → mark `[NO INFO]`
- Reference: `references/secondary-selectors.md` for platform navigation details

## 4. Market Context & Competitive Position
- TAM estimate with source and methodology
- SAM and SOM with clear assumptions
- Market growth rate (historical and projected CAGR)
- Tailwinds: macro trends supporting growth
- Headwinds: structural or cyclical challenges
- Category maturity: early / growth / scaling / mature / consolidating
- Competitive landscape: key competitors, market share estimates
- Moat assessment with specific evidence for each moat type claimed
- Competitive intensity and threat of new entrants

## 5. Growth & Momentum
- Key operating metrics (ARR, users, GMV, transactions, etc.) with trend
- Customer count and growth trajectory
- Net dollar retention and logo retention
- Recent strategic achievements (partnerships, product launches, geographic expansion)
- Sales efficiency metrics (Magic Number, CAC Ratio)
- Hiring velocity and key talent acquisition
- Product roadmap and upcoming catalysts
- **Crunchbase Signals** (captured per SKILL.md § Crunchbase Signals Capture): **Growth Score** (0-100, with arrow), **CB Rank** (integer, lower = better, with arrow), **Heat Score** (0-100, with arrow). Date-stamp the values and add one line of analyst commentary using the interpretation rubric — arrows matter as much as the numbers. Example commentary: *"Heat 92 ↑ reflects active news cycle from Series B close; Growth 86 ↓ shows the underlying employee/traffic momentum is decelerating from a 12-month peak — interpret as 'currently in the spotlight but the fundamentals were stronger six months ago.'"* Mark `[NO INFO]` if analyst declined to provide and no Crunchbase PDF was supplied.

## 6. Investor & Governance Quality
- Lead investors by round with track record assessment
- Repeat participation across rounds (signal of insider conviction)
- Strategic investors and their operational value-add
- Board composition and governance quality
- Investor rights and protective provisions (if known)
- Pro-rata and follow-on capacity of existing investors

## 7. Risk Assessment Matrix

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

## 8. Valuation & Return Analysis

### 8.1 Deal Mechanics (for non-trivial deal structures)

**Include this subsection if the deal is structurally complex** — multi-tranche, SPAC/de-SPAC, SAFE conversion, tender offer, primary + secondary mix, or any instrument with non-standard conversion mechanics. Skip for plain primary or secondary equity.

For each tranche / instrument offered, document:
- Instrument type (SAFE / PIPE / direct primary / secondary / SPV unit / etc.)
- Pricing (headline + any discount mechanic)
- Effective entry valuation (analyst math)
- Day-1 paper gain at par (entry vs. fair value)
- Net Day-1 gain after vehicle/SPV fees
- Lockup
- Capacity available
- What happens if the deal mechanics fail (SPAC doesn't close, round fails to fill)
- Status (signed / open / pending)

Use a single side-by-side comparison table when multiple tranches are offered.

### 8.2 Current Pricing

- Current valuation (last round and/or secondary) vs. fundamental value
- Implied multiples at current valuation (EV/Revenue, EV/Gross Profit, etc.)
- For multi-tranche deals: implied multiples at EACH effective entry price (e.g., post-discount SAFE valuation, post-discount PIPE valuation)
- Comparison to public comp implied range (from Section 3)

### 8.3 Scenario Analysis

Scenario-based return analysis. **For multi-tranche deals, show MOIC and IRR per tranche** (the underlying scenarios are identical, but entry prices differ):

| Scenario   | Probability | Exit Multiple | Exit Valuation | [Tranche A] MOIC | [Tranche A] IRR | [Tranche B] MOIC | [Tranche B] IRR |
|------------|-------------|---------------|----------------|------------------|-----------------|------------------|-----------------|
| Bull Case  |             |               |                |                  |                 |                  |                 |
| Base Case  |             |               |                |                  |                 |                  |                 |
| Bear Case  |             |               |                |                  |                 |                  |                 |
| **Expected** |           |               |                |                  |                 |                  |                 |

State whether MOIC/IRR figures are **gross** or **net of fees** (and the fee assumptions used). Standard is to show both: gross at the deal level, then net after applying SPV/vehicle 2/20 (or actual) fee structure over the hold period.

### 8.4 Sensitivity Analysis

Sensitivity table: IRR (and MOIC) at various entry prices and exit multiples. For multi-tranche deals, sensitivity is most useful at the BEST tranche's entry price (since that's the most attractive available cost basis).

### 8.5 Exit Pathways

Exit pathway assessment (IPO timeline, likely acquirers, secondary liquidity). For SPAC deals, include the "SPAC merger fails to close" scenario explicitly with its consequences per tranche.

## 9. Investment Thesis
- **Conviction rating**: Strong Pass / Pass / Neutral / Buy / Strong Buy
- **Top 3-5 reasons to invest** (with specific supporting evidence)
- **Top 3-5 reasons NOT to invest** (with specific counter-arguments)
- **Key catalysts** that could inflect the investment positively
- **Key de-risking milestones** to monitor
- **Position sizing recommendation** (relative to portfolio context)
- **Follow-up diligence questions** that remain unanswered

## 10. Supporting Materials & Data Room
- Links to data room (if available)
- Key articles, press coverage, and analyst reports
- Pitch deck assessment (quality, consistency with financials)
- Management references and background checks
- Prior research notes and internal memos

## 11. Verification Report (auto-generated)

After drafting sections 1-10, launch an independent verification agent that:
- Reads the completed memo draft
- Independently web-searches all factual claims (company facts, financials, market data, comps, partnerships)
- Rates each claim: CONFIRMED / DISPUTED / UNVERIFIABLE
- Produces an Accuracy Score = confirmed / (confirmed + disputed)
- Flags DISPUTED claims inline in the memo for analyst review
- This section is appended automatically — do not write it manually

**On memo rewrites:** If the memo is substantially rewritten after initial verification (e.g., new deal-structure details from GP, corrected framing), append an "Update — {date}" sub-section to the existing Verification Report describing what changed and what was re-verified. Re-run a focused verification pass (not the full original) — checking only: (1) internal arithmetic consistency, (2) new claims added in the rewrite, (3) stale-data spot-check on time-sensitive facts (valuations, leadership roles, public stock prices).

## 12. Appendix (optional)

Use this section for analytical commentary that does not fit cleanly in Sections 1–11 but is material to the IC's understanding. Examples:
- Why this deal is structured the way it is (e.g., "Why a SPAC and not a private round?")
- Cross-cycle / cross-comparable historical context
- Detailed walk-throughs of specific risk scenarios
- Counterfactual analysis (what would change our view)

Keep to one focused topic per Appendix item; multiple appendices can use sub-headings (12.1, 12.2, etc.). The full memo retains its conviction rating in Section 9 — the Appendix does not duplicate the recommendation, it provides structural / analytical context that informs it.
