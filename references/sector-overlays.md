# Sector-Specific Analysis Overlays

These overlays extend the core analysis framework with sector-specific metrics, questions, and benchmarks. Apply the relevant overlay based on the company's primary sector.

**Load only the matching sector section** — do not read all overlays.

## Table of Contents

- [SaaS / Cloud Software](#saas--cloud-software)
- [Cross-Border Payments / Remittance](#cross-border-payments--remittance)
- [Fintech](#fintech)
- [Medtech / Biotech](#medtech--biotech)
- [AI / ML](#ai--ml)
- [Infrastructure / Industrials](#infrastructure--industrials)
- [Semiconductors / Chips](#semiconductors--chips)
- [Marketplace / Platform](#marketplace--platform)
- [Consumer / D2C](#consumer--d2c)

---

## SaaS / Cloud Software

### Additional Financial Metrics
- Net Revenue Retention (NRR) — benchmark: >120% best-in-class, >110% good, <100% concerning
- Gross Revenue Retention (GRR) — benchmark: >90% good, <85% concerning
- Magic Number — benchmark: >1.0 efficient, 0.5-1.0 acceptable, <0.5 inefficient
- CAC Payback Period — benchmark: <18 months good, <12 months excellent
- Gross margin — benchmark: >75% strong, 65-75% acceptable, <65% investigate
- DBNER (Dollar-Based Net Expansion Rate) by cohort vintage
- Annual contract value (ACV) distribution
- Billings vs. revenue growth differential

### Additional DD Questions
- What % of revenue is truly recurring (annual/multi-year contracts) vs. monthly?
- What is the upsell/cross-sell motion? Land-and-expand evidence?
- Professional services as % of revenue (lower is better for margins)?
- Free-to-paid conversion rate (if PLG model)?
- Average contract length and renewal timing concentration?
- Multi-product vs. single-product? Attach rate for additional products?

### Comp Considerations
- Primary multiples: EV/ARR, EV/NTM Revenue, EV/Gross Profit
- Key differentiator: NRR-adjusted multiples (high-NRR SaaS trades at premium)
- Rule of 40 is the standard efficiency benchmark

---

## Cross-Border Payments / Remittance

### Additional Financial Metrics
- **TPV (Total Payment Volume)** — THE primary scale metric, not ARR
- **Revenue Yield** (bps) — revenue as % of volume, by segment (Consumer vs Enterprise)
- **Buy Rate** (bps) — cost of sales as % of volume (pay-in + pay-out + FX costs)
- **Gross Profit Yield** (bps) — GP as % of volume
- **OPN / Infrastructure Efficiency** — cost savings from proprietary settlement rails vs. correspondent banking
- **Scheme Incentives** — revenue from card network performance incentives (Visa, Mastercard)
- **Corridor-level economics** — volume, revenue, revenue yield, buy rate, GP, active customers per corridor
- **Number of corridors at scale** (e.g., >$1m monthly volume) — network density metric
- **Pay-in partner mix** — % by Visa, Mastercard, APMs, banks, crypto
- **Pay-out partner mix** — % by Visa, Mastercard, banks, wallets, IPS, stablecoins
- **Average volume per customer** (Consumer) and **average volume per client** (Enterprise)
- **Average revenue per customer/client** by segment
- **FTE efficiency** — revenue per FTE (benchmark: $300k-$500k+ for scaled payments companies)
- **LTV/CAC** — Consumer LTV vs. acquisition cost (benchmark: >3x good, >5x excellent)
- **Number of delivery endpoints** — cards, bank accounts, wallets, mobile, IPS
- **Settlement speed** — real-time vs. T+1 vs. T+2/3 and trend
- **Run rate metrics** — quarterly x 4 annualization (standard in payments)
- **Consumer active customers** — monthly active transacting users (not just registered)
- **Enterprise client count** and client retention rate

### Sub-Segment Decomposition
Consumer and Enterprise segments should each be further broken down:

**Consumer:**
- **Traditional/Current Markets** — established corridors with market share (highest margins, lowest growth)
- **Expansion/Priority Markets** — high-growth receiving markets being actively scaled (lower margins, higher growth)
- **New Sending Markets** — newly launched origination countries (lowest volume, highest growth potential)

**Enterprise:**
- **Existing API** — mature API integration clients (stable, predictable volume)
- **New API / ISA / Embed** — new products (Instant Settlement Accounts, embedded payments)
- **Web Platform / Legacy** — legacy product, winding down

For each sub-segment, track: customers/clients, volume, revenue, revenue yield, buy rate, GP, GP yield, GP margin

### Bridge Analysis Framework
- **Volume bridge**: Current quarter RR → Consumer growth (by sub-segment) → Enterprise growth (by sub-segment) → Next quarter RR
- **Revenue bridge**: Volume growth → Revenue yield change → Total revenue change
- **Gross profit bridge**: Revenue growth → Buy rate change → OPN efficiency → Total GP change
- **Revenue yield bridge**: Segment mix shift → Corridor mix shift → Pricing changes → Net yield change

### Cohort Analysis (Consumer)
- Monthly acquisition cohorts tracked over 24+ months
- Three views: **Calendarised** (absolute active users), **Indexed** (relative to cohort size), **Retention** (% still active)
- Key benchmarks: M1 retention ~50%, M6 ~30-35%, M12 ~25-30%, M24 ~20%
- Seasonal patterns: higher retention in established corridors, lower in expansion markets
- Volume-weighted retention (not just logo retention)

### Additional DD Questions
- What EMI (Electronic Money Institution) licenses does the company hold? In which jurisdictions?
- Principal membership or sponsor bank model for Visa/Mastercard?
- What is the settlement model? Pre-funding requirements? Liquidity tied up in operations?
- Safeguarding obligations for e-money — how are customer funds protected?
- Corridor concentration: what % of volume comes from top 3 corridors?
- Sending market concentration vs. receiving market concentration?
- Scheme incentive contracts: duration, renewal risk, volume targets?
- OPN (proprietary rails) rollout status — how many countries live? Cost saving per transaction?
- Stablecoin settlement capabilities — regulatory status, volume, partner banks?
- FX risk management — hedging strategy, open position limits?
- Correspondent bank dependencies — how many, single-source risk?
- Pay-out partner redundancy — can you route around a partner failure?
- Sanctions and compliance risk in CIS/Central Asian corridors?
- Competitive positioning vs. Wise, Remitly, WorldRemit, Western Union, MoneyGram?
- Media-for-equity deals — how are marketing credits valued and amortized?

### Risk Weight Adjustments
- Regulatory Risk weight: increase to 20% (cross-border payments are heavily regulated)
- Market Risk (geopolitical, sanctions, corridor disruption): increase to 20%
- Competition Risk: keep at 15%
- Financial Risk: keep at 15%
- Execution Risk: 10%
- Technology Risk: 10%
- Key-Person Risk: 5%
- Valuation Risk: 5%

### Comp Considerations
- Primary multiples: EV/Revenue, EV/Gross Profit (margins vary widely)
- **Revenue yield matters**: compare companies at similar yield levels (high-yield remittance vs. low-yield B2B)
- Segment by: consumer remittance vs. B2B cross-border vs. infrastructure/rails
- Key public comps: Wise (WISE.L), Remitly (RELY), Flywire (FLYW), dLocal (DLO), Payoneer (PAYO), MoneyGram, Western Union
- For infrastructure plays: Visa, Mastercard, SWIFT network comparisons
- **TPV growth rate** is the primary growth metric, not revenue growth alone
- **Gross profit growth** is often more meaningful than revenue growth (captures yield dynamics)
- Rule of 40 using GP growth + FCF margin (not revenue growth)

---

## Fintech

### Additional Financial Metrics
- Take rate / interchange spread / net interest margin (depending on model)
- Transaction volume and growth
- Loss rate / default rate / charge-off rate (for lending)
- Gross payment volume (GPV) for payments companies
- Cost of funds and funding diversification
- Regulatory capital ratios (if applicable)
- Fraud rate and fraud loss as % of volume
- Average revenue per user (ARPU) by segment

### Additional DD Questions
- What licenses and regulatory approvals does the company hold? In which jurisdictions?
- Banking partner dependencies? Sponsor bank relationships?
- What happens if a key banking partner terminates?
- Credit risk: who holds the risk? Is it balance sheet or off-balance-sheet?
- What is the path to a banking charter (if relevant)?
- Money transmission licenses: which states/countries?
- AML/KYC compliance infrastructure — in-house or third-party?
- How does the company make money in a rising vs. falling rate environment?
- Embedded finance or BaaS dependencies?
- PCI compliance status?

### Risk Weight Adjustments
- Regulatory Risk weight: increase to 20% (from 10%)
- Technology Risk weight: decrease to 5%
- Rebalance remaining weights proportionally

### Comp Considerations
- Primary multiples: EV/Revenue, P/E (profitability matters more in fintech)
- Segment carefully: payments vs. lending vs. insurance vs. neobank vs. infrastructure
- Lending fintechs often trade on P/Book or P/Tangible Book as secondary metric

---

## Medtech / Biotech

### Additional Financial Metrics
- Clinical pipeline breakdown by phase (Phase I, II, III, approved)
- R&D spend as % of revenue (or total spend if pre-revenue)
- Probability-adjusted pipeline value (rNPV)
- Reimbursement revenue vs. out-of-pocket revenue
- Gross margin by product line
- Patent expiry timeline and IP cliff dates
- Regulatory milestone timeline and associated costs

### Additional DD Questions
- FDA pathway: 510(k), PMA, De Novo, breakthrough designation?
- Current regulatory status for each product?
- Clinical trial status, enrollment progress, endpoint design?
- Reimbursement strategy: CPT codes, payer coverage, ASP?
- Manufacturing: in-house or CMO/CDMO? GMP compliance?
- Key opinion leader (KOL) endorsements and advisory board?
- IP landscape: freedom-to-operate analysis done? Patent challenges?
- Competitive clinical data comparison?
- Post-market surveillance obligations?
- International regulatory strategy (CE mark, PMDA, NMPA)?

### Risk Weight Adjustments
- Regulatory Risk weight: increase to 25% (from 10%)
- Technology Risk (clinical/scientific risk): increase to 15%
- Financial Risk: adjust based on whether pre-revenue or post-revenue
- Rebalance remaining weights proportionally

### Comp Considerations
- Pre-revenue: value on rNPV (risk-adjusted net present value) of pipeline
- Post-revenue: EV/Revenue, but segment by medtech vs. pharma vs. diagnostics
- Peak sales estimates are critical — what is the market opportunity per indication?
- Often valued on EV/Peak Revenue or EV/pipeline-adjusted revenue

---

## AI / ML

### Additional Financial Metrics
- Compute costs as % of revenue (and trend)
- Inference cost per query/transaction
- GPU/TPU spend and committed capacity
- Training cost per model iteration
- Gross margin excluding compute (software-like margin)
- Data acquisition and licensing costs
- API call volume and pricing per unit

### Additional DD Questions
- Model defensibility: proprietary data, fine-tuning, architecture advantage?
- Build vs. buy risk: can a foundation model provider replicate this?
- Dependency on third-party models (OpenAI, Anthropic, Google)? Switching cost?
- Data moat: proprietary training data? Flywheel effects?
- Inference economics: cost trajectory as model scales?
- Customer lock-in: is value in the model or the workflow integration?
- Talent concentration: how many key ML engineers? Retention risk?
- Regulatory exposure: AI governance, EU AI Act, sector-specific AI rules?
- Hallucination/accuracy risk for the specific use case?
- Open-source competitive threat?

### Risk Weight Adjustments
- Technology Risk weight: increase to 20% (from 10%)
- Competition Risk weight: increase to 20% (from 15%)
- Reduce Market Risk and Key-Person Risk by 5% each to compensate

### Comp Considerations
- No clean public comp set yet — use blended SaaS + platform comps
- Distinguish: AI-native company vs. AI feature added to existing product
- Growth premium is high but scrutinize compute-adjusted margins
- Watch for "AI washing" — is AI genuinely core or a marketing overlay?

---

## Infrastructure / Industrials

### Additional Financial Metrics
- Contract backlog and book-to-bill ratio
- CapEx as % of revenue and CapEx intensity trend
- Capacity utilization rate
- ROIC (Return on Invested Capital)
- Maintenance CapEx vs. growth CapEx split
- Average contract duration and visibility into future revenue
- Working capital intensity

### Additional DD Questions
- Government contract exposure: what % of revenue? Concentration risk?
- Contract type: fixed-price, cost-plus, time-and-materials?
- Supply chain dependencies and single-source risks?
- Permitting and regulatory approval timelines?
- Labor availability and workforce concentration?
- Cyclicality: how does this business perform in a downturn?
- Physical asset condition and maintenance obligations?
- Environmental liabilities and remediation costs?
- Defense/classified work: clearance requirements and limitations?

### Risk Weight Adjustments
- Execution Risk weight: increase to 20% (from 15%)
- Regulatory Risk weight: increase to 15% (from 10%)
- Technology Risk weight: decrease to 5%
- Rebalance remaining weights proportionally

### Comp Considerations
- Primary multiples: EV/EBITDA (capital-intensive, profitability matters)
- EV/Revenue as secondary, but margins vary wildly in this sector
- Backlog-adjusted multiples: EV / (Revenue + Backlog) for visibility premium
- Segment carefully: defense vs. commercial vs. energy vs. transport

---

## Semiconductors / Chips

### Additional Financial Metrics
- Design win pipeline and conversion rate
- ASP (Average Selling Price) trends
- Wafer cost and yield rates (if fabless: foundry partner economics)
- Inventory-to-revenue ratio and days of inventory
- R&D as % of revenue (benchmark: 15-25% typical)
- Gross margin by product line (benchmark: >50% for fabless, >40% for IDM)
- Customer concentration by end-market (data center, auto, mobile, IoT)

### Additional DD Questions
- Fabless or IDM? If fabless, foundry dependencies (TSMC, Samsung, GlobalFoundries)?
- Process node roadmap and access to leading-edge nodes?
- Design win visibility: how far out can you see revenue?
- End-market diversification: how exposed to any single cycle (mobile, auto, PC)?
- IP portfolio: key patents, licensing revenue, freedom-to-operate?
- Export control and sanctions exposure (US-China, ITAR)?
- EDA tool and IP block dependencies?
- Competitive positioning vs. Nvidia, AMD, Intel, Qualcomm, Broadcom (as relevant)?
- Custom silicon threat from hyperscalers (Google TPU, Amazon Graviton, etc.)?
- Packaging technology: advanced packaging capabilities (chiplet, CoWoS)?

### Risk Weight Adjustments
- Technology Risk weight: increase to 20% (from 10%)
- Market Risk (cyclicality): increase to 20% (from 15%)
- Regulatory Risk (export controls): increase to 15%
- Reduce Key-Person Risk and Execution Risk by 5% each

### Comp Considerations
- Primary multiples: EV/Revenue, EV/EBITDA, P/E
- Segment: fabless vs. IDM vs. EDA vs. IP licensing vs. equipment
- Cyclicality adjustment: use mid-cycle margins, not peak or trough
- Growth-adjusted P/E (PEG ratio) is meaningful for this sector

---

## Marketplace / Platform

### Additional Financial Metrics
- GMV (Gross Merchandise Volume) and GMV growth
- Take rate (net revenue / GMV) and take rate trend
- Supply-side and demand-side unit economics separately
- Buyer-to-seller ratio and liquidity metrics
- Average order value (AOV) and frequency
- Contribution margin per transaction
- Supply acquisition cost vs. demand acquisition cost

### Additional DD Questions
- Which side of the marketplace is harder to acquire? (This is the side to protect)
- Multi-homing risk: do users use competing platforms simultaneously?
- Disintermediation risk: can buyers and sellers bypass the platform after matching?
- Geographic density requirements: is this a local, regional, or global network?
- Managed vs. unmanaged marketplace? What does the platform control?
- Trust and safety investment: fraud, disputes, quality control?
- Regulatory classification: is the platform an employer, broker, or neutral intermediary?
- Network effects: cross-side, same-side, or both? Evidence of strength?

### Risk Weight Adjustments
- Competition Risk weight: increase to 20% (from 15%)
- Market Risk weight: increase to 20% (disintermediation, multi-homing)
- Reduce Regulatory Risk and Technology Risk by 5% each

### Comp Considerations
- Primary multiples: EV/Revenue (on net revenue), EV/Gross Profit
- GMV-based multiples as secondary (EV/GMV)
- Take rate normalization: compare companies at equivalent take rates
- Maturity matters: early-stage marketplaces invest in liquidity (low margins); mature ones harvest

---

## Consumer / D2C

### Additional Financial Metrics
- Repeat purchase rate and purchase frequency
- Customer lifetime value by acquisition cohort
- CAC by channel (paid social, organic, influencer, retail, etc.)
- Blended vs. marginal CAC trend
- Average order value (AOV) and basket size
- Return rate and net revenue after returns
- Brand awareness and NPS scores
- Retail distribution points (if omnichannel)
- Inventory turnover and sell-through rate

### Additional DD Questions
- Channel mix: what % DTC vs. wholesale vs. retail vs. marketplace (Amazon)?
- Brand defensibility: is this a commodity product with a brand or a genuine moat?
- Supply chain: manufacturing origin, lead times, single-source dependencies?
- Customer acquisition: how dependent on paid social (Meta, Google)? CAC trajectory?
- Influencer/celebrity dependency: is growth tied to a single personality?
- Subscription component: is there recurring revenue or is each sale a re-acquisition?
- Amazon risk: what happens if Amazon launches a competitive private label?
- Tariff and import duty exposure?
- Sustainability and ESG requirements from retail partners?

### Risk Weight Adjustments
- Competition Risk weight: increase to 20% (low barriers in consumer)
- Market Risk weight: increase to 20% (consumer sentiment, discretionary spend)
- Reduce Technology Risk to 5%
- Rebalance remaining weights proportionally

### Comp Considerations
- Primary multiples: EV/Revenue, EV/EBITDA, P/E
- Segment: beauty vs. food vs. apparel vs. wellness vs. pet vs. home
- Growth premium for DTC brands but discount for high CAC dependency
- Profitability inflection is a major valuation driver in consumer
