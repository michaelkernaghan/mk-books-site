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
