#!/usr/bin/env bash
# check-progressive-disclosure.sh — validate repo doc navigation stays layered

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

FAIL=0

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
  if rg -q --fixed-strings "$pattern" "$file"; then
    ok "$label"
  else
    fail "$label"
  fi
}

forbidden_text() {
  local file="$1" pattern="$2" label="$3"
  if rg -q --fixed-strings "$pattern" "$file"; then
    fail "$label"
  else
    ok "$label"
  fi
}

echo "check-progressive-disclosure: validating required navigation hubs..."

require_file "README.md"
require_file "docs/README.md"
require_file "docs/architecture/README.md"
require_file "docs/architecture/overview.md"
require_file "docs/adr/README.md"
require_file "tasks/README.md"
require_file "tasks/phases/README.md"
require_file "tasks/features/README.md"

echo
echo "check-progressive-disclosure: validating root navigation..."

require_text "README.md" "(./docs/README.md)" "root README links to docs home"
require_text "README.md" "(./docs/architecture/overview.md)" "root README links to architecture overview"
require_text "README.md" "(./tasks/README.md)" "root README links to tasks home"

forbidden_text "README.md" "(./docs/architecture/phase-plan.md)" "root README does not deep-link phase plan"
forbidden_text "README.md" "(./docs/architecture/requirements-breakdown.md)" "root README does not deep-link requirements breakdown"
forbidden_text "README.md" "(./docs/architecture/requirements-management.md)" "root README does not deep-link requirements management"
forbidden_text "README.md" "(./docs/architecture/solution-design.md)" "root README does not deep-link solution design"
forbidden_text "README.md" "(./docs/architecture/system-architecture.md)" "root README does not deep-link source architecture notes"
forbidden_text "README.md" "(./docs/architecture/testing-and-evals.md)" "root README does not deep-link testing strategy"

echo
echo "check-progressive-disclosure: validating docs and tasks indexes..."

require_text "docs/README.md" "(./architecture/README.md)" "docs home links to architecture index"
require_text "docs/README.md" "(../tasks/README.md)" "docs home links to tasks home"
require_text "docs/README.md" "(./adr/README.md)" "docs home links to ADR index"

require_text "tasks/README.md" "(./phases/README.md)" "tasks home links to phase index"
require_text "tasks/README.md" "(./features/README.md)" "tasks home links to feature index"

forbidden_text "tasks/README.md" "(./features/REQ-" "tasks home does not deep-link individual REQ files"
forbidden_text "tasks/README.md" "(./phases/PHASE-" "tasks home does not deep-link individual phase files"

echo
if [[ "$FAIL" -ne 0 ]]; then
  echo -e "${RED}check-progressive-disclosure: failed${NC}"
  exit 1
fi

echo -e "${GREEN}check-progressive-disclosure: all checks passed${NC}"
