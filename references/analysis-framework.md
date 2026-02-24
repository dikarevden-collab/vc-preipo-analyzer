# Analysis Framework — Sections 1-10

When analyzing a company, follow this structured sequence. Each section builds on the previous.

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
