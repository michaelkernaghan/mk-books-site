# MK Books Stripe Activation Site — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deploy a 5-page static business website for MK Books (sole prop, Mission BC) on Netlify behind a custom `.ca` domain, suitable for Stripe account-activation review.

**Architecture:** Plain HTML + CSS, no build step. One shared `styles.css`. One file per page. New public GitHub repo `michaelkernaghan/mk-books-site` connected to Netlify with auto-deploy on push to `main`. Custom `.ca` domain with Netlify-managed DNS and auto-provisioned TLS.

**Tech Stack:** HTML5, CSS3 (no framework), Netlify (hosting + DNS + TLS), GitHub (source), `gh` CLI for repo creation.

**Spec:** `docs/superpowers/specs/2026-04-19-mk-books-stripe-site-design.md`

---

## Prerequisites (ask user before starting Task 1)

These inputs are required to avoid placeholders in the implemented pages. If any are unknown at plan-execution time, pause and ask the user before proceeding past the task that needs them.

| Input | Needed by task | Default / note |
|-------|----------------|----------------|
| Public phone number to display | Task 7 (Contact page) | User agreed to display one; number itself not yet provided |
| Final custom domain name | Task 11 (DNS) | Check availability of `mkbooks.ca`, `mkbookstore.ca`, `mkrarebooks.ca` first |
| Confirm email: `michael.kernaghan@gmail.com` | Task 7 | Owner may decide to use a dedicated alias later — confirm at Task 7 |

Business name, location, AbeBooks URL, and category list are already fixed in the spec and used literally below.

---

## File Structure

Working directory: `C:/Users/Michael Kernaghan/mk-books-site/`

| Path | Purpose |
|------|---------|
| `index.html` | Home — hero, categories, CTA to AbeBooks, how-it-works |
| `about.html` | Owner intro, specialties, AbeBooks store ID |
| `policies.html` | Returns, Shipping, Terms (three H2 sections on one page) |
| `privacy.html` | Privacy policy — no data collection statement |
| `contact.html` | Email, phone, location, AbeBooks link |
| `styles.css` | All shared styling (typography, nav, footer, layout, buttons, cards) |
| `assets/` | Images (favicon + any hero graphic) — kept minimal |
| `netlify.toml` | Publish directory config |
| `README.md` | What this site is, how to edit and redeploy |
| `.gitignore` | Ignore OS junk, editor state |

Each HTML file is self-contained (no templating). Header/footer markup is duplicated by hand — 5 copies is cheaper than a build step for a site this small.

---

## Task 1: Scaffold the repo locally

**Files:**
- Create: `C:/Users/Michael Kernaghan/mk-books-site/.gitignore`
- Create: `C:/Users/Michael Kernaghan/mk-books-site/README.md`
- Create: `C:/Users/Michael Kernaghan/mk-books-site/netlify.toml`
- Create: `C:/Users/Michael Kernaghan/mk-books-site/assets/.gitkeep`

- [ ] **Step 1: Create `.gitignore`**

```
# OS
.DS_Store
Thumbs.db

# Editor
.vscode/
.idea/
*.swp
*~

# Netlify local CLI state
.netlify/
```

- [ ] **Step 2: Create `netlify.toml`**

```toml
[build]
  publish = "."

[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"
```

- [ ] **Step 3: Create `README.md`**

```markdown
# mk-books-site

Public business website for **MK Books** — a sole proprietorship based in Mission, BC selling military history, classic cookery, and rare older books exclusively through our [AbeBooks storefront](https://www.abebooks.com/servlet/StoreFrontDisplay?cid=91160525).

This site exists so that Stripe's account-activation review can verify the business. There is no on-site checkout.

## Editing

Edit the relevant `.html` file and `styles.css`. No build step.

## Deploying

Push to `main`. Netlify auto-deploys in ~10 seconds.

## Pages

- `index.html` — home
- `about.html` — about the business
- `policies.html` — returns, shipping, terms
- `privacy.html` — privacy policy
- `contact.html` — contact info

## Local preview

Open any `.html` file directly in a browser, or run a tiny static server from the repo root:

    python -m http.server 8000

Then visit <http://localhost:8000>.
```

- [ ] **Step 4: Create the `assets/` directory**

```bash
mkdir -p "C:/Users/Michael Kernaghan/mk-books-site/assets"
touch "C:/Users/Michael Kernaghan/mk-books-site/assets/.gitkeep"
```

- [ ] **Step 5: Initialize git and stage**

```bash
cd "C:/Users/Michael Kernaghan/mk-books-site"
git init -b main
git add .gitignore README.md netlify.toml assets/.gitkeep docs/
```

- [ ] **Step 6: Present commit command to user**

Show `git status` and `git diff --cached`, then present this command for the user to run manually:

```bash
git -C "C:/Users/Michael Kernaghan/mk-books-site" commit -m "chore: scaffold mk-books-site repo"
```

Do **not** run the commit — the user's git-safety hook requires manual execution.

---

## Task 2: Build shared `styles.css`

**Files:**
- Create: `C:/Users/Michael Kernaghan/mk-books-site/styles.css`

- [ ] **Step 1: Write the stylesheet**

```css
:root {
  --ink: #1f1a15;
  --paper: #faf6ef;
  --accent: #6b2e2a;
  --muted: #6d655a;
  --rule: #d8cfc0;
  --max: 780px;
}

* { box-sizing: border-box; }

html, body {
  margin: 0;
  padding: 0;
  background: var(--paper);
  color: var(--ink);
  font-family: Georgia, "Times New Roman", serif;
  font-size: 18px;
  line-height: 1.6;
}

a { color: var(--accent); text-decoration: underline; }
a:hover { text-decoration: none; }

.container {
  max-width: var(--max);
  margin: 0 auto;
  padding: 2rem 1.25rem 3rem;
}

header.site {
  border-bottom: 1px solid var(--rule);
  padding: 1rem 1.25rem;
}
header.site .wrap {
  max-width: var(--max);
  margin: 0 auto;
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 0.75rem;
}
header.site .brand {
  font-size: 1.5rem;
  font-weight: bold;
  letter-spacing: 0.02em;
  color: var(--ink);
  text-decoration: none;
}
header.site nav a {
  margin-left: 1rem;
  font-size: 0.95rem;
}

h1 { font-size: 2rem; margin: 0 0 0.5rem; }
h2 { font-size: 1.35rem; margin: 2rem 0 0.5rem; border-bottom: 1px solid var(--rule); padding-bottom: 0.25rem; }
h3 { font-size: 1.1rem; margin: 1.25rem 0 0.5rem; }

.lede {
  font-size: 1.1rem;
  color: var(--muted);
  margin-bottom: 1.5rem;
}

.btn {
  display: inline-block;
  background: var(--accent);
  color: var(--paper);
  padding: 0.75rem 1.25rem;
  border-radius: 2px;
  text-decoration: none;
  font-weight: bold;
  margin: 1rem 0;
}
.btn:hover { background: #532320; text-decoration: none; }

.cards {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
  margin: 1.5rem 0;
}
@media (min-width: 640px) {
  .cards { grid-template-columns: repeat(3, 1fr); }
}
.card {
  border: 1px solid var(--rule);
  padding: 1rem;
  background: #fff;
}
.card h3 { margin-top: 0; }
.card p { margin: 0.5rem 0 0; color: var(--muted); font-size: 0.95rem; }

footer.site {
  border-top: 1px solid var(--rule);
  margin-top: 3rem;
  padding: 1.5rem 1.25rem;
  font-size: 0.9rem;
  color: var(--muted);
  text-align: center;
}
footer.site a { color: var(--muted); }
footer.site .links { margin-top: 0.25rem; }
footer.site .links a { margin: 0 0.5rem; }

.meta {
  color: var(--muted);
  font-size: 0.95rem;
}
```

- [ ] **Step 2: Stage and present commit**

```bash
git -C "C:/Users/Michael Kernaghan/mk-books-site" add styles.css
```

Present to user:

```bash
git -C "C:/Users/Michael Kernaghan/mk-books-site" commit -m "feat: add shared stylesheet"
```

---

## Task 3: Build `index.html` (Home)

**Files:**
- Create: `C:/Users/Michael Kernaghan/mk-books-site/index.html`

- [ ] **Step 1: Write the home page**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>MK Books — Military History, Classic Cookery, Rare Older Books</title>
  <meta name="description" content="MK Books is a Canadian sole proprietorship selling curated military history, classic cookery, and rare older titles exclusively through our AbeBooks storefront.">
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <header class="site">
    <div class="wrap">
      <a class="brand" href="index.html">MK Books</a>
      <nav>
        <a href="about.html">About</a>
        <a href="policies.html">Policies</a>
        <a href="privacy.html">Privacy</a>
        <a href="contact.html">Contact</a>
      </nav>
    </div>
  </header>

  <main class="container">
    <h1>Curated used and rare books from a longtime collector</h1>
    <p class="lede">Military history, classic cookery, and rare older titles — sold exclusively through our AbeBooks storefront.</p>

    <a class="btn" href="https://www.abebooks.com/servlet/StoreFrontDisplay?cid=91160525" rel="noopener">Shop on AbeBooks</a>

    <section class="cards">
      <div class="card">
        <h3>Military History</h3>
        <p>Campaigns, regimental histories, memoirs, and reference works spanning the 19th and 20th centuries.</p>
      </div>
      <div class="card">
        <h3>Classic Cookery</h3>
        <p>Mid-century and earlier cookbooks, regional and international titles, and collectible food writing.</p>
      </div>
      <div class="card">
        <h3>Rare &amp; Miscellaneous</h3>
        <p>Scarce older editions, first printings, and curiosities that do not fit the other two shelves.</p>
      </div>
    </section>

    <h2>How ordering works</h2>
    <p>Every MK Books title is listed in our <a href="https://www.abebooks.com/servlet/StoreFrontDisplay?cid=91160525" rel="noopener">AbeBooks storefront</a>. When you place an order:</p>
    <ol>
      <li>AbeBooks handles payment and provides purchase protection through the AbeBooks Buyer Guarantee.</li>
      <li>We pack and ship your order within two business days.</li>
      <li>AbeBooks sets the shipping options, rates, and delivery estimates at checkout.</li>
    </ol>
    <p>See our <a href="policies.html">Policies</a> page for returns, shipping, and terms.</p>
  </main>

  <footer class="site">
    <div>© 2026 MK Books · Mission, British Columbia, Canada</div>
    <div class="links">
      <a href="about.html">About</a>·
      <a href="policies.html">Policies</a>·
      <a href="privacy.html">Privacy</a>·
      <a href="contact.html">Contact</a>
    </div>
  </footer>
</body>
</html>
```

- [ ] **Step 2: Content verification**

Run this check — every required string must appear in `index.html`:

```bash
cd "C:/Users/Michael Kernaghan/mk-books-site"
for s in "MK Books" "Military History" "Classic Cookery" "Rare" "AbeBooks" "91160525" "two business days" "Buyer Guarantee" "Mission, British Columbia, Canada"; do
  grep -q "$s" index.html && echo "OK: $s" || echo "MISSING: $s"
done
```

Expected: every line prefixed `OK:`. If anything says `MISSING:`, fix before continuing.

- [ ] **Step 3: Visual preview**

```bash
start chrome "file:///C:/Users/Michael Kernaghan/mk-books-site/index.html"
```

Confirm: header visible, hero text readable, button shown in accent color, three category cards in a row on wide viewport, footer at bottom.

- [ ] **Step 4: Stage and present commit**

```bash
git -C "C:/Users/Michael Kernaghan/mk-books-site" add index.html
```

Present:

```bash
git -C "C:/Users/Michael Kernaghan/mk-books-site" commit -m "feat: add home page"
```

---

## Task 4: Build `about.html`

**Files:**
- Create: `C:/Users/Michael Kernaghan/mk-books-site/about.html`

- [ ] **Step 1: Write the about page**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>About — MK Books</title>
  <meta name="description" content="MK Books is a Canadian sole proprietorship run by Michael Kernaghan in Mission, British Columbia.">
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <header class="site">
    <div class="wrap">
      <a class="brand" href="index.html">MK Books</a>
      <nav>
        <a href="about.html">About</a>
        <a href="policies.html">Policies</a>
        <a href="privacy.html">Privacy</a>
        <a href="contact.html">Contact</a>
      </nav>
    </div>
  </header>

  <main class="container">
    <h1>About MK Books</h1>
    <p class="lede">A small, owner-run bookseller in Mission, British Columbia, Canada.</p>

    <p>MK Books is a sole proprietorship operated by Michael Kernaghan. The business grew out of a personal library of several hundred titles accumulated over many years — military history, classic cookery, and a steady trickle of older and unusual books. Rather than let those volumes sit in boxes, we are listing the best of them for other readers and collectors.</p>

    <h2>What we carry</h2>
    <ul>
      <li><strong>Military history</strong> — regimental histories, campaign studies, memoirs, and reference works, with a bias toward 19th- and 20th-century conflicts.</li>
      <li><strong>Classic cookery</strong> — mid-century and earlier cookbooks, regional and international titles, and collectible food writing.</li>
      <li><strong>Rare and miscellaneous</strong> — scarce editions, early printings, and older titles outside the two main categories.</li>
    </ul>

    <h2>How we work</h2>
    <p>Every book is inspected and described by hand before it is listed. We grade condition conservatively, flag known flaws, and pack for safe transit. We list exclusively through AbeBooks, which handles payment, provides the AbeBooks Buyer Guarantee, and sets shipping at checkout.</p>

    <h2>Storefront</h2>
    <p>Our AbeBooks storefront ID is <strong>91160525</strong>. Browse the current inventory at <a href="https://www.abebooks.com/servlet/StoreFrontDisplay?cid=91160525" rel="noopener">abebooks.com/servlet/StoreFrontDisplay?cid=91160525</a>.</p>
  </main>

  <footer class="site">
    <div>© 2026 MK Books · Mission, British Columbia, Canada</div>
    <div class="links">
      <a href="about.html">About</a>·
      <a href="policies.html">Policies</a>·
      <a href="privacy.html">Privacy</a>·
      <a href="contact.html">Contact</a>
    </div>
  </footer>
</body>
</html>
```

- [ ] **Step 2: Content verification**

```bash
cd "C:/Users/Michael Kernaghan/mk-books-site"
for s in "About MK Books" "sole proprietorship" "Michael Kernaghan" "Mission, British Columbia, Canada" "91160525" "AbeBooks Buyer Guarantee"; do
  grep -q "$s" about.html && echo "OK: $s" || echo "MISSING: $s"
done
```

Expected: all `OK:`.

- [ ] **Step 3: Visual preview**

```bash
start chrome "file:///C:/Users/Michael Kernaghan/mk-books-site/about.html"
```

Confirm: nav highlights work, headings render, lists readable.

- [ ] **Step 4: Stage and present commit**

```bash
git -C "C:/Users/Michael Kernaghan/mk-books-site" add about.html
```

Present:

```bash
git -C "C:/Users/Michael Kernaghan/mk-books-site" commit -m "feat: add about page"
```

---

## Task 5: Build `policies.html`

**Files:**
- Create: `C:/Users/Michael Kernaghan/mk-books-site/policies.html`

- [ ] **Step 1: Write the policies page**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Policies — MK Books</title>
  <meta name="description" content="Returns, shipping, and terms of service for MK Books. All sales are fulfilled through AbeBooks.">
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <header class="site">
    <div class="wrap">
      <a class="brand" href="index.html">MK Books</a>
      <nav>
        <a href="about.html">About</a>
        <a href="policies.html">Policies</a>
        <a href="privacy.html">Privacy</a>
        <a href="contact.html">Contact</a>
      </nav>
    </div>
  </header>

  <main class="container">
    <h1>Policies</h1>
    <p class="lede">All MK Books sales are fulfilled through AbeBooks. The AbeBooks Buyer Guarantee covers every transaction.</p>
    <p class="meta">Last updated: 19 April 2026</p>

    <h2>Returns &amp; Refunds</h2>
    <p>All sales are fulfilled through AbeBooks and are subject to the <a href="https://www.abebooks.com/docs/HelpCentral/buyerIndex.shtml" rel="noopener">AbeBooks Buyer Guarantee</a>. Returns and refunds are handled per AbeBooks' standard policy. In the usual case:</p>
    <ul>
      <li>If a book is materially different from its listed description, you may request a return through AbeBooks.</li>
      <li>If a book does not arrive, the AbeBooks Buyer Guarantee provides a full refund.</li>
      <li>Return shipping and restocking terms follow AbeBooks' current policy at the time of the transaction.</li>
    </ul>
    <p>If you have a question before or after purchase, contact us at <a href="contact.html">the address on our contact page</a> and we will respond within two business days.</p>

    <h2>Shipping</h2>
    <p>Orders placed through our AbeBooks storefront are packed and shipped within <strong>two business days</strong>. Shipping options, rates, carriers, and delivery estimates are set by AbeBooks at checkout; we do not operate a separate shipping channel.</p>
    <p>We ship from Mission, British Columbia, Canada. AbeBooks restricts the destinations we offer; please consult the storefront for current availability.</p>

    <h2>Terms of Service</h2>
    <p>MK Books is a sole proprietorship based in Mission, British Columbia, Canada, operated by Michael Kernaghan. By purchasing from our AbeBooks storefront you agree to the following:</p>
    <ul>
      <li>All transactions are processed by AbeBooks and are additionally governed by <a href="https://www.abebooks.com/docs/Policies/termsconditions.shtml" rel="noopener">AbeBooks' terms and conditions</a>.</li>
      <li>MK Books reserves the right to cancel orders in the event of pricing errors, inventory unavailability, or suspected fraud. In such cases any payment taken will be refunded in full through AbeBooks.</li>
      <li>Book descriptions are made in good faith. If we have misdescribed a book, the return and refund path is through AbeBooks as described above.</li>
      <li>Nothing on this website constitutes a separate contract of sale; the contract is formed at AbeBooks checkout.</li>
    </ul>
  </main>

  <footer class="site">
    <div>© 2026 MK Books · Mission, British Columbia, Canada</div>
    <div class="links">
      <a href="about.html">About</a>·
      <a href="policies.html">Policies</a>·
      <a href="privacy.html">Privacy</a>·
      <a href="contact.html">Contact</a>
    </div>
  </footer>
</body>
</html>
```

- [ ] **Step 2: Content verification**

```bash
cd "C:/Users/Michael Kernaghan/mk-books-site"
for s in "Returns" "Shipping" "Terms of Service" "AbeBooks Buyer Guarantee" "two business days" "Mission, British Columbia, Canada" "sole proprietorship"; do
  grep -q "$s" policies.html && echo "OK: $s" || echo "MISSING: $s"
done
```

Expected: all `OK:`.

- [ ] **Step 3: Visual preview**

```bash
start chrome "file:///C:/Users/Michael Kernaghan/mk-books-site/policies.html"
```

Confirm: three clearly separated H2 sections, all three AbeBooks links open in new window (`rel=noopener` present).

- [ ] **Step 4: Stage and present commit**

```bash
git -C "C:/Users/Michael Kernaghan/mk-books-site" add policies.html
```

Present:

```bash
git -C "C:/Users/Michael Kernaghan/mk-books-site" commit -m "feat: add policies page"
```

---

## Task 6: Build `privacy.html`

**Files:**
- Create: `C:/Users/Michael Kernaghan/mk-books-site/privacy.html`

- [ ] **Step 1: Write the privacy page**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Privacy — MK Books</title>
  <meta name="description" content="MK Books does not collect visitor data on this website. Purchase data is handled by AbeBooks.">
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <header class="site">
    <div class="wrap">
      <a class="brand" href="index.html">MK Books</a>
      <nav>
        <a href="about.html">About</a>
        <a href="policies.html">Policies</a>
        <a href="privacy.html">Privacy</a>
        <a href="contact.html">Contact</a>
      </nav>
    </div>
  </header>

  <main class="container">
    <h1>Privacy Policy</h1>
    <p class="meta">Last updated: 19 April 2026</p>

    <h2>What this website collects</h2>
    <p>Nothing. This website does not use analytics, advertising trackers, or cookies. We do not operate any forms or accounts on this site, and we do not log visitor behaviour.</p>

    <h2>Email correspondence</h2>
    <p>If you contact us by email using the address on our <a href="contact.html">Contact</a> page, we use your message and email address solely to respond to your inquiry. We do not add correspondents to any mailing list.</p>

    <h2>Purchases on AbeBooks</h2>
    <p>Every purchase from MK Books is completed on AbeBooks. AbeBooks collects and processes the personal and payment information required to fulfil an order. That information is governed by <a href="https://www.abebooks.com/docs/Policies/privacypolicy.shtml" rel="noopener">AbeBooks' privacy policy</a>, not this one.</p>
    <p>When AbeBooks provides us with a shipping address and name in order to fulfil an order, we use that information only to pack and ship the book, and we retain it for the period required for tax and record-keeping purposes in British Columbia, Canada.</p>

    <h2>Third parties</h2>
    <p>This site is hosted on Netlify. Netlify may log incoming requests for the purposes of operating its service; see <a href="https://www.netlify.com/privacy/" rel="noopener">Netlify's privacy policy</a> for details. We do not receive or process those logs.</p>

    <h2>Contact</h2>
    <p>Privacy questions can be sent to the email address on our <a href="contact.html">Contact</a> page.</p>
  </main>

  <footer class="site">
    <div>© 2026 MK Books · Mission, British Columbia, Canada</div>
    <div class="links">
      <a href="about.html">About</a>·
      <a href="policies.html">Policies</a>·
      <a href="privacy.html">Privacy</a>·
      <a href="contact.html">Contact</a>
    </div>
  </footer>
</body>
</html>
```

- [ ] **Step 2: Content verification**

```bash
cd "C:/Users/Michael Kernaghan/mk-books-site"
for s in "Privacy Policy" "does not use analytics" "cookies" "AbeBooks' privacy policy" "Netlify" "British Columbia, Canada"; do
  grep -q "$s" privacy.html && echo "OK: $s" || echo "MISSING: $s"
done
```

Expected: all `OK:`.

- [ ] **Step 3: Visual preview**

```bash
start chrome "file:///C:/Users/Michael Kernaghan/mk-books-site/privacy.html"
```

- [ ] **Step 4: Stage and present commit**

```bash
git -C "C:/Users/Michael Kernaghan/mk-books-site" add privacy.html
```

Present:

```bash
git -C "C:/Users/Michael Kernaghan/mk-books-site" commit -m "feat: add privacy page"
```

---

## Task 7: Build `contact.html`

**Files:**
- Create: `C:/Users/Michael Kernaghan/mk-books-site/contact.html`

**Before writing this file**, confirm with the user:

- Phone number to publish (the owner has agreed to show one but has not yet provided the digits)
- Confirm the email `michael.kernaghan@gmail.com` is still the correct address, or swap for a dedicated alias

Do not leave placeholder strings like `TBD` or `555-` in the committed file.

- [ ] **Step 1: Write the contact page** (replace `PHONE_NUMBER_HERE` with the confirmed value before writing)

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Contact — MK Books</title>
  <meta name="description" content="Contact MK Books. Based in Mission, British Columbia, Canada.">
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <header class="site">
    <div class="wrap">
      <a class="brand" href="index.html">MK Books</a>
      <nav>
        <a href="about.html">About</a>
        <a href="policies.html">Policies</a>
        <a href="privacy.html">Privacy</a>
        <a href="contact.html">Contact</a>
      </nav>
    </div>
  </header>

  <main class="container">
    <h1>Contact</h1>
    <p class="lede">Questions about a listing, a shipment, or a title you are hunting? Send us a note.</p>

    <h2>Business</h2>
    <p><strong>MK Books</strong><br>
    Sole proprietorship<br>
    Mission, British Columbia, Canada</p>

    <h2>Email</h2>
    <p><a href="mailto:michael.kernaghan@gmail.com">michael.kernaghan [at] gmail [dot] com</a></p>
    <p class="meta">We respond within two business days.</p>

    <h2>Phone</h2>
    <p><a href="tel:PHONE_NUMBER_HERE">PHONE_NUMBER_HERE</a></p>

    <h2>Storefront</h2>
    <p>Browse current inventory at our <a href="https://www.abebooks.com/servlet/StoreFrontDisplay?cid=91160525" rel="noopener">AbeBooks storefront</a> (store ID 91160525).</p>
  </main>

  <footer class="site">
    <div>© 2026 MK Books · Mission, British Columbia, Canada</div>
    <div class="links">
      <a href="about.html">About</a>·
      <a href="policies.html">Policies</a>·
      <a href="privacy.html">Privacy</a>·
      <a href="contact.html">Contact</a>
    </div>
  </footer>
</body>
</html>
```

Replace both instances of `PHONE_NUMBER_HERE` with the confirmed phone number before saving. Format the visible text in human-readable form (e.g., `+1 604 555 0123`); format the `tel:` href as `tel:+16045550123`.

- [ ] **Step 2: Content verification**

```bash
cd "C:/Users/Michael Kernaghan/mk-books-site"
for s in "MK Books" "Mission, British Columbia, Canada" "michael.kernaghan" "gmail" "two business days" "91160525"; do
  grep -q "$s" contact.html && echo "OK: $s" || echo "MISSING: $s"
done

# Fail if placeholder tokens leaked in
grep -n "PHONE_NUMBER_HERE\|TBD\|TODO" contact.html && echo "FAIL: placeholder still in file" || echo "OK: no placeholders"
```

Expected: all content lines `OK:`, placeholder check says `OK: no placeholders`.

- [ ] **Step 3: Visual preview**

```bash
start chrome "file:///C:/Users/Michael Kernaghan/mk-books-site/contact.html"
```

Confirm: clicking the email opens the user's mail client to a new message; clicking the phone number invokes the dialer on mobile (not testable on desktop but the `tel:` link should be present).

- [ ] **Step 4: Stage and present commit**

```bash
git -C "C:/Users/Michael Kernaghan/mk-books-site" add contact.html
```

Present:

```bash
git -C "C:/Users/Michael Kernaghan/mk-books-site" commit -m "feat: add contact page"
```

---

## Task 8: Cross-site verification

**Files:** none created — verification only.

- [ ] **Step 1: Link integrity — every internal href resolves**

```bash
cd "C:/Users/Michael Kernaghan/mk-books-site"
for page in index.html about.html policies.html privacy.html contact.html; do
  echo "--- $page ---"
  # Extract local hrefs, skip external and mailto/tel
  grep -oE 'href="[^"]+"' "$page" \
    | sed -E 's/href="([^"]+)"/\1/' \
    | grep -vE '^(https?:|mailto:|tel:|#)' \
    | sort -u \
    | while read target; do
        if [ -f "$target" ]; then
          echo "OK: $page -> $target"
        else
          echo "BROKEN: $page -> $target"
        fi
      done
done
```

Expected: every line `OK:`. Any `BROKEN:` line is a stop-the-line bug.

- [ ] **Step 2: AbeBooks storefront URL is identical across every page**

```bash
grep -n "StoreFrontDisplay" *.html
```

Expected: every occurrence is exactly `https://www.abebooks.com/servlet/StoreFrontDisplay?cid=91160525`. No typos in the store ID.

- [ ] **Step 3: Mobile layout sanity check**

```bash
start chrome --window-size=375,812 "file:///C:/Users/Michael Kernaghan/mk-books-site/index.html"
```

Click through every page. Confirm the nav wraps gracefully on narrow viewports and the category cards stack vertically.

- [ ] **Step 4: No console errors**

Open DevTools on `index.html` and each other page. Expected: no errors in the Console tab, no failed resource requests in the Network tab.

- [ ] **Step 5: If any issue found, fix it and commit as a follow-up**

If all checks pass, no commit needed for this task.

---

## Task 9: Create GitHub repo and push

**Files:** none in the working tree — remote action only.

- [ ] **Step 1: Create the public repo via `gh`**

```bash
gh repo create michaelkernaghan/mk-books-site \
  --public \
  --description "MK Books public business website (Stripe activation site)" \
  --source "C:/Users/Michael Kernaghan/mk-books-site" \
  --remote origin
```

Expected: `gh` reports the repo URL. Do not pass `--push` — the user's git-safety rules require manual push.

- [ ] **Step 2: Verify remote**

```bash
git -C "C:/Users/Michael Kernaghan/mk-books-site" remote -v
```

Expected: two lines pointing at `https://github.com/michaelkernaghan/mk-books-site.git` (fetch + push).

- [ ] **Step 3: Present push command to user**

```bash
git -C "C:/Users/Michael Kernaghan/mk-books-site" push -u origin main
```

Wait for the user to run it and confirm the push succeeded.

- [ ] **Step 4: Verify the repo contents in the browser**

```bash
start chrome "https://github.com/michaelkernaghan/mk-books-site"
```

Confirm: all five HTML files, `styles.css`, `netlify.toml`, `README.md`, and `docs/superpowers/` are visible in the repo view.

---

## Task 10: Connect Netlify and verify initial deploy

**Files:** none in the working tree — Netlify dashboard action.

- [ ] **Step 1: Open Netlify "Add new site" flow**

```bash
start chrome "https://app.netlify.com/start/repos"
```

Ask the user to:
1. Click **Import from Git** → **GitHub**
2. Select repository `michaelkernaghan/mk-books-site`
3. Branch: `main`
4. Build command: *(leave blank)*
5. Publish directory: `.`
6. Click **Deploy**

- [ ] **Step 2: Confirm deploy succeeded**

Wait for the Netlify dashboard to show **Published**. Note the auto-generated `*.netlify.app` URL.

- [ ] **Step 3: Verify the live site on the Netlify subdomain**

Ask the user for the subdomain URL, then:

```bash
start chrome "https://<subdomain>.netlify.app"
```

Click every nav link and confirm all five pages load over HTTPS with no mixed-content warnings. Hit the "Shop on AbeBooks" button from the home page and confirm it opens the real storefront.

- [ ] **Step 4: Rename the Netlify site (optional, cosmetic)**

Have the user go to **Site configuration → Change site name** and pick `mk-books` (or similar) to make the interim URL less random.

---

## Task 11: Register custom `.ca` domain and configure DNS

**Files:** none in the working tree — external action.

- [ ] **Step 1: Check availability of candidate domains**

```bash
start chrome "https://www.google.com/search?q=mkbooks.ca+whois"
```

Check, in order of preference:
1. `mkbooks.ca`
2. `mkbookstore.ca`
3. `mkrarebooks.ca`
4. `mk-books.ca`

Have the user pick one that is available and register it (via Netlify Domains, a Canadian registrar like Rebel or Namespro, or any `.ca`-authorized registrar).

- [ ] **Step 2: Add the custom domain in Netlify**

Netlify dashboard → **Domain management** → **Add a domain** → enter the chosen domain.

- [ ] **Step 3: Point DNS at Netlify**

Two options, pick one:
- **Netlify DNS**: transfer DNS to Netlify by updating the nameservers at the registrar to the four Netlify nameservers shown in the Netlify dashboard.
- **External DNS**: at the registrar, create an `A` record for `@` pointing at Netlify's load balancer IP (currently `75.2.60.5`) and a `CNAME` for `www` pointing at the site's `*.netlify.app` hostname.

Netlify DNS is simpler and is the recommended path.

- [ ] **Step 4: Wait for TLS certificate**

Netlify auto-provisions a Let's Encrypt certificate once DNS resolves. This typically takes 5–30 minutes; can take up to 24 hours.

Check status periodically:

```bash
start chrome "https://app.netlify.com/sites/<site-name>/settings/domain#https"
```

- [ ] **Step 5: Verify the site on the custom domain**

```bash
start chrome "https://<chosen-domain>"
```

Confirm:
- Page loads over HTTPS
- Certificate is valid (Netlify / Let's Encrypt)
- Every nav link works on the custom domain
- No mixed content warnings

- [ ] **Step 6: Update the repo `README.md` with the live domain**

Edit `README.md` to add near the top:

```markdown
**Live site:** https://<chosen-domain>
```

Then:

```bash
git -C "C:/Users/Michael Kernaghan/mk-books-site" add README.md
```

Present:

```bash
git -C "C:/Users/Michael Kernaghan/mk-books-site" commit -m "docs: record live domain in README" && git -C "C:/Users/Michael Kernaghan/mk-books-site" push origin main
```

---

## Task 12: Submit to Stripe for account activation

**Files:** none — Stripe dashboard action.

- [ ] **Step 1: Open Stripe account settings**

```bash
start chrome "https://dashboard.stripe.com/settings/account"
```

- [ ] **Step 2: Enter the business website**

In **Business details** → **Business website**, enter the full URL including `https://`:

```
https://<chosen-domain>
```

Save.

- [ ] **Step 3: Complete any remaining activation fields**

Stripe may also ask for:
- Legal business name (the individual's legal name, since this is a sole proprietorship)
- Business address (Mission, BC — full street address)
- SIN or business number (sole prop uses SIN in Canada)
- Bank account for payouts
- Product description (copy from `index.html` hero)

Fill these in but **do not commit anything to the repo** — this is Stripe account data, not website content.

- [ ] **Step 4: Submit for review and record the decision**

Click **Submit for review**. Stripe usually decides within one to three business days. When the decision arrives:
- If approved: done.
- If Stripe requests clarification or more detail, update the relevant page, push, and respond to Stripe with a link to the specific page that now satisfies the request.

- [ ] **Step 5: Final acceptance check**

Walk through the acceptance criteria from the spec and confirm every item:

- [ ] Site is live on the custom `.ca` domain over HTTPS
- [ ] All 5 pages render correctly on desktop and mobile
- [ ] Every Stripe-required element is visible: business description, contact, refund policy, shipping policy, terms of service, privacy policy
- [ ] The AbeBooks storefront link works from at least 3 pages (home, about, contact)
- [ ] No browser console errors, no broken links, no placeholder copy in the source
- [ ] `README.md` documents how to edit and redeploy
- [ ] Stripe account submitted for activation review

Once all six boxes are ticked and Stripe has the submission, the feature is done.

---

## Out of Scope (explicitly not in this plan)

- On-site cart, checkout, or direct Stripe integration (site is informational only)
- Live inventory feed from AbeBooks
- Analytics, cookie banner, visitor tracking
- Contact form backend (mailto only)
- CMS, blog, newsletter
- Any JavaScript beyond the standard HTML `tel:`/`mailto:` behavior
- SEO beyond `<title>` and `<meta name="description">`
- Logo design — plain wordmark is acceptable for v1
