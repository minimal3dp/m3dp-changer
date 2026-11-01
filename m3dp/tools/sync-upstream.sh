#!/usr/bin/env bash
# Fetch and report upstream CxChanger changes for manual review.
# The historical filename is retained; this script never merges or pushes.
# Usage: m3dp/tools/sync-upstream.sh [--no-merge]
set -euo pipefail

case "${1:-}" in
  ""|--no-merge) ;;
  --help|-h)
    echo "Usage: m3dp/tools/sync-upstream.sh [--no-merge]"
    echo "Fetch upstream/main and report changes; no merge, push, or branch switch."
    exit 0 ;;
  *) echo "Unknown option: $1" >&2; exit 2 ;;
esac

cd "$(git rev-parse --show-toplevel)"
UPSTREAM_URL="https://github.com/cx330-TXY/CxChanger.git"
git remote get-url upstream >/dev/null 2>&1 || git remote add upstream "$UPSTREAM_URL"
git remote set-url --push upstream DISABLE
git fetch upstream main

NEW=$(git rev-list --count main..upstream/main)
echo "Upstream commits not included in M3DP Changer main: $NEW"
if [[ "$NEW" -gt 0 ]]; then
  git --no-pager log --format='%h %ci %s' main..upstream/main
  BASE=$(git merge-base main upstream/main)
  git --no-pager diff --stat "$BASE" upstream/main
fi
echo "Review changes on a development branch; record adopted changes in m3dp/UPSTREAM-CHANGELOG.md."
