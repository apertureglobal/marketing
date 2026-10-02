#!/usr/bin/env bash
# Publish html5/ to Cloudflare Pages.
#
# First run, once per machine:   wrangler login
# Then:                          ./tools/deploy-ads.sh
#
# Creative zips land at:
#   https://<project>.pages.dev/<PropertySlug>/APERTURE_<Slug>_<size>.zip
# which is the file you upload to StackAdapt.

set -euo pipefail
PROJECT="${CF_PAGES_PROJECT:-aperture-ads}"
cd "$(dirname "$0")/.."

if ! wrangler whoami >/dev/null 2>&1; then
  echo "Not logged in to Cloudflare. Run:  wrangler login" >&2
  exit 1
fi

echo "Deploying html5/ ($(find html5 -type f | wc -l | tr -d ' ') files) to Pages project '$PROJECT'..."
wrangler pages deploy html5 --project-name "$PROJECT" --commit-dirty=true

echo
echo "Creative zips are now at:"
echo "  https://$PROJECT.pages.dev/<PropertySlug>/<zip name>"
