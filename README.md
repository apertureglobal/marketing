# Aperture Global — Marketing Library

Internal marketing library for Aperture Global Real Estate agents, published with GitHub Pages.

**Live site:** https://apertureglobal.github.io/marketing/

> ⚠️ **This site is public.** GitHub Pages on a public repo has no password or access
> control, and anything committed here is readable by anyone with the URL. The page carries a
> `noindex` tag, which discourages search engines but does not restrict access. Do not commit
> commission structures, agent rosters, client data, unreleased listings, or anything else that
> shouldn't leave the brokerage. See "Making this actually private" below.

---

## Adding or updating an item

Two steps: drop the file in the right folder, then add an entry to `library.json`.

### 1. Add the file

| Section | Folder |
|---|---|
| Strategy documents | `assets/strategy/` |
| Performance reports | `assets/reports/` |
| Brand kit | `assets/brand/` |
| Social graphics | `assets/social/` |

Use lowercase filenames with dashes instead of spaces — `q3-digital-report.pdf`, not
`Q3 Digital Report.pdf`. Spaces work but produce ugly `%20` links when agents copy them.

You can skip this step entirely for externally hosted items (Google Drive, Canva, Dropbox)
and just use a `url` instead — see below.

### 2. Add the entry

Open `library.json` and add an object to the matching array.

```jsonc
{
  "title":       "Q4 2026 Digital Performance Report",  // required
  "description": "Impressions, CTR, and cost per lead.", // shown under the title
  "channel":     "digital",        // strategy + reports only: digital | billboard | directmail
  "kind":        "Brand guide",    // brand kit only: free-text label, e.g. Logos, Templates
  "platform":    "Instagram",      // social only: free-text label
  "updated":     "2026-12-15",     // YYYY-MM-DD
  "file":        "assets/reports/q4-digital-report.pdf",  // file in this repo
  "url":         "https://...",    // OR an external link — use one or the other
  "thumb":       "assets/social/preview.png",  // social: defaults to `file` if it's an image
  "caption":     "Just listed in..."           // social: suggested caption, copyable
}
```

Every entry needs a `title` and either a `file` or a `url`. Everything else is optional.

`directmail` is intentionally only offered on strategy documents, not reports.

### 3. Commit

```bash
git add -A && git commit -m "Add Q4 digital report" && git push
```

The live site updates within a minute or two.

---

## Removing the example content

`library.json` ships with placeholder entries whose filenames start with `EXAMPLE-`. They point
at files that don't exist, so they render with a "No file yet" badge or an empty thumbnail.
Delete those entries as you replace them with real assets.

---

## Working on the page locally

`index.html` loads `library.json` with `fetch()`, which browsers block on `file://` URLs. Opening
the file by double-clicking will show a load error. Run a local server instead:

```bash
python3 -m http.server 8000
```

Then open http://localhost:8000.

---

## How it's built

- `index.html` — the entire site. No build step, no dependencies, no framework.
- `library.json` — all content. This is the only file you need to touch day to day.
- `assets/` — the actual documents and graphics.

Adding a new top-level section means editing the `SECTIONS` array near the top of the script
block in `index.html`, then adding a matching key to `library.json`.

---

## Making this actually private

Free GitHub Pages cannot be access-controlled. Real options, cheapest first:

1. **Cloudflare Pages + Cloudflare Access** — free tier covers up to 50 users. Connect this repo,
   put an Access policy in front requiring an `@apertureglobal.com` email. This is the usual
   answer and requires no plan change on GitHub.
2. **Netlify** — password protection or role-based access on paid tiers.
3. **GitHub Enterprise Cloud** — supports private Pages visible only to org members. Expensive
   if this is the only reason to upgrade.
4. **Make the repo private and drop Pages** — agents would use the repo directly, which is a
   poor fit for non-technical users.

Until one of those is in place, treat everything committed here as public.
