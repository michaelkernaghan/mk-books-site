# MK Books — Stripe Activation Website Design

**Date**: 2026-04-19
**Status**: Approved design, ready for implementation plan
**Owner**: Michael Kernaghan

## Purpose

Deploy a public business website for **MK Books** so that Stripe's account-activation review can verify the business is legitimate. The business is a sole proprietorship selling used/rare books exclusively through AbeBooks storefront ID `91160525`. The website does **not** host any on-site checkout — it is an informational landing page that links out to the AbeBooks storefront.

## Non-Goals

- No on-site commerce, cart, or checkout
- No live inventory feed from AbeBooks
- No analytics, tracking, or cookies
- No contact form backend (mailto only)
- No CMS, blog, newsletter, or comments
- No framework, build step, or runtime JavaScript beyond a trivial footer-year snippet

## Constraints & Context

- **Business**: MK Books, sole proprietorship, Mission, British Columbia, Canada
- **Contact email**: michael.kernaghan@gmail.com
- **Public phone**: TBD (owner has agreed to display a phone number; number itself to be supplied at content-writing time)
- **AbeBooks storefront**: https://www.abebooks.com/servlet/StoreFrontDisplay?cid=91160525 (store ID 91160525)
- **Categories marketed**: Military history, classic cookery, rare and miscellaneous older titles
- **Sales model**: 100% AbeBooks-fulfilled; AbeBooks handles payment, shipping charges, and Buyer Guarantee
- **GST/HST**: not required for this volume of AbeBooks selling (confirmed 2026-04-14)
- **Stripe requirements** driving content: business description, contact info, refund policy, shipping policy, terms of service, privacy policy

## Architecture

### Repo

- **New public GitHub repo**: `michaelkernaghan/mk-books-site`
- Separate from the existing `michaelkernaghan/book-management` repo, which holds private inventory notes and triage activity logs
- Rationale: the Stripe-facing site is public marketing; inventory workflow data must not appear in what a Stripe reviewer or casual visitor sees when clicking a repo link

### Hosting

- **Netlify**, connected to `main` branch of the new repo
- Auto-deploy on every push to `main`
- Publish directory: `.` (repo root)
- No build command — plain static files
- TLS certificate auto-provisioned by Netlify

### Domain

- **Custom `.ca` domain** (preferred), e.g. `mkbooks.ca`, `mkbookstore.ca`, `mkrarebooks.ca`
- Exact name chosen at registration time based on availability
- DNS managed via Netlify DNS (simplest path) or external registrar with CNAME to Netlify
- Netlify subdomain (`*.netlify.app`) available as interim while DNS propagates, but final Stripe submission uses the custom domain

### Stack

Plain HTML + CSS. No build step, no framework, no package manager.

- One `.html` file per page
- Shared `styles.css`
- Optional tiny inline `<script>` for dynamic footer year — no external JS dependencies
- No analytics, no cookies, no tracking pixels

## Repo Layout

```
mk-books-site/
├── index.html           # Home
├── about.html           # About MK Books
├── contact.html         # Contact info
├── policies.html        # Returns, Shipping, Terms (one page, three H2 sections)
├── privacy.html         # Privacy policy (separate page)
├── styles.css
├── assets/              # Logo, images — kept small, no stock photos
├── netlify.toml         # Minimal: publish = "."
├── README.md            # What this site is, how to update it
└── .gitignore
```

## Page Content

### `index.html` — Home

- Header: "MK Books" wordmark, nav links (About · Policies · Contact)
- Hero: business name + one-sentence description: "Curated military history, classic cookery, and rare older titles — sold exclusively through our AbeBooks storefront."
- Three category cards (text only, no live inventory): Military History · Classic Cooking · Rare & Miscellaneous
- Primary CTA button: "Shop on AbeBooks" → AbeBooks storefront URL
- "How it works" section: browse on AbeBooks → order there → AbeBooks handles payment and shipping → AbeBooks Buyer Guarantee covers the transaction
- Footer: copyright, links to About / Policies / Privacy / Contact

### `about.html` — About

- Owner introduction: Michael Kernaghan, Mission, British Columbia, Canada
- Origin paragraph: longtime collector downsizing a personal library; every book is hand-inspected and described
- Areas of specialty: military history, classic cookery, older rare titles
- AbeBooks seller ID (91160525) and storefront link

### `policies.html` — Policies (single page, three sections)

**Returns & Refunds**

> All sales are fulfilled through AbeBooks and are subject to the AbeBooks Buyer Guarantee. Returns and refunds are handled per AbeBooks' standard policy. Contact us with any questions.

Links to AbeBooks' buyer-guarantee / returns page.

**Shipping**

> Orders are packed and shipped within 2 business days of an AbeBooks order being placed. Shipping rates, carriers, and delivery times are set by AbeBooks at checkout.

**Terms of Service**

> MK Books is a sole proprietorship based in Mission, British Columbia, Canada. All transactions are processed through AbeBooks and are governed by AbeBooks' terms of service in addition to these terms. MK Books reserves the right to cancel orders in the event of pricing errors, inventory unavailability, or suspected fraud.

### `privacy.html` — Privacy

- We do not collect visitor data on this site: no analytics, no cookies, no tracking pixels
- The site has no forms; contact is by email only, and any information shared by email is used solely to respond to the inquiry
- Purchase data is handled by AbeBooks — see AbeBooks' privacy policy
- Contact email for privacy inquiries

### `contact.html` — Contact

- Business name: MK Books
- Location: Mission, British Columbia, Canada
- Email: michael.kernaghan@gmail.com (displayed with a simple anti-scrape obfuscation, e.g., `michael [dot] kernaghan [at] gmail`, plus a working `mailto:` link)
- Phone: TBD number, displayed
- AbeBooks storefront link
- Response time: within 2 business days

## Deployment Flow (one-time, ~30 min)

1. Create empty GitHub repo `michaelkernaghan/mk-books-site` (public)
2. Scaffold files locally in `C:/Users/Michael Kernaghan/mk-books-site/`
3. `git init`, initial commit, push to `main`
4. Netlify: New site from Git → select repo → publish directory `.` → deploy
5. Register `.ca` domain (via Netlify registrar or external)
6. Configure DNS in Netlify; wait for TLS cert to auto-provision
7. Verify site loads on custom domain over HTTPS
8. Submit custom-domain URL to Stripe for account-activation review

## Ongoing Operations

- Edit HTML locally, commit, push — Netlify redeploys in ~10 seconds
- No dependencies to patch, no lockfiles to update
- If the site later needs to grow into a real catalog, port to Astro is a half-day job

## Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Stripe rejects for "insufficient business detail" | About page names the business, owner, location, and AbeBooks storefront ID; Policies page covers all three required policy areas |
| Domain registration or DNS propagation delays Stripe submission | Register domain early; site is still demonstrable on `*.netlify.app` while DNS settles |
| Plaintext email invites spam | Display email with `[dot]` / `[at]` obfuscation in visible text, working `mailto:` link underneath |
| Policy language drifts out of sync with AbeBooks' actual policy | Defer to AbeBooks rather than restating their terms; link out instead of paraphrasing |

## Acceptance Criteria

Done when **all** of the following are true:

- [ ] Site is live on the custom `.ca` domain over HTTPS
- [ ] All 5 pages (home, about, policies, privacy, contact) render correctly on desktop and mobile
- [ ] Every Stripe-required element is present and visible without login: business description, contact, refund policy, shipping policy, terms of service, privacy policy
- [ ] The AbeBooks storefront link works from at least 3 pages (home, about, contact)
- [ ] No browser console errors, no broken links, no placeholder copy left in the source
- [ ] The repo `README.md` documents how to edit and redeploy the site
- [ ] Stripe account has been submitted for activation review against the custom-domain URL

## Open Items To Resolve at Implementation Time

1. Final custom domain name (check availability of several `.ca` options)
2. Phone number to display on contact page
3. Whether to create a dedicated business email alias or continue with `michael.kernaghan@gmail.com`
4. Logo / wordmark treatment — plain text set in a serif face is acceptable for v1; a proper logo can replace it later without a redesign
