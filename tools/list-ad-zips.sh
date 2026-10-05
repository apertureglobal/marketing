#!/usr/bin/env bash
# Print every creative zip with the URL it will serve from, so you can
# copy the right one into StackAdapt's creative uploader.
#
# Usage: ./tools/list-ad-zips.sh [property-slug-fragment]

PROJECT="${CF_PAGES_PROJECT:-aperture-ads}"
cd "$(dirname "$0")/.."
FILTER="${1:-}"

find html5 -name '*.zip' | sort | while read -r z; do
  rel="${z#html5/}"
  [ -n "$FILTER" ] && [[ "$rel" != *"$FILTER"* ]] && continue
  kb=$(( $(stat -f%z "$z") / 1024 ))
  printf "%4s KB  https://%s.pages.dev/%s\n" "$kb" "$PROJECT" "$rel"
done
