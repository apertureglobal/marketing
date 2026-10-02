# Ad hosting (Cloudflare Pages)

Operational host for HTML5 display creative. **Not client-facing** — client
previews stay on GitHub Pages. This host is `noindex`ed and exists so campaigns
can be launched without serving production traffic off GitHub Pages, which
GitHub's terms do not permit.

## What StackAdapt actually needs

StackAdapt ingests HTML5 display creative as a **zip upload** — markup, assets,
a clickTag and a static fallback in one package — then serves it from its own
CDN. It does not serve creative from our URL. So the zips in each property
folder are the deliverable; this host is where you fetch them from, and a
durable archive of exactly what was trafficked.

Each ad set ships six zips, one per core size: 768x1024, 1024x768, 480x320,
970x250, 320x480, 300x600.

## One-time setup

```bash
wrangler login                      # interactive; must be run by a human
wrangler pages project create aperture-ads --production-branch=main
```

For push-to-deploy, add two repository secrets and the workflow does the rest:
`CLOUDFLARE_API_TOKEN` (needs "Cloudflare Pages: Edit") and
`CLOUDFLARE_ACCOUNT_ID`.

## Deploying

```bash
./tools/deploy-ads.sh               # manual publish
```

Or just push to `main` — `.github/workflows/deploy-ads.yml` fires on any change
under `html5/`.

## Getting a zip to upload

```bash
./tools/list-ad-zips.sh 312Madison  # prints URLs + sizes for one property
./tools/list-ad-zips.sh             # everything
```

## Budget

Every unit stays under **700 KB**. With no video there is no bitrate to trade,
so JPEG quality is the only lever. Check before trafficking:

```bash
find html5 -name '*.zip' -size +700k
```

An empty result is a pass.
