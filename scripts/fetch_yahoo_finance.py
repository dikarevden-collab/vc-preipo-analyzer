#!/usr/bin/env python3
"""Fetch structured financial data from Yahoo Finance using yfinance.

Usage:
    python scripts/fetch_yahoo_finance.py TICKER [TICKER2 ...] [--format json|table]

Examples:
    python scripts/fetch_yahoo_finance.py WISE.L RELY PAYONEER DLO FLYW WU
    python scripts/fetch_yahoo_finance.py WISE.L --format json

Output includes: market cap, enterprise value, EV/Revenue, EV/EBITDA, EV/Gross Profit,
P/E, revenue, revenue growth, gross margin, EBITDA margin, FCF margin, Rule of 40.

Requires: pip install yfinance
"""

import sys
import json
import argparse

try:
    import yfinance as yf
except ImportError:
    print("ERROR: yfinance not installed. Run: pip install yfinance", file=sys.stderr)
    sys.exit(1)


def fetch_ticker_data(ticker_symbol: str) -> dict:
    """Fetch key financial metrics for a single ticker."""
    t = yf.Ticker(ticker_symbol)
    info = t.info

    # Basic identifiers
    name = info.get("shortName") or info.get("longName") or ticker_symbol
    market_cap = info.get("marketCap")
    enterprise_value = info.get("enterpriseValue")

    # Multiples
    ev_revenue = info.get("enterpriseToRevenue")
    ev_ebitda = info.get("enterpriseToEbitda")
    trailing_pe = info.get("trailingPE")
    forward_pe = info.get("forwardPE")
    price_to_sales = info.get("priceToSalesTrailing12Months")

    # Revenue and growth
    total_revenue = info.get("totalRevenue")
    revenue_growth = info.get("revenueGrowth")  # YoY as decimal

    # Margins
    gross_margin = info.get("grossMargins")
    ebitda_margin = info.get("ebitdaMargins")
    operating_margin = info.get("operatingMargins")
    profit_margin = info.get("profitMargins")

    # Cash flow
    free_cash_flow = info.get("freeCashflow")
    operating_cash_flow = info.get("operatingCashflow")

    # Computed metrics
    fcf_margin = None
    if free_cash_flow and total_revenue and total_revenue > 0:
        fcf_margin = free_cash_flow / total_revenue

    rule_of_40 = None
    if revenue_growth is not None and fcf_margin is not None:
        rule_of_40 = (revenue_growth * 100) + (fcf_margin * 100)

    ev_gross_profit = None
    if enterprise_value and total_revenue and gross_margin:
        gross_profit = total_revenue * gross_margin
        if gross_profit > 0:
            ev_gross_profit = enterprise_value / gross_profit

    # NRR not available from Yahoo Finance — mark as N/A
    return {
        "ticker": ticker_symbol,
        "name": name,
        "market_cap_B": round(market_cap / 1e9, 2) if market_cap else None,
        "enterprise_value_B": round(enterprise_value / 1e9, 2) if enterprise_value else None,
        "ev_revenue_ttm": round(ev_revenue, 2) if ev_revenue else None,
        "ev_ebitda_ttm": round(ev_ebitda, 2) if ev_ebitda else None,
        "ev_gross_profit": round(ev_gross_profit, 2) if ev_gross_profit else None,
        "trailing_pe": round(trailing_pe, 2) if trailing_pe else None,
        "forward_pe": round(forward_pe, 2) if forward_pe else None,
        "price_to_sales": round(price_to_sales, 2) if price_to_sales else None,
        "total_revenue_M": round(total_revenue / 1e6, 1) if total_revenue else None,
        "revenue_growth_pct": round(revenue_growth * 100, 1) if revenue_growth is not None else None,
        "gross_margin_pct": round(gross_margin * 100, 1) if gross_margin is not None else None,
        "ebitda_margin_pct": round(ebitda_margin * 100, 1) if ebitda_margin is not None else None,
        "operating_margin_pct": round(operating_margin * 100, 1) if operating_margin is not None else None,
        "fcf_margin_pct": round(fcf_margin * 100, 1) if fcf_margin is not None else None,
        "rule_of_40": round(rule_of_40, 1) if rule_of_40 is not None else None,
    }


def validate_ticker(data: dict) -> list[str]:
    """Cross-check fetched multiples for internal consistency. Returns list of warnings."""
    warnings = []
    ticker = data.get("ticker", "?")

    # 1. EV/Revenue vs Price/Sales should be in the same ballpark
    ev_rev = data.get("ev_revenue_ttm")
    ps = data.get("price_to_sales")
    if ev_rev and ps and ps > 0:
        ratio = ev_rev / ps
        if ratio > 2.0 or ratio < 0.5:
            warnings.append(f"{ticker}: EV/Rev ({ev_rev}) vs P/S ({ps}) diverge by {ratio:.1f}x — check debt/cash")

    # 2. EV/GP should be >= EV/Revenue (since GP <= Revenue)
    ev_gp = data.get("ev_gross_profit")
    if ev_rev and ev_gp and ev_rev > 0 and ev_gp < ev_rev * 0.95:
        warnings.append(f"{ticker}: EV/GP ({ev_gp}) < EV/Rev ({ev_rev}) — impossible, data inconsistency")

    # 3. Gross margin sanity (should be 0-100%)
    gm = data.get("gross_margin_pct")
    if gm is not None and (gm < 0 or gm > 100):
        warnings.append(f"{ticker}: Gross margin {gm}% outside 0-100% range")

    # 4. EV/GP cross-check against EV/Rev / Gross Margin
    if ev_rev and gm and gm > 0:
        expected_ev_gp = round(ev_rev / (gm / 100), 2)
        if ev_gp and abs(ev_gp - expected_ev_gp) / max(ev_gp, expected_ev_gp) > 0.15:
            warnings.append(f"{ticker}: EV/GP ({ev_gp}) vs computed EV/Rev÷GM ({expected_ev_gp}) — {abs(ev_gp - expected_ev_gp)/max(ev_gp, expected_ev_gp)*100:.0f}% drift")

    # 5. Negative multiples (distressed or data error)
    if ev_rev is not None and ev_rev < 0:
        warnings.append(f"{ticker}: Negative EV/Revenue ({ev_rev}) — likely negative EV (cash > mkt cap + debt)")
    ev_ebitda = data.get("ev_ebitda_ttm")
    if ev_ebitda is not None and ev_ebitda < 0:
        warnings.append(f"{ticker}: Negative EV/EBITDA ({ev_ebitda}) — negative EBITDA or negative EV")

    # 6. Extreme outlier multiples
    if ev_rev is not None and ev_rev > 50:
        warnings.append(f"{ticker}: EV/Revenue ({ev_rev}x) extremely high — verify")
    if ev_ebitda is not None and ev_ebitda > 100:
        warnings.append(f"{ticker}: EV/EBITDA ({ev_ebitda}x) extremely high — verify")
    if data.get("trailing_pe") is not None and data["trailing_pe"] > 200:
        warnings.append(f"{ticker}: P/E ({data['trailing_pe']}x) extremely high — verify")

    # 7. Missing critical fields
    missing = []
    for key, label in [("market_cap_B", "market cap"), ("ev_revenue_ttm", "EV/Revenue"),
                        ("total_revenue_M", "revenue"), ("gross_margin_pct", "gross margin")]:
        if data.get(key) is None:
            missing.append(label)
    if missing:
        warnings.append(f"{ticker}: Missing critical data — {', '.join(missing)}")

    # 8. Revenue growth sanity
    rg = data.get("revenue_growth_pct")
    if rg is not None and (rg > 500 or rg < -90):
        warnings.append(f"{ticker}: Revenue growth {rg}% looks extreme — verify")

    return warnings


def validate_peer_set(results: list[dict]) -> list[str]:
    """Cross-validate multiples across the peer set. Flag outliers beyond 2x IQR."""
    warnings = []
    valid = [r for r in results if r.get("error") is None]
    if len(valid) < 3:
        return warnings

    for key, label in [("ev_revenue_ttm", "EV/Revenue"), ("ev_ebitda_ttm", "EV/EBITDA"),
                        ("gross_margin_pct", "Gross Margin %"), ("revenue_growth_pct", "Rev Growth %")]:
        values = [(r["ticker"], r[key]) for r in valid if r.get(key) is not None]
        if len(values) < 3:
            continue
        nums = sorted([v for _, v in values])
        q1_idx = len(nums) // 4
        q3_idx = 3 * len(nums) // 4
        q1 = nums[q1_idx]
        q3 = nums[q3_idx]
        iqr = q3 - q1
        if iqr == 0:
            continue
        lower = q1 - 2 * iqr
        upper = q3 + 2 * iqr
        for ticker, val in values:
            if val < lower or val > upper:
                warnings.append(f"{ticker}: {label} ({val}) is a peer-set outlier (IQR range: {round(lower, 1)}–{round(upper, 1)})")

    return warnings


def format_table(results: list[dict]) -> str:
    """Format results as a markdown table."""
    headers = [
        "Ticker", "Name", "Mkt Cap ($B)", "EV ($B)", "EV/Rev", "EV/EBITDA",
        "EV/GP", "P/E (TTM)", "Rev ($M)", "Rev Growth %", "Gross Margin %",
        "EBITDA Margin %", "FCF Margin %", "Rule of 40"
    ]
    keys = [
        "ticker", "name", "market_cap_B", "enterprise_value_B", "ev_revenue_ttm",
        "ev_ebitda_ttm", "ev_gross_profit", "trailing_pe", "total_revenue_M",
        "revenue_growth_pct", "gross_margin_pct", "ebitda_margin_pct",
        "fcf_margin_pct", "rule_of_40"
    ]

    rows = []
    rows.append("| " + " | ".join(headers) + " |")
    rows.append("| " + " | ".join(["---"] * len(headers)) + " |")

    for r in results:
        vals = []
        for k in keys:
            v = r.get(k)
            vals.append(str(v) if v is not None else "N/A")
        rows.append("| " + " | ".join(vals) + " |")

    # Add median row
    numeric_keys = keys[2:]  # skip ticker and name
    medians = ["**Median**", ""]
    for k in numeric_keys:
        values = [r[k] for r in results if r.get(k) is not None]
        if values:
            values.sort()
            mid = len(values) // 2
            median = values[mid] if len(values) % 2 == 1 else round((values[mid - 1] + values[mid]) / 2, 2)
            medians.append(str(median))
        else:
            medians.append("N/A")
    rows.append("| " + " | ".join(medians) + " |")

    return "\n".join(rows)


def main():
    parser = argparse.ArgumentParser(description="Fetch Yahoo Finance data for public comps")
    parser.add_argument("tickers", nargs="+", help="Ticker symbols (e.g., WISE.L RELY DLO)")
    parser.add_argument("--format", choices=["json", "table"], default="table",
                        help="Output format (default: table)")
    args = parser.parse_args()

    results = []
    for ticker in args.tickers:
        try:
            data = fetch_ticker_data(ticker)
            results.append(data)
            print(f"  Fetched: {ticker} — {data['name']}", file=sys.stderr)
        except Exception as e:
            print(f"  ERROR fetching {ticker}: {e}", file=sys.stderr)
            results.append({"ticker": ticker, "name": "ERROR", "error": str(e)})

    if args.format == "json":
        print(json.dumps(results, indent=2))
    else:
        print(format_table(results))

    print(f"\nSource: Yahoo Finance (finance.yahoo.com) via yfinance — accessed {__import__('datetime').date.today()}", file=sys.stderr)


if __name__ == "__main__":
    main()
