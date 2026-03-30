#!/usr/bin/env bash

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

FAIL=0
HAS_RG=0

if command -v rg >/dev/null 2>&1 && rg --version >/dev/null 2>&1; then
  HAS_RG=1
fi

RED='\033[0;31m'; GREEN='\033[0;32m'; NC='\033[0m'
ok()   { echo -e "${GREEN}  ✓${NC} $*"; }
fail() { echo -e "${RED}  ✗${NC} $*"; FAIL=1; }

require_file() {
  local path="$1"
  if [[ -f "$path" ]]; then
    ok "$path exists"
  else
    fail "$path is missing"
  fi
}

require_text() {
  local file="$1" pattern="$2" label="$3"
  if (( HAS_RG == 1 )); then
    if rg -q --fixed-strings "$pattern" "$file"; then
      ok "$label"
    else
      fail "$label"
    fi
  elif grep -Fq -- "$pattern" "$file"; then
    ok "$label"
  else
    fail "$label"
  fi
}

echo "check-pr-review-packet-layout: validating packet layout docs..."

require_file "docs/architecture/patterns/pr-review-packet-visual-language.md"
require_file "docs/architecture/patterns/pr-review-packet-example.md"
require_file "docs/architecture/diagrams/pr-review-packet-layout.svg"

require_text "docs/architecture/patterns/README.md" "pr-review-packet-visual-language.md" "patterns index links to packet visual language"
require_text "docs/architecture/patterns/README.md" "pr-review-packet-example.md" "patterns index links to packet example"
require_text "docs/architecture/patterns/pr-review-packet-visual-language.md" "## Standard section order" "visual language doc defines standard section order"
require_text "docs/architecture/patterns/pr-review-packet-visual-language.md" "## Table conventions" "visual language doc defines table conventions"
require_text "docs/architecture/patterns/pr-review-packet-visual-language.md" "## Visual guidance" "visual language doc defines visual guidance"
require_text "docs/architecture/patterns/pr-review-packet-visual-language.md" "pr-review-packet-example.md" "visual language doc links to example packet"
require_text "docs/architecture/patterns/pr-review-packet-visual-language.md" "pr-review-packet-layout.svg" "visual language doc links to layout SVG"
require_text "docs/architecture/patterns/phase-graph-orchestration.md" "pr-review-packet-visual-language.md" "phase graph doc links to packet visual language"
require_text "docs/architecture/patterns/structured-generation.md" "pr-review-packet-visual-language.md" "structured generation doc links to packet visual language"
require_text "docs/architecture/patterns/pr-review-packet-example.md" "| Area | Impact | Primary files |" "example packet includes changed areas table"
require_text "docs/architecture/patterns/pr-review-packet-example.md" "| Check | Status | Evidence |" "example packet includes validation table"
require_text "docs/architecture/patterns/pr-review-packet-example.md" "| Category | Severity | Reviewer concern | Mitigation |" "example packet includes risk matrix"
require_text "docs/architecture/patterns/pr-review-packet-example.md" "../diagrams/pr-review-packet-layout.svg" "example packet embeds the layout SVG"

echo
if [[ "$FAIL" -ne 0 ]]; then
  echo -e "${RED}check-pr-review-packet-layout: failed${NC}"
  exit 1
fi

echo -e "${GREEN}check-pr-review-packet-layout: all checks passed${NC}"
