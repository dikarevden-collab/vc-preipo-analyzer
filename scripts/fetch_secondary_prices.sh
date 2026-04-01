#!/bin/bash
# Single-company secondary pricing scraper for vc-preipo-analyzer
# Uses agent-browser to search Forge, Caplight, and Hiive for a given company
# Usage: bash fetch_secondary_prices.sh "Company Name"
# Requires: agent-browser connected to Chrome debug profile on port 9222
# Output: JSON to stdout with prices from each platform

set +e  # Don't abort on individual command failures

COMPANY="$1"
if [ -z "$COMPANY" ]; then
  echo '{"error": "Usage: fetch_secondary_prices.sh \"Company Name\""}' >&2
  exit 1
fi

SLUG=$(echo "$COMPANY" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | sed 's/[^a-z0-9-]//g')
RESULTS_FILE=$(mktemp)
echo '{}' > "$RESULTS_FILE"

# Helper: random delay between min and max seconds
delay() {
  local min=${1:-2} max=${2:-5}
  sleep $(( RANDOM % (max - min + 1) + min ))
}

# Helper: save result to JSON
save_result() {
  local platform="$1" price="$2" url="$3"
  python -c "
import json, sys
with open(r'$RESULTS_FILE','r') as f: d=json.load(f)
d['$platform'] = {'price': '$price', 'url': '$url'}
with open(r'$RESULTS_FILE','w') as f: json.dump(d,f,indent=2)
"
}

# Check agent-browser is available
if ! command -v agent-browser &> /dev/null; then
  echo '{"error": "agent-browser not installed. Run: npm i -g agent-browser"}' >&2
  exit 1
fi

# ========== FORGE (no login, direct URL with slug guess) ==========
echo "=== Forge: $COMPANY ===" >&2
forge_url="https://forgeglobal.com/${SLUG}_stock/"
agent-browser tab new "$forge_url" 2>/dev/null
agent-browser wait --load networkidle 2>/dev/null || sleep 5
delay 2 4

snap=$(agent-browser snapshot 2>/dev/null)
# Check if page exists (not 404)
if echo "$snap" | grep -q 'Forge Price'; then
  forge_price=$(echo "$snap" | grep -A6 'link "Forge Price"' | grep 'StaticText "\$[0-9]' | head -1 | sed 's/.*StaticText "\$\([0-9,\.]*\).*/\1/' | tr -d ',')
  [ -z "$forge_price" ] && forge_price="n/a"
else
  forge_price="n/a"
  # Try without hyphens in slug
  alt_slug=$(echo "$SLUG" | tr -d '-')
  if [ "$alt_slug" != "$SLUG" ]; then
    forge_url="https://forgeglobal.com/${alt_slug}_stock/"
    agent-browser tab close 2>/dev/null
    agent-browser tab new "$forge_url" 2>/dev/null
    agent-browser wait --load networkidle 2>/dev/null || sleep 5
    delay 2 4
    snap=$(agent-browser snapshot 2>/dev/null)
    if echo "$snap" | grep -q 'Forge Price'; then
      forge_price=$(echo "$snap" | grep -A6 'link "Forge Price"' | grep 'StaticText "\$[0-9]' | head -1 | sed 's/.*StaticText "\$\([0-9,\.]*\).*/\1/' | tr -d ',')
      [ -z "$forge_price" ] && forge_price="n/a"
    fi
  fi
fi
echo "Forge: \$$forge_price" >&2
save_result "forge" "$forge_price" "$forge_url"
agent-browser tab close 2>/dev/null
delay 2 4

# ========== CAPLIGHT (requires login, search by name) ==========
echo "=== Caplight: $COMPANY ===" >&2
agent-browser open "https://platform.caplight.com/market" 2>/dev/null
agent-browser wait --load networkidle 2>/dev/null || sleep 5
delay 3 5

# Auth check
logged_in=$(agent-browser snapshot 2>/dev/null | grep -c "denis.dikarev" || true)
if [ "$logged_in" -eq 0 ]; then
  echo "Caplight: not logged in" >&2
  save_result "caplight" "n/a" "https://platform.caplight.com"
else
  # Open search modal with Ctrl+K
  agent-browser act "press Control+k" 2>/dev/null
  delay 1 2

  # Type company name
  agent-browser act "type \"$COMPANY\"" 2>/dev/null
  delay 2 4

  # Look for matching result in snapshot
  snap=$(agent-browser snapshot 2>/dev/null)
  match_link=$(echo "$snap" | grep -i "$COMPANY" | grep 'link "' | head -1 | sed 's/.*link "\([^"]*\)".*/\1/')

  if [ -n "$match_link" ]; then
    agent-browser act "click \"$match_link\"" 2>/dev/null
    agent-browser wait --load networkidle 2>/dev/null || sleep 5
    delay 3 5

    snap=$(agent-browser snapshot 2>/dev/null)
    cap_price=$(echo "$snap" | grep -A2 'Caplight MarketPrice' | grep 'StaticText "\$' | head -1 | sed 's/.*StaticText "\$\([0-9,\.]*\).*/\1/' | tr -d ',')
    cap_url=$(agent-browser url 2>/dev/null || echo "https://platform.caplight.com")
    [ -z "$cap_price" ] && cap_price="n/a"
  else
    cap_price="n/a"
    cap_url="https://platform.caplight.com"
  fi

  echo "Caplight: \$$cap_price" >&2
  save_result "caplight" "$cap_price" "$cap_url"
fi
delay 2 4

# ========== HIIVE (requires login, search by name) ==========
echo "=== Hiive: $COMPANY ===" >&2
agent-browser open "https://app.hiive.com/dashboard" 2>/dev/null
agent-browser wait --load networkidle 2>/dev/null || sleep 5
delay 3 5

# Auth check
logged_in=$(agent-browser snapshot 2>/dev/null | grep -c 'Search company' || true)
if [ "$logged_in" -eq 0 ]; then
  echo "Hiive: not logged in" >&2
  save_result "hiive" "n/a" "https://app.hiive.com"
else
  # Click search combobox and type
  agent-browser act "click \"Search company\"" 2>/dev/null
  delay 1 2
  agent-browser act "type \"$COMPANY\"" 2>/dev/null
  delay 2 4

  # Look for matching option
  snap=$(agent-browser snapshot 2>/dev/null)
  match_option=$(echo "$snap" | grep -i "$COMPANY" | grep 'option "' | head -1 | sed 's/.*option "\([^"]*\)".*/\1/')

  if [ -n "$match_option" ]; then
    agent-browser act "click \"$match_option\"" 2>/dev/null
    agent-browser wait --load networkidle 2>/dev/null || sleep 5
    delay 3 5

    snap=$(agent-browser snapshot 2>/dev/null)
    hiive_price=$(echo "$snap" | grep -A4 '"Hiive Price"' | grep 'StaticText "\$' | head -1 | sed 's/.*StaticText "\$\([0-9,\.]*\).*/\1/' | tr -d ',')
    hiive_url=$(agent-browser url 2>/dev/null || echo "https://app.hiive.com")
    [ -z "$hiive_price" ] && hiive_price="n/a"
  else
    hiive_price="n/a"
    hiive_url="https://app.hiive.com"
  fi

  echo "Hiive: \$$hiive_price" >&2
  save_result "hiive" "$hiive_price" "$hiive_url"
fi

# ========== Output final JSON to stdout ==========
echo "" >&2
echo "=== Results for $COMPANY ===" >&2
cat "$RESULTS_FILE" >&2

# Add metadata
python -c "
import json, datetime
with open(r'$RESULTS_FILE','r') as f: d=json.load(f)
d['company'] = '$COMPANY'
d['date'] = datetime.date.today().isoformat()
print(json.dumps(d, indent=2))
"

rm -f "$RESULTS_FILE"
