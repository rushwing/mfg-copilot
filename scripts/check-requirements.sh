#!/usr/bin/env bash
# check-requirements.sh — validate repo-native requirement files

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

FAIL=0
WARN_COUNT=0
ERROR_COUNT=0
HAS_RG=0

if command -v rg >/dev/null 2>&1 && rg --version >/dev/null 2>&1; then
  HAS_RG=1
fi

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'
ok()   { echo -e "${GREEN}  ✓${NC} $*"; }
fail() { echo -e "${RED}  ✗${NC} $*"; FAIL=1; (( ERROR_COUNT++ )) || true; }
warn() { echo -e "${YELLOW}  ⚠${NC} $*"; (( WARN_COUNT++ )) || true; }

get_field() {
  local file="$1" field="$2"
  awk -F': ' "/^${field}:/{gsub(/^[[:space:]]+|[[:space:]]+$/, \"\", \$2); print \$2; exit}" "$file"
}

get_array_field() {
  local file="$1" field="$2"
  local raw
  raw="$(awk -F': ' "/^${field}:/{for(i=2;i<=NF;i++) printf \$i; print \"\"}" "$file" | tr -d '[]')"
  echo "$raw"
}

check_enum() {
  local val="$1" allowed="$2" context="$3"
  local found=false
  for a in $allowed; do
    if [[ "$val" == "$a" ]]; then
      found=true
      break
    fi
  done
  if ! $found; then
    fail "$context: value '$val' is not in allowed enum [$allowed]"
  fi
}

require_heading() {
  local file="$1" heading="$2" context="$3"
  if (( HAS_RG == 1 )); then
    if ! rg -q "^# ${heading}$" "$file"; then
      fail "$context: missing heading '# ${heading}'"
    fi
  elif ! grep -Eq "^# ${heading}$" "$file"; then
    fail "$context: missing heading '# ${heading}'"
  fi
}

count_section_items() {
  local file="$1" start_heading="$2"
  awk -v h="# ${start_heading}" '
    $0 == h { in_section=1; next }
    in_section && /^# / { exit }
    in_section && ($0 ~ /^- / || $0 ~ /^[0-9]+\./) { count++ }
    END { print count + 0 }
  ' "$file"
}

phase_to_file() {
  local phase="$1"
  local n="${phase#phase-}"
  printf "tasks/phases/PHASE-%03d.md" "$n"
}

FEATURE_REQUIRED_FIELDS=("req_id" "title" "status" "priority" "phase" "epic" "owner" "depends_on" "scope" "acceptance_summary")
FEATURE_STATUS_ENUM="draft ready in_progress blocked review done cancelled"
FEATURE_SCOPE_ENUM="runtime ui data infra observability docs harness"
FEATURE_PRIORITY_ENUM="P0 P1 P2 P3"
FEATURE_OWNER_ENUM="unassigned human codex claude_code"

PHASE_REQUIRED_FIELDS=("phase_id" "title" "status" "priority" "last_updated" "feature_refs")
PHASE_PRIORITY_ENUM="P0 P1 P2 P3"

TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT
FEATURE_PHASE_MAP="$TMP_DIR/feature-phase-map.txt"

if [[ ! -d "tasks/features" ]]; then
  echo "check-requirements: tasks/features/ directory not found, skipping"
  exit 0
fi

REQ_FILES=()
for f in tasks/features/REQ-*.md; do
  [[ -f "$f" ]] && REQ_FILES+=("$f")
done

if [[ ${#REQ_FILES[@]} -eq 0 ]]; then
  echo "check-requirements: no REQ files found, skipping"
  exit 0
fi

if [[ ! -d "tasks/phases" ]]; then
  fail "tasks/phases/ directory is required when tasks/features/ is present"
fi

echo "check-requirements: validating ${#REQ_FILES[@]} feature files..."
echo ""

for req_file in "${REQ_FILES[@]}"; do
  req_id="$(get_field "$req_file" "req_id")"
  file_base="$(basename "$req_file" .md)"
  echo "── ${req_id} (${req_file})"

  for field in "${FEATURE_REQUIRED_FIELDS[@]}"; do
    val="$(get_field "$req_file" "$field")"
    if [[ -z "$val" ]]; then
      fail "${req_file}: missing field '${field}'"
    fi
  done

  if [[ "$req_id" != "$file_base" ]]; then
    fail "${req_file}: req_id '$req_id' does not match filename '$file_base'"
  fi

  status="$(get_field "$req_file" "status")"
  priority="$(get_field "$req_file" "priority")"
  scope="$(get_field "$req_file" "scope")"
  owner="$(get_field "$req_file" "owner")"
  phase="$(get_field "$req_file" "phase")"

  [[ -n "$status" ]] && check_enum "$status" "$FEATURE_STATUS_ENUM" "${req_id}.status"
  [[ -n "$priority" ]] && check_enum "$priority" "$FEATURE_PRIORITY_ENUM" "${req_id}.priority"
  [[ -n "$scope" ]] && check_enum "$scope" "$FEATURE_SCOPE_ENUM" "${req_id}.scope"
  [[ -n "$owner" ]] && check_enum "$owner" "$FEATURE_OWNER_ENUM" "${req_id}.owner"

  if [[ ! "$phase" =~ ^phase-[0-9]+$ ]]; then
    fail "${req_id}: phase '$phase' must match pattern phase-N"
  else
    phase_file="$(phase_to_file "$phase")"
    if [[ ! -f "$phase_file" ]]; then
      fail "${req_id}: referenced phase file '$phase_file' does not exist"
    fi
  fi

  depends_on="$(get_array_field "$req_file" "depends_on")"
  if [[ -n "$depends_on" ]]; then
    IFS=',' read -ra deps <<< "$depends_on"
    for dep in "${deps[@]}"; do
      dep="$(echo "$dep" | tr -d ' ')"
      [[ -z "$dep" ]] && continue
      if [[ ! "$dep" =~ ^REQ-[0-9]{3}$ ]]; then
        fail "${req_id}: depends_on entry '$dep' must match REQ-xxx format"
        continue
      fi
      found_dep=false
      for d in "tasks/features/${dep}.md" "tasks/archive/done/${dep}.md" "tasks/archive/cancelled/${dep}.md"; do
        [[ -f "$d" ]] && found_dep=true && break
      done
      if ! $found_dep; then
        fail "${req_id}: depends_on reference '${dep}' does not exist"
      fi
    done
  fi

  require_heading "$req_file" "User Story" "$req_id"
  require_heading "$req_file" "Goal" "$req_id"
  require_heading "$req_file" "Deliverables" "$req_id"
  require_heading "$req_file" "In Scope" "$req_id"
  require_heading "$req_file" "Out of Scope" "$req_id"
  require_heading "$req_file" "Acceptance Criteria" "$req_id"
  require_heading "$req_file" "Validation Notes" "$req_id"
  require_heading "$req_file" "Dependency Notes" "$req_id"

  deliverable_count="$(count_section_items "$req_file" "Deliverables")"
  if (( deliverable_count < 1 )); then
    fail "${req_id}: Deliverables section must contain at least 1 list item"
  fi

  acceptance_count="$(count_section_items "$req_file" "Acceptance Criteria")"
  if (( acceptance_count < 3 )); then
    fail "${req_id}: Acceptance Criteria section must contain at least 3 list items"
  fi

  validation_count="$(count_section_items "$req_file" "Validation Notes")"
  if (( validation_count < 1 )); then
    fail "${req_id}: Validation Notes section must contain at least 1 list item"
  fi

  dependency_count="$(count_section_items "$req_file" "Dependency Notes")"
  if (( dependency_count < 1 )); then
    fail "${req_id}: Dependency Notes section must contain at least 1 list item"
  fi

  if [[ "$status" == "in_progress" && "$owner" == "unassigned" ]]; then
    fail "${req_id}: status=in_progress but owner=unassigned"
  fi

  if [[ "$status" == "blocked" ]]; then
    if (( HAS_RG == 1 )); then
      if ! rg -q '^blocked_reason:' "$req_file"; then
        warn "${req_id}: blocked story has no blocked_reason field yet"
      fi
    elif ! grep -Eq '^blocked_reason:' "$req_file"; then
      warn "${req_id}: blocked story has no blocked_reason field yet"
    fi
  fi

  echo "${req_id} ${phase}" >> "$FEATURE_PHASE_MAP"

  ok "${req_id}: feature checks passed"
  echo ""
done

if [[ -d "tasks/phases" ]]; then
  echo "check-requirements: validating phase files..."
  echo ""

  PHASE_FILES=()
  for f in tasks/phases/PHASE-*.md; do
    [[ -f "$f" ]] && PHASE_FILES+=("$f")
  done

  for phase_file in "${PHASE_FILES[@]}"; do
    phase_id="$(get_field "$phase_file" "phase_id")"
    file_base="$(basename "$phase_file" .md)"
    echo "── ${phase_id} (${phase_file})"

    for field in "${PHASE_REQUIRED_FIELDS[@]}"; do
      val="$(get_field "$phase_file" "$field")"
      if [[ -z "$val" ]]; then
        fail "${phase_file}: missing field '${field}'"
      fi
    done

    if [[ ! "$phase_id" =~ ^phase-[0-9]+$ ]]; then
      fail "${phase_file}: phase_id '$phase_id' must match pattern phase-N"
    else
      expected_phase_file="$(phase_to_file "$phase_id")"
      if [[ "$phase_file" != "$expected_phase_file" ]]; then
        fail "${phase_file}: phase_id '$phase_id' should live at '$expected_phase_file'"
      fi
    fi

    phase_priority="$(get_field "$phase_file" "priority")"
    [[ -n "$phase_priority" ]] && check_enum "$phase_priority" "$PHASE_PRIORITY_ENUM" "${phase_id}.priority"

    require_heading "$phase_file" "Goal" "$phase_id"
    require_heading "$phase_file" "In Scope" "$phase_id"
    require_heading "$phase_file" "Out of Scope" "$phase_id"
    require_heading "$phase_file" "Exit Criteria" "$phase_id"

    feature_refs="$(get_array_field "$phase_file" "feature_refs")"
    if [[ -z "$(echo "$feature_refs" | tr -d ' ')" ]]; then
      fail "${phase_id}: feature_refs must not be empty"
    else
      IFS=',' read -ra refs <<< "$feature_refs"
      for ref in "${refs[@]}"; do
        ref="$(echo "$ref" | tr -d ' ')"
        [[ -z "$ref" ]] && continue
        if [[ ! "$ref" =~ ^REQ-[0-9]{3}$ ]]; then
          fail "${phase_id}: feature_refs entry '$ref' must match REQ-xxx format"
          continue
        fi
        if [[ ! -f "tasks/features/${ref}.md" ]]; then
          fail "${phase_id}: feature_refs references missing feature '$ref'"
          continue
        fi
        ref_phase="$(awk -v req="$ref" '$1 == req { print $2; exit }' "$FEATURE_PHASE_MAP")"
        if [[ "$ref_phase" != "$phase_id" ]]; then
          fail "${phase_id}: feature_refs includes '$ref' but feature.phase is '$ref_phase'"
        fi
      done
    fi

    # Reverse cross-check: every feature mapped to this phase should appear in feature_refs
    phase_feature_list="$(awk -v phase="$phase_id" '$2 == phase { print $1 }' "$FEATURE_PHASE_MAP")"
    for req in $phase_feature_list; do
      if ! grep -q "$req" <<< "$feature_refs"; then
        fail "${phase_id}: feature '$req' has phase=$phase_id but is missing from feature_refs"
      fi
    done

    ok "${phase_id}: phase checks passed"
    echo ""
  done
fi

if [[ $FAIL -eq 0 ]]; then
  echo -e "${GREEN}check-requirements: all checks passed (warnings: ${WARN_COUNT})${NC}"
  exit 0
else
  echo -e "${RED}check-requirements: found ${ERROR_COUNT} errors and ${WARN_COUNT} warnings${NC}"
  exit 1
fi
