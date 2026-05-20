# Comparable Public Multiples — Methodology Reference

## Table of Contents

- [Comp Selection Criteria](#comp-selection-criteria)
- [Key Multiples by Business Model](#key-multiples-by-business-model)
- [Private Company Discount Framework](#private-company-discount-framework)
- [Comp Table Template](#comp-table-template)
- [Implied Valuation Summary](#implied-valuation-summary)
- [Common Pitfalls](#common-pitfalls)
- [Data Sources](#data-sources)

## Comp Selection Criteria

When building a comparable company set, apply these filters in order of priority:

### Primary Filters (must match)
1. **Business model**: SaaS, marketplace, fintech, hardware, consumer, etc.
2. **Sector/vertical**: Same industry or closely adjacent
3. **Revenue scale**: Within 0.3x-3x of the target's revenue (or ARR)

### Secondary Filters (should match where possible)
4. **Growth rate**: Within +/- 15 percentage points of target's growth rate
5. **Margin profile**: Similar gross margin structure (e.g., 70%+ for SaaS, 40-60% for marketplace)
6. **Geographic focus**: Same primary market or similar market dynamics
7. **Monetization model**: Subscription, transaction-based, usage-based, hybrid

### Ideal Comp Set Size
- **Minimum**: 5 companies (fewer introduces selection bias)
- **Target**: 7-10 companies
- **Maximum**: 15 (beyond this, signal-to-noise degrades)

## Key Multiples by Business Model

### SaaS / Subscription Software
| Multiple | Primary | Why It Matters |
|----------|---------|----------------|
| EV/Revenue (NTM) | Yes | Standard SaaS valuation metric |
| EV/Gross Profit | Yes | Normalizes for margin differences |
| EV/ARR | Yes | Captures recurring revenue quality |
| Rule of 40 | Yes | Growth + profitability balance |
| EV/FCF | Secondary | Relevant for mature SaaS |

**Key operating metrics to compare**: NRR, GRR, CAC payback, Magic Number, LTV/CAC

### Marketplaces / Platforms
| Multiple | Primary | Why It Matters |
|----------|---------|----------------|
| EV/Revenue (NTM) | Yes | Net revenue basis |
| EV/Gross Profit | Yes | Normalizes for take rate |
| GMV Multiple | Secondary | Scale comparison |
| P/E | Secondary | For profitable marketplaces |

**Key operating metrics to compare**: Take rate, GMV growth, buyer/seller economics, liquidity

### Fintech
| Multiple | Primary | Why It Matters |
|----------|---------|----------------|
| EV/Revenue (NTM) | Yes | Standard |
| P/E (NTM) | Yes | Profitability matters more here |
| Price/Book | Secondary | For lending/banking models |
| EV/Gross Profit | Yes | Normalizes for funding costs |

**Key operating metrics to compare**: Net interest margin, loss rates, origination growth, unit economics

### Hardware / Deep Tech
| Multiple | Primary | Why It Matters |
|----------|---------|----------------|
| EV/Revenue (NTM) | Yes | Standard |
| EV/EBITDA | Yes | Capital intensity matters |
| P/E | Secondary | For profitable companies |
| EV/Gross Profit | Yes | Hardware margins vary widely |

**Key operating metrics to compare**: Gross margin, backlog, capacity utilization, R&D as % of revenue

### Cross-Border Payments / Remittance
| Multiple | Primary | Why It Matters |
|----------|---------|----------------|
| EV/Revenue (NTM) | Yes | Standard, but compare at similar revenue yields |
| EV/Gross Profit | Yes | **Critical** — normalizes for vastly different yield structures |
| EV/TPV | Secondary | Scale comparison, but misleading across yield tiers |
| P/E | Secondary | For profitable payments companies (Wise, WU) |
| EV/EBITDA | Secondary | For mature, profitable operators |

**Key operating metrics to compare**: TPV growth, revenue yield (bps), gross profit yield (bps), gross margin, corridors at scale, LTV/CAC, retention curves, FTE efficiency

**Key public comps**: Wise (WISE.L), Remitly (RELY), Flywire (FLYW), dLocal (DLO), Payoneer (PAYO), Western Union (WU), MoneyGram, Corpay (CPAY), Euronet (EEFT)

**Important nuances**:
- Revenue yield varies 10x+ between consumer remittance (~200-250bps) and B2B payments (~20-70bps) — never compare across yield tiers without GP normalization
- Gross profit growth is more meaningful than revenue growth for yield-compression businesses
- Scheme incentive revenue should be separated and evaluated for durability
- Infrastructure plays (proprietary rails, principal membership) command premium multiples vs. aggregator models

### Consumer / D2C
| Multiple | Primary | Why It Matters |
|----------|---------|----------------|
| EV/Revenue (NTM) | Yes | Standard |
| P/S | Yes | Simpler for consumer brands |
| EV/EBITDA | Yes | Profitability focus |
| P/E | Secondary | For mature consumer companies |

**Key operating metrics to compare**: Customer acquisition cost, repeat purchase rate, LTV, brand NPS

## Private Company Discount Framework

### Base Discount Range: 20-40%

Apply adjustments from the base based on these factors:

| Factor | Narrower Discount (toward 20%) | Wider Discount (toward 40%+) |
|--------|-------------------------------|------------------------------|
| IPO timeline | < 12 months | > 36 months or unclear |
| Revenue scale | > $500M ARR | < $50M ARR |
| Profitability | FCF positive | High burn, long path to profit |
| Market conditions | Hot IPO market | Cold/risk-off market |
| Data transparency | Audited financials | Self-reported, limited data |
| Governance | Independent board, clean structure | Founder-controlled, complex cap table |
| Liquidity | Active secondary market | No secondary liquidity |
| Growth rate | Significantly above public comps | In-line or below public comps |

### Discount Calculation

```
Implied EV = (Peer Median Multiple) x (Target Metric) x (1 - Private Discount %)
```

**Example:**
- Peer median EV/NTM Revenue = 12x
- Target NTM Revenue = $200M
- Private discount = 30%
- Implied EV = 12 x $200M x (1 - 0.30) = $1,680M

### Growth-Adjusted Multiples

When growth rates differ significantly between target and comps:

```
Growth-Adjusted Multiple = EV/Revenue / Revenue Growth Rate
```

This normalizes valuation per unit of growth. A lower growth-adjusted multiple suggests the company is cheaper relative to its growth.

## Comp Table Template

| Company | Ticker | Mkt Cap ($B) | EV ($B) | Rev NTM ($M) | Rev Growth YoY | Gross Margin | EBITDA Margin | FCF Margin | EV/Rev NTM | EV/GP | EV/EBITDA | Rule of 40 | NRR |
|---------|--------|-------------|---------|---------------|-----------------|--------------|---------------|------------|------------|-------|-----------|------------|-----|
| Comp 1 | | | | | | | | | | | | | |
| Comp 2 | | | | | | | | | | | | | |
| ... | | | | | | | | | | | | | |
| **Median** | | | | | | | | | | | | | |
| **Mean** | | | | | | | | | | | | | |
| **25th %** | | | | | | | | | | | | | |
| **75th %** | | | | | | | | | | | | | |

## Implied Valuation Summary

| Methodology | Multiple Used | Target Metric | Raw Implied EV | Private Discount | Adjusted Implied EV |
|-------------|-------------|---------------|----------------|------------------|---------------------|
| Median EV/Revenue | | | | | |
| Median EV/Gross Profit | | | | | |
| Growth-Adjusted | | | | | |
| 25th Percentile (Bear) | | | | | |
| 75th Percentile (Bull) | | | | | |
| **Blended Implied EV** | | | | | |

## Common Pitfalls

1. **Comparing apples to oranges**: A 20%-growth SaaS company should not be comped against 60%-growth peers without adjustment
2. **Ignoring margin differences**: EV/Revenue is misleading when gross margins differ by 30+ points; use EV/Gross Profit instead
3. **Stale multiples**: Public multiples move daily; always note the date of the data pull
4. **Survivorship bias**: Don't only pick the best-performing public comps
5. **Over-weighting one multiple**: Triangulate across at least 3 different multiples
6. **Ignoring balance sheet**: EV-based multiples account for debt/cash; equity multiples don't
7. **Applying uniform discounts**: Adjust the private discount for company-specific factors, not a flat 30%

## Data Sources

For live public multiples data, use any of these sources (user must provide access):
- Financial data terminals (Bloomberg, Capital IQ, FactSet, Koyfin)
- Free sources: Yahoo Finance, Google Finance, Finviz, macrotrends.net
- SaaS-specific: Meritech Capital SaaS Index, Jamin Ball's Clouded Judgement
- Marketplace-specific: a16z marketplace benchmarks
- General: Damodaran's sector data (NYU Stern)
