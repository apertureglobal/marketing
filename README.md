# Aperture Global, Marketing Library

Internal marketing library for Aperture Global Real Estate agents, published with GitHub Pages.

**Live site:** https://apertureglobal.github.io/marketing/

> **This site is public.** GitHub Pages on a public repo carries no password and no access
> control, so anything committed here is readable by anyone holding the URL. The page sends a
> `noindex` tag, which discourages search engines without restricting access. Commission
> structures, agent rosters, client data, and unreleased listings do not belong in this repo.
> Options for closing that gap appear at the bottom of this file.

---

## Adding or updating an item

Two steps: place the file in the right folder, then add an entry to `library.json`.

### 1. Add the file

| Section | Folder |
| --- | --- |
| Campaign documents | `assets/campaigns/` |
| Brand kit | `assets/brand/` |
| Social graphics | `assets/social/` |

Lowercase filenames with dashes rather than spaces keep the copied links clean:
`q3-digital-report.pdf` rather than `Q3 Digital Report.pdf`.

Externally hosted items on Google Drive, Canva, or Dropbox skip this step and use a `url`.

### 2. Add the entry

Add an object to the matching array in `library.json`.

```jsonc
{
  "title":       "Fourth Quarter Digital Performance Report",  // required
  "description": "Impressions, click through rate, and cost per lead.",
  "agent":       "Kyle Foreman",   // campaigns: owning agent, or Corporate
  "type":        "report",         // campaigns: strategy | report
  "channel":     "digital",        // campaigns: digital | billboard | directmail
  "kind":        "Brand guide",    // brand kit: free text, such as Logos or Templates
  "platform":    "Instagram",      // social: free text
  "updated":     "2026-12-15",     // YYYY-MM-DD
  "file":        "assets/campaigns/q4-digital-report.pdf",  // a file in this repo
  "url":         "https://...",    // or an external link, one or the other
  "thumb":       "assets/social/preview.png",  // social, defaults to `file` when it is an image
  "caption":     "Just listed in..."           // social, the suggested caption
}
```

Each entry needs a `title` and either a `file` or a `url`. The rest is optional.

### Campaign documents, grouped by agent

Strategy documents and performance reports share one `campaigns` bucket, grouped on the page by
the `agent` field and separated by the `type` field.

An entry missing `agent` falls back to Corporate, which is the right home for brokerage wide
playbooks belonging to no single agent. Corporate sorts first, and every other agent follows
alphabetically. Agent names are matched as plain strings, so spelling one two ways produces two
groups.

Both filter rows apply together, and the search box matches agent names as well as titles and
descriptions.

### 3. Commit

```bash
git add -A && git commit -m "Add fourth quarter digital report" && git push
```

The live site follows within a minute or two.

---

## Copy conventions

Everything visible on the page follows `guidelines/brand-voice.md`: no em or en dashes, numbers
spelled out in prose, facts ahead of superlatives, no commands, and one verifiable claim per
block. That applies to titles, descriptions, and the suggested social captions in `library.json`.

The page spells out counts at runtime through a `spell()` helper, so a section holding fourteen
items reads as "fourteen" rather than as a numeral.

---

## Design system

`index.html` implements `guidelines/tokens-handoff.md`. The token block at the top of the file
is the single source of truth, and three rules from the handoff sheet shape everything below it:

- **Corners are square.** A global `border-radius: var(--radius-0)` enforces this.
- **There are no shadows.** Separation comes from hairline rules and whitespace.
- **Accent blue carries one verifiable claim per block, never decoration.** On this page the blue
  appears in exactly two places, both of them counts: the tally under the headline and the item
  count on each section tab. Nothing else uses it, and the logo blues stay reserved for the mark.

Labels are uppercase Archivo at ten pixels with `letter-spacing: var(--label-tracking)`. That
treatment carries the tabs, filters, metadata, and action controls.

### Fonts

Self hosted from `assets/fonts/`, matching the variable TTFs named in the handoff sheet.
Browsers download only the faces actually rendered, so declaring all four costs nothing at load.

These are the raw TTFs, roughly two and a half megabytes across the three faces in use.
Converting them to woff2 would cut that by about seventy percent and needs `fonttools[woff]`,
which is not installed on this machine.

### Logos

`assets/logos/` is not populated yet. The masthead currently renders a text wordmark. Dropping
`aperture-color-horizontal.svg` and `aperture-color-horizontal-ondark.svg` into that folder and
swapping the `.wordmark` element for an `<img>` finishes it.

---

## Removing the example content

`library.json` ships with placeholder entries whose filenames begin with `EXAMPLE-`. They point
at files that do not exist, so they render with a "Not yet uploaded" state. Delete each one as a
real asset replaces it.

---

## Working on the page locally

`index.html` loads `library.json` through `fetch()`, which browsers block on `file://` URLs, so
opening the file by double clicking shows a load error. Use a local server:

```bash
python3 -m http.server 8000
```

Then open http://localhost:8000.

---

## How it is built

- `index.html`, the entire site. No build step, no dependencies, no framework.
- `library.json`, all content. This is the only file that changes day to day.
- `assets/`, the documents, graphics, and fonts.

Adding a new top level section means editing the `SECTIONS` array in the script block of
`index.html` and adding a matching key to `library.json`.

---

## Making this private

Free GitHub Pages cannot be access controlled. The practical options, cheapest first:

1. **Cloudflare Pages with Cloudflare Access.** The free tier covers fifty users. Connect this
   repo and place an Access policy in front requiring an Aperture Global email address. This is
   the usual answer and asks for no plan change at GitHub.
2. **Netlify.** Password protection and role based access arrive on the paid tiers.
3. **GitHub Enterprise Cloud.** Supports private Pages visible to organization members only, and
   is expensive when this page is the only reason to upgrade.
4. **A private repo without Pages.** Agents would navigate the repo directly, which suits
   non technical users poorly.

Until one of those is in place, everything committed here is public.
