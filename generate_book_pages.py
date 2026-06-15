"""Generate SEO book pages for mkbookstore.ca from the book-management inventory.

Reads active listings (triage=sell, listed, not sold) from books.json and emits:
  books/<slug>.html   one page per book, with schema.org Book JSON-LD
  books/index.html    catalogue grouped by category
  books/img/<slug>.jpg first photo per book, downscaled
  sitemap.xml, robots.txt at site root

Re-run after any inventory change (sale, new listing, price change), then
rebuild the Netlify Drop zip. Generated output is gitignored - the script is
the source of truth.

Usage: python generate_book_pages.py
"""

import html
import json
import shutil
from pathlib import Path
from urllib.parse import quote_plus

from PIL import Image

SITE = Path(__file__).resolve().parent
INVENTORY = SITE.parent / "book-management" / "inventory" / "books.json"
PHOTOS_ROOT = SITE.parent / "book-management"
OUT_BOOKS = SITE / "books"
OUT_IMG = OUT_BOOKS / "img"

BASE_URL = "https://mkbookstore.ca"
STOREFRONT_ID = "91160525"
STATIC_PAGES = ["index.html", "about.html", "policies.html", "privacy.html", "contact.html"]
MAX_IMG_WIDTH = 800
JPEG_QUALITY = 80

PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title_tag}</title>
  <meta name="description" content="{meta_description}">
  <link rel="canonical" href="{canonical}">
  <link rel="stylesheet" href="../styles.css">
  <script type="application/ld+json">
{json_ld}
  </script>
</head>
<body>
  <header class="site">
    <div class="wrap">
      <a class="brand" href="../index.html">MK Bookstore</a>
      <nav>
        <a href="index.html">Books</a>
        <a href="../about.html">About</a>
        <a href="../policies.html">Policies</a>
        <a href="../contact.html">Contact</a>
      </nav>
    </div>
  </header>

  <main class="container">
    <p class="meta"><a href="index.html">&larr; All books</a></p>
    <h1>{title}</h1>
    <p class="lede">{byline}</p>
{photo_block}
    <p><strong>{price}</strong> &middot; {condition}</p>
{description_block}
    <h2>Details</h2>
    <ul>
{details}
    </ul>
    <p><a class="btn" href="{abebooks_url}" rel="noopener">Buy on AbeBooks</a></p>
    <p class="meta">Sold through our AbeBooks storefront with the AbeBooks Buyer Guarantee. Availability and final shipping rates are shown at checkout.</p>
  </main>

  <footer class="site">
    <div>&copy; 2026 MK Bookstore &middot; Mission, British Columbia, Canada</div>
    <div class="links">
      <a href="index.html">Books</a>&middot;
      <a href="../about.html">About</a>&middot;
      <a href="../policies.html">Policies</a>&middot;
      <a href="../privacy.html">Privacy</a>&middot;
      <a href="../contact.html">Contact</a>
    </div>
  </footer>
</body>
</html>
"""

CATALOG_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Books for Sale — MK Bookstore</title>
  <meta name="description" content="All {count} books currently for sale at MK Bookstore: military history, science and mathematics, literary fiction, and rare older titles. Sold via AbeBooks.">
  <link rel="canonical" href="{base}/books/">
  <link rel="stylesheet" href="../styles.css">
</head>
<body>
  <header class="site">
    <div class="wrap">
      <a class="brand" href="../index.html">MK Bookstore</a>
      <nav>
        <a href="index.html">Books</a>
        <a href="../about.html">About</a>
        <a href="../policies.html">Policies</a>
        <a href="../contact.html">Contact</a>
      </nav>
    </div>
  </header>

  <main class="container">
    <h1>Books for sale</h1>
    <p class="lede">{count} titles currently listed. Every book ships via our <a href="https://www.abebooks.com/servlet/StoreFrontDisplay?cid={storefront}" rel="noopener">AbeBooks storefront</a>.</p>
{sections}
  </main>

  <footer class="site">
    <div>&copy; 2026 MK Bookstore &middot; Mission, British Columbia, Canada</div>
    <div class="links">
      <a href="index.html">Books</a>&middot;
      <a href="../about.html">About</a>&middot;
      <a href="../policies.html">Policies</a>&middot;
      <a href="../privacy.html">Privacy</a>&middot;
      <a href="../contact.html">Contact</a>
    </div>
  </footer>
</body>
</html>
"""


def load_active_books() -> list[dict]:
    data = json.loads(INVENTORY.read_text(encoding="utf-8"))
    books = data if isinstance(data, list) else data["books"]
    return [
        b for b in books
        if b.get("triage") == "sell" and b.get("listed") and not b.get("date_sold")
    ]


def first_photo(book: dict) -> Path | None:
    rel = book.get("photo")
    if not rel:
        return None
    photo_dir = PHOTOS_ROOT / rel
    if not photo_dir.is_dir():
        return None
    files = sorted(
        f for f in photo_dir.iterdir()
        if f.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp")
    )
    return files[0] if files else None


def write_image(book: dict) -> str | None:
    src = first_photo(book)
    if src is None:
        return None
    dest = OUT_IMG / f"{book['slug']}.jpg"
    with Image.open(src) as im:
        im = im.convert("RGB")
        if im.width > MAX_IMG_WIDTH:
            ratio = MAX_IMG_WIDTH / im.width
            im = im.resize((MAX_IMG_WIDTH, round(im.height * ratio)))
        im.save(dest, "JPEG", quality=JPEG_QUALITY, optimize=True)
    return dest.name


def abebooks_url(book: dict) -> str:
    return (
        "https://www.abebooks.com/servlet/SearchResults?vci="
        f"{STOREFRONT_ID}&kn={quote_plus(book['title'])}"
    )


def imprint(book: dict) -> str:
    parts = [book.get("publisher_name") or book.get("publisher")]
    parts.append(book.get("place_published"))
    if book.get("year"):
        parts.append(str(book["year"]))
    return ", ".join(p for p in parts if p)


def meta_description(book: dict) -> str:
    desc = (book.get("description") or "").replace("\n", " ").strip()
    if not desc:
        desc = f"{book['title']} by {book.get('author', '')}. {imprint(book)}."
    if len(desc) > 155:
        desc = desc[:152].rsplit(" ", 1)[0] + "..."
    return desc


def json_ld(book: dict, img_name: str | None) -> str:
    data: dict = {
        "@context": "https://schema.org",
        "@type": "Book",
        "name": book["title"],
        "author": {"@type": "Person", "name": book.get("author") or ""},
        "bookFormat": "https://schema.org/Hardcover"
        if (book.get("binding") or "").lower() == "hardcover"
        else "https://schema.org/Paperback",
        "inLanguage": "en",
        "url": f"{BASE_URL}/books/{book['slug']}.html",
        "offers": {
            "@type": "Offer",
            "price": str(book.get("listed_price") or ""),
            "priceCurrency": "CAD",
            "availability": "https://schema.org/InStock",
            "itemCondition": "https://schema.org/UsedCondition",
            "url": abebooks_url(book),
        },
    }
    if book.get("isbn"):
        data["isbn"] = book["isbn"]
    if book.get("year"):
        data["datePublished"] = str(book["year"])
    if book.get("publisher_name"):
        data["publisher"] = {"@type": "Organization", "name": book["publisher_name"]}
    if book.get("edition"):
        data["bookEdition"] = book["edition"]
    if img_name:
        data["image"] = f"{BASE_URL}/books/img/{img_name}"
    return json.dumps(data, indent=2, ensure_ascii=False)


def details_list(book: dict) -> str:
    rows = [
        ("Publisher", imprint(book)),
        ("Binding", book.get("binding")),
        ("Edition", book.get("edition")),
        ("Condition", (book.get("condition") or "").title()),
        (
            "Dust jacket",
            (book.get("jacket_condition") or "").title() or None,
        ),
        ("ISBN", book.get("isbn")),
        ("Category", (book.get("category") or "").replace("-", " ").title()),
    ]
    return "\n".join(
        f"      <li><strong>{label}:</strong> {html.escape(str(value))}</li>"
        for label, value in rows
        if value
    )


def render_book(book: dict, img_name: str | None) -> str:
    title = html.escape(book["title"])
    author = html.escape(book.get("author") or "")
    byline = f"{author} &middot; {html.escape(imprint(book))}"
    price = f"C${book.get('listed_price')}"
    condition = html.escape((book.get("condition") or "used").title() + " condition")
    paragraphs = [
        f"    <p>{html.escape(p.strip())}</p>"
        for p in (book.get("description") or "").split("\n\n")
        if p.strip()
    ]
    description_block = "\n".join(paragraphs)
    photo_block = (
        f'    <p><img src="img/{img_name}" alt="{title}" '
        'style="max-width:100%;border:1px solid var(--rule);"></p>'
        if img_name
        else ""
    )
    return PAGE_TEMPLATE.format(
        title_tag=f"{title} — {author} | MK Bookstore",
        meta_description=html.escape(meta_description(book)),
        canonical=f"{BASE_URL}/books/{book['slug']}.html",
        json_ld=json_ld(book, img_name),
        title=title,
        byline=byline,
        photo_block=photo_block,
        price=price,
        condition=condition,
        description_block=description_block,
        details=details_list(book),
        abebooks_url=html.escape(abebooks_url(book)),
    )


def render_catalog(books: list[dict]) -> str:
    by_category: dict[str, list[dict]] = {}
    for b in books:
        cat = (b.get("category") or "miscellaneous").replace("-", " ").title()
        by_category.setdefault(cat, []).append(b)
    sections = []
    for cat in sorted(by_category, key=lambda c: -len(by_category[c])):
        items = sorted(
            by_category[cat], key=lambda b: -(b.get("listed_price") or 0)
        )
        rows = "\n".join(
            f'      <li><a href="{b["slug"]}.html">{html.escape(b["title"])}</a>'
            f" — {html.escape(b.get('author') or '')}"
            f" ({b.get('year') or 'n.d.'}) · C${b.get('listed_price')}</li>"
            for b in items
        )
        sections.append(
            f"    <h2>{html.escape(cat)} ({len(items)})</h2>\n    <ul>\n{rows}\n    </ul>"
        )
    return CATALOG_TEMPLATE.format(
        count=len(books),
        base=BASE_URL,
        storefront=STOREFRONT_ID,
        sections="\n".join(sections),
    )


def render_sitemap(books: list[dict]) -> str:
    urls = [f"{BASE_URL}/{p}" for p in STATIC_PAGES]
    urls.append(f"{BASE_URL}/books/")
    urls.extend(f"{BASE_URL}/books/{b['slug']}.html" for b in books)
    entries = "\n".join(f"  <url><loc>{u}</loc></url>" for u in urls)
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{entries}\n</urlset>\n"
    )


def main() -> None:
    books = load_active_books()
    if OUT_BOOKS.exists():
        shutil.rmtree(OUT_BOOKS)
    OUT_IMG.mkdir(parents=True)

    no_photo = []
    for book in books:
        img_name = write_image(book)
        if img_name is None:
            no_photo.append(book["slug"])
        page = render_book(book, img_name)
        (OUT_BOOKS / f"{book['slug']}.html").write_text(page, encoding="utf-8")

    (OUT_BOOKS / "index.html").write_text(render_catalog(books), encoding="utf-8")
    (SITE / "sitemap.xml").write_text(render_sitemap(books), encoding="utf-8")
    (SITE / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nSitemap: {BASE_URL}/sitemap.xml\n", encoding="utf-8"
    )

    print(f"{len(books)} book pages + catalogue + sitemap generated.")
    if no_photo:
        print(f"No photo found for: {', '.join(no_photo)}")


if __name__ == "__main__":
    main()
