# Secondary Platform Selectors & Search Flows

Reference for `scripts/fetch_secondary_prices.sh`. Describes how to search for any company on each platform and extract the current price.

## Forge Global (forgeglobal.com)

### Auth
- **No login required** — prices are public

### Navigation (search by slug)
- Try direct URL: `https://forgeglobal.com/{slug}_stock/` where slug = lowercase company name
- Common slug patterns: `spacex`, `revolut`, `bytedance`, `cerebras`, `kraken`
- If 404 → try without hyphens → if still 404 → company not on Forge, record "n/a"

### Price Extraction
- Label: `link "Forge Price"`
- Price: `StaticText "$102.62 "` following the Forge Price link
- Regex on snapshot: `grep -A6 'link "Forge Price"' | grep 'StaticText "\$[0-9]'`
- If price shows `$--` → not yet available, record "n/a"

---

## Caplight (platform.caplight.com)

### Auth Check
- Logged in if snapshot contains `denis.dikarev`
- If not logged in → inform user to re-login in Chrome debug profile

### Search Flow
1. Navigate to `https://platform.caplight.com/market`
2. Press `Control+k` to open search modal
3. Modal contains: `textbox "Search for a Company or Investor"` inside a `dialog`
4. Type company name → results appear as links
5. Click link matching company name → navigates to company page

### Price Extraction
- Label: `StaticText "Caplight MarketPrice™"`
- Price: next `StaticText` starting with `$` (e.g., `StaticText "$97.18"`)
- Regex on snapshot: `grep -A2 'Caplight MarketPrice' | grep 'StaticText "\$'`

---

## Hiive (app.hiive.com)

### Auth Check
- Logged in if snapshot contains `combobox "Search company"`
- If not logged in → inform user to re-login in Chrome debug profile

### Search Flow
1. Navigate to `https://app.hiive.com/dashboard`
2. Find and click `combobox "Search company"`
3. Type company name → options appear in `listbox`
4. Click matching `option` → navigates to company page

### Price Extraction
- Label: `StaticText "Hiive Price"` (inside a paragraph)
- Price: `StaticText "$113.00"` in the paragraph following "Hiive Price"
- Regex on snapshot: `grep -A4 '"Hiive Price"' | grep 'StaticText "\$'`

---

## Prerequisites

- `agent-browser` CLI installed (`npm i -g agent-browser`)
- Chrome debug profile at `~/.chrome-debug` with Caplight + Hiive sessions active
- Launch Chrome before running: `"/c/Program Files/Google/Chrome/Application/chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\\Users\\denis\\.chrome-debug" --profile-directory="Default" &`
- Connect agent-browser: `agent-browser connect 9222`
