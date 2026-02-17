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
