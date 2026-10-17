"""Assemble the static pages with a shared header and footer.

Usage: python3 scripts/build.py .
"""
import json, pathlib, sys
from datetime import date
from urllib.parse import quote

OUT = pathlib.Path(sys.argv[1])

SITE = "https://ezekiel-bible-school.vercel.app"
NAME = "Ezekiel Bible Institute"
PHONE = "+233 00 000 0000"          # TODO: real number
PHONE_HREF = "+233000000000"
EMAIL = "admissions@example.com"    # TODO: real address
ADDRESS = {
    "street": "Christian Service Church",
    "locality": "East Legon",
    "city": "Accra",
    "region": "Greater Accra",
    "country": "GH",
}
ADDRESS_LINE = "Christian Service Church, East Legon, Accra, Ghana"
# TODO: set to (latitude, longitude) of the church gate once confirmed.
GEO = None

MAP_QUERY = quote(ADDRESS_LINE)
MAP_EMBED = f"https://maps.google.com/maps?q={MAP_QUERY}&z=15&output=embed"
MAP_LINK = f"https://www.google.com/maps/search/?api=1&query={MAP_QUERY}"

NAV = [("/about", "About"), ("/programmes", "Programmes"), ("/admissions", "Admissions"), ("/hostel", "Hostel"), ("/visit", "Visit")]


def ld(*objects):
    """Render JSON-LD script tags."""
    return "\n".join(
        f'  <script type="application/ld+json">{json.dumps(o, ensure_ascii=False, separators=(",", ":"))}</script>'
        for o in objects
    )


def postal_address():
    return {
        "@type": "PostalAddress",
        "streetAddress": ADDRESS["street"],
        "addressLocality": f'{ADDRESS["locality"]}, {ADDRESS["city"]}',
        "addressRegion": ADDRESS["region"],
        "addressCountry": ADDRESS["country"],
    }


ORG = {
    "@context": "https://schema.org",
    "@type": ["CollegeOrUniversity", "EducationalOrganization"],
    "@id": f"{SITE}/#org",
    "name": NAME,
    "alternateName": ["EBI", "Ezekiel Bible School"],
    "url": f"{SITE}/",
    "logo": f"{SITE}/icon-512.png",
    "image": f"{SITE}/og-image.jpg",
    "description": "Ezekiel Bible Institute is an evangelical, interdenominational Bible school in East Legon, Accra, Ghana. It offers certificate, diploma and degree programmes in Bible, theology and ministry, on campus and online, with hostel accommodation. Ghanaian and international students are welcome.",
    "slogan": "Study Scripture closely. Serve the church well.",
    "foundingDate": "2001",
    "address": postal_address(),
    "hasMap": MAP_LINK,
    "telephone": PHONE,
    "email": EMAIL,
    "knowsLanguage": "en",
    "areaServed": [{"@type": "Country", "name": "Ghana"}, {"@type": "Place", "name": "West Africa"}, {"@type": "Place", "name": "Worldwide (online)"}],
    "amenityFeature": [
        {"@type": "LocationFeatureSpecification", "name": "Student hostel", "value": True},
        {"@type": "LocationFeatureSpecification", "name": "Library", "value": True},
        {"@type": "LocationFeatureSpecification", "name": "Wi-Fi", "value": True},
    ],
    "openingHoursSpecification": [{
        "@type": "OpeningHoursSpecification",
        "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "opens": "08:00",
        "closes": "16:30",
    }],
}
if GEO:
    ORG["geo"] = {"@type": "GeoCoordinates", "latitude": GEO[0], "longitude": GEO[1]}

WEBSITE = {
    "@context": "https://schema.org",
    "@type": "WebSite",
    "@id": f"{SITE}/#website",
    "url": f"{SITE}/",
    "name": NAME,
    "inLanguage": "en-GH",
    "publisher": {"@id": f"{SITE}/#org"},
}


def breadcrumbs(path, title):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": title, "item": f"{SITE}{path}"},
        ],
    }


def faq_ld(items):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in items
        ],
    }


def faq_html(items):
    return "\n".join(f"""          <details>
            <summary>{q}</summary>
            <p>{a}</p>
          </details>""" for q, a in items)

def head(title, desc, path, schema=()):
    full = f"{NAME} | Bible School in East Legon, Accra, Ghana" if path == "/" else f"{title} | {NAME}, Accra"
    geo_meta = f'\n  <meta name="geo.position" content="{GEO[0]};{GEO[1]}">\n  <meta name="ICBM" content="{GEO[0]}, {GEO[1]}">' if GEO else ""
    return f"""<!doctype html>
<html lang="en-GH">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{full}</title>
  <meta name="description" content="{desc}">
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
  <link rel="canonical" href="https://ezekiel-bible-school.vercel.app{path}">
  <meta name="geo.region" content="GH-AA">
  <meta name="geo.placename" content="East Legon, Accra">{geo_meta}
  <meta name="theme-color" content="#fbf9f4">
  <meta property="og:title" content="{full}">
  <meta property="og:description" content="{desc}">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="en_GH">
  <meta property="og:site_name" content="Ezekiel Bible Institute">
  <meta property="og:url" content="https://ezekiel-bible-school.vercel.app{path}">
  <meta property="og:image" content="https://ezekiel-bible-school.vercel.app/og-image.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="Ezekiel Bible Institute: Study Scripture closely. Serve the church well.">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="https://ezekiel-bible-school.vercel.app/og-image.jpg">
  <link rel="icon" href="/favicon.ico" sizes="48x48">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="manifest" href="/site.webmanifest">
  <link rel="alternate" type="text/plain" href="/llms.txt" title="Plain-text summary for AI assistants">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,opsz,wght@0,8..60,300;0,8..60,400;0,8..60,600;1,8..60,300;1,8..60,400&family=Cinzel:wght@500;600&family=Public+Sans:wght@400;500;600&display=swap">
  <link rel="stylesheet" href="/styles.css">
  <script src="/main.js" defer></script>
{ld(*schema)}
</head>"""

def cur(href, path):
    return ' aria-current="page"' if href == path else ""

def header(path):
    links = "\n".join(
        f'        <a href="{href}"{cur(href, path)}>{label}</a>'
        for href, label in NAV
    )
    menu_links = "\n".join(
        f'          <li style="--i: {i}"><a href="{href}"{cur(href, path)}>{label}</a></li>'
        for i, (href, label) in enumerate([("/", "Home")] + NAV + [("/enquire", "Enquire")])
    )
    return f"""<body>
  <svg width="0" height="0" style="position:absolute" aria-hidden="true">
    <symbol id="mark" viewBox="0 0 120 120">
      <path d="M25 76A38 38 0 0 1 51 22.5M95 76A38 38 0 0 0 69 22.5" fill="none" stroke="var(--mark-gold)" stroke-width="4" stroke-linecap="round"/>
      <path d="M58 6h4v7h6v4h-6v7h-4v-7h-6v-4h6Z" fill="var(--mark-fg)"/>
      <path d="M60 24 69 41v6l19 13v22H32V60l19-13v-6Z" fill="var(--mark-fg)"/>
      <path d="M57 50a3 3 0 0 1 6 0v7h-6ZM54 82V71a6 6 0 0 1 12 0v11Z" fill="var(--mark-bg)"/>
      <path d="M8 84q26-8 52 2 26-10 52-2v16q-26-7-52 4-26-11-52-4Z" fill="var(--mark-fg)"/>
      <path d="M14 82q22-8 46 2 24-10 46-2v12q-22-7-46 3-24-10-46-3Z" fill="var(--mark-bg)" stroke="var(--mark-gold)" stroke-width="2"/>
      <path d="M60 84v13" stroke="var(--mark-gold)" stroke-width="2"/>
      <path d="M71 100h7v12l-3.5-3-3.5 3Z" fill="var(--mark-gold)"/>
    </symbol>
  </svg>

  <a class="skip" href="#main">Skip to content</a>

  <div class="notice">
    <div class="wrap notice__inner">
      <p><span class="notice__long">January 2027 applications close</span><span class="notice__short">Applications close</span> <strong>30 November</strong></p>
      <a href="/admissions">Key dates</a>
    </div>
  </div>

  <header class="header">
    <div class="wrap header__inner">
      <a class="logo" href="/" aria-label="Ezekiel Bible Institute, home">
        <svg class="logo__mark" aria-hidden="true"><use href="#mark"/></svg>
        <span class="logo__word">Ezekiel<span>Bible Institute</span></span>
      </a>

      <nav class="nav" aria-label="Primary">
{links}
        <a class="button button--sm" href="/enquire">Enquire</a>
      </nav>

      <button class="burger" type="button" aria-expanded="false" aria-controls="menu">
        <span class="burger__label">Menu</span>
        <span class="burger__icon" aria-hidden="true"><span></span><span></span></span>
      </button>
    </div>
  </header>

  <div class="menu" id="menu">
    <div class="menu__body wrap">
      <nav aria-label="Site">
        <ul class="menu__links">
{menu_links}
        </ul>
      </nav>
      <div class="menu__foot">
        <p class="menu__intake">January 2027 intake<br><span>Applications close 30 November</span></p>
        <p class="menu__contact">
          <a href="tel:{PHONE_HREF}">{PHONE}</a>
          <a href="mailto:{EMAIL}">{EMAIL}</a>
        </p>
      </div>
    </div>
  </div>
"""

FOOTER = f"""
  <footer class="footer">
    <div class="wrap footer__grid">
      <div class="footer__about">
        <a class="footer__logo" href="/">
          <svg class="logo__mark" aria-hidden="true"><use href="#mark"/></svg>
          <span class="logo__word">Ezekiel<span>Bible Institute</span></span>
        </a>
        <address>Christian Service Church<br>East Legon, Accra, Ghana</address>
        <p><a href="tel:{PHONE_HREF}">{PHONE}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p>
        <p><a href="{MAP_LINK}" rel="noopener">Get directions</a></p>
      </div>
      <nav class="footer__nav" aria-label="Footer">
        <div>
          <h2>Study</h2>
          <ul>
            <li><a href="/programmes">Programmes</a></li>
            <li><a href="/admissions">Admissions</a></li>
            <li><a href="/admissions#fees">Fees and bursaries</a></li>
            <li><a href="/enquire">Request a prospectus</a></li>
          </ul>
        </div>
        <div>
          <h2>Institute</h2>
          <ul>
            <li><a href="/about">About</a></li>
            <li><a href="/about#faculty">Faculty</a></li>
            <li><a href="/visit">Events</a></li>
            <li><a href="/hostel">Hostel</a></li>
            <li><a href="/admissions#international">International students</a></li>
            <li><a href="/visit#find-us">Find us</a></li>
          </ul>
        </div>
      </nav>
    </div>
    <div class="wrap footer__base">
      <p>&copy; <span data-year>2026</span> Ezekiel Bible Institute</p>
      <p class="footer__verse">“I will give you a new heart.” <span>Ezekiel 36:26</span></p>
    </div>
  </footer>
</body>
</html>
"""

def page_head(crumb, title, intro):
    return f"""
    <header class="page-head">
      <div class="wrap">
        <p class="crumb"><a href="/">Home</a> <span aria-hidden="true">/</span> {crumb}</p>
        <h1>{title}</h1>
        <p class="page-head__intro">{intro}</p>
      </div>
    </header>
"""

CTA = """
    <section class="cta">
      <svg class="cta__mark" aria-hidden="true"><use href="#mark"/></svg>
      <div class="wrap cta__inner">
        <h2>Applications for January close on 30 November.</h2>
        <div class="cta__actions">
          <a class="button button--light" href="/enquire">Request a prospectus</a>
          <a class="link-arrow link-arrow--light" href="/visit">Come to open day</a>
        </div>
      </div>
    </section>
"""

PROGRAMMES = [
    ("Certificate in Biblical Studies", "Old and New Testament survey, Christian doctrine, prayer and the spiritual disciplines.", "1 year", "Campus, online", "$1,200", "campus online"),
    ("Diploma in Pastoral Ministry", "Preaching, pastoral care and church leadership, with a supervised placement.", "2 years", "Campus", "$1,850", "campus"),
    ("Bachelor of Theology", "Greek and Hebrew, systematic theology, church history and hermeneutics.", "3 years", "Campus, online", "$2,400", "campus online"),
    ("Diploma in Missions", "Cross-cultural ministry and church planting. Includes a three-week field trip.", "18 months", "Online", "$1,500", "online"),
    ("Certificate in Biblical Counselling", "Care for individuals and families, grounded in Scripture.", "6 months", "Campus, online", "$650", "campus online"),
    ("Evening School of Discipleship", "A short course for church members. Tuesday evenings, no entry requirements.", "12 weeks", "Online", "$120", "online"),
]

def prog_rows(items):
    return "\n".join(f"""            <tr data-modes="{m}">
              <th scope="row"><a href="/enquire?programme={n.replace(' ', '+')}">{n}</a><span>{d}</span></th>
              <td>{l}</td>
              <td>{mode}</td>
              <td>{fee}</td>
            </tr>""" for n, d, l, mode, fee, m in items)

def prog_table(items, caption_hidden=True):
    return f"""        <table class="programmes">
          <thead>
            <tr>
              <th scope="col">Programme</th>
              <th scope="col">Length</th>
              <th scope="col">Mode</th>
              <th scope="col">Per year</th>
            </tr>
          </thead>
          <tbody>
{prog_rows(items)}
          </tbody>
        </table>"""

# Hero background photos, in order. Files live in img/. Leave empty for the
# plain navy background.
HERO_IMAGES = []

def hero_slides():
    return "\n".join(
        f'        <div class="hero__slide{" is-active" if i == 0 else ""}" style="background-image: url(/img/{name})"></div>'
        for i, name in enumerate(HERO_IMAGES)
    )

# ---------------------------------------------------------------- pages

HOME_FAQ = [
    ("Where is Ezekiel Bible Institute located?",
     "Ezekiel Bible Institute meets at Christian Service Church in East Legon, Accra, in the Greater Accra Region of Ghana. Online students can study from anywhere in the world."),
    ("Does Ezekiel Bible Institute accept international students?",
     "Yes. Students from outside Ghana are welcome on every programme, on campus in Accra or online. We issue admission letters for visa applications and can arrange airport pickup from Kotoka International Airport."),
    ("Is there hostel accommodation?",
     "Yes. The institute runs a student hostel on site in East Legon, with furnished shared rooms, Wi-Fi, study space and security. Rooms are open to Ghanaian and international students."),
    ("What programmes are offered?",
     "Certificates in Biblical Studies and Biblical Counselling, diplomas in Pastoral Ministry and Missions, a three-year Bachelor of Theology and a twelve-week Evening School of Discipleship."),
]

EVENTS = [
    ("2026-11-07", "Open day", "Sit in on a class, have lunch with students and meet the faculty.", "10:00", "15:00", "offline"),
    ("2026-11-21", "Online information evening", "For anyone considering online study, in Ghana or abroad. On Zoom.", "18:00", "19:00", "online"),
    ("2026-12-05", "Graduation service", "The class of 2026 is commissioned. Families and churches welcome.", "15:00", "17:00", "offline"),
]


def events_ld():
    out = []
    for day, name, desc, start, end, mode in EVENTS:
        ev = {
            "@context": "https://schema.org",
            "@type": "Event",
            "name": f"{name}, {NAME}",
            "description": desc,
            "startDate": f"{day}T{start}:00+00:00",
            "endDate": f"{day}T{end}:00+00:00",
            "eventStatus": "https://schema.org/EventScheduled",
            "organizer": {"@id": f"{SITE}/#org"},
            "isAccessibleForFree": True,
        }
        if mode == "online":
            ev["eventAttendanceMode"] = "https://schema.org/OnlineEventAttendanceMode"
            ev["location"] = {"@type": "VirtualLocation", "url": f"{SITE}/enquire"}
        else:
            ev["eventAttendanceMode"] = "https://schema.org/OfflineEventAttendanceMode"
            ev["location"] = {"@type": "Place", "name": ADDRESS_LINE, "address": postal_address()}
        out.append(ev)
    return out


def courses_ld():
    return {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": f"Programmes at {NAME}",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "item": {
                    "@type": "Course",
                    "name": n,
                    "description": d,
                    "provider": {"@id": f"{SITE}/#org"},
                    "inLanguage": "en",
                    "timeRequired": l,
                    "offers": {"@type": "Offer", "category": "Paid", "price": fee.strip("$").replace(",", ""), "priceCurrency": "USD"},
                    "hasCourseInstance": [
                        {"@type": "CourseInstance", "courseMode": "Onsite" if mm == "campus" else "Online",
                         **({"location": {"@type": "Place", "name": ADDRESS_LINE, "address": postal_address()}} if mm == "campus" else {})}
                        for mm in m.split()
                    ],
                },
            }
            for i, (n, d, l, mode, fee, m) in enumerate(PROGRAMMES)
        ],
    }


HOME = f"""
  <main id="main">
    <section class="hero" aria-labelledby="hero-title">
      <div class="hero__media" aria-hidden="true">
{hero_slides()}
        <svg class="hero__mark"><use href="#mark"/></svg>
        <svg class="hero__rings" viewBox="0 0 600 600"><circle cx="300" cy="300" r="298"/><circle cx="300" cy="300" r="236"/><circle cx="300" cy="300" r="174"/></svg>
      </div>

      <div class="wrap hero__body">
        <p class="hero__kicker">East Legon, Accra <span aria-hidden="true">·</span> Since 2001</p>
        <h1 id="hero-title" class="hero__title">
          <span class="line"><span>Study Scripture</span></span>
          <span class="line"><span>closely.</span></span>
          <span class="line"><span><em>Serve the church well.</em></span></span>
        </h1>
        <p class="hero__lede">Theological training for pastors, missionaries and church leaders from Ghana and around the world. Live and study on campus in East Legon, Accra, or learn online from anywhere.</p>
        <div class="hero__actions">
          <a class="button button--gold" href="/enquire">Request a prospectus</a>
          <a class="link-arrow link-arrow--light" href="/programmes">Explore programmes</a>
        </div>
        <ul class="hero__tags">
          <li>
            <a href="/admissions#international">
              <svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.6 2.5 3.8 5.5 3.8 9s-1.2 6.5-3.8 9c-2.6-2.5-3.8-5.5-3.8-9S9.4 5.5 12 3Z"/></svg>
              <span><strong>International</strong> All nations</span>
            </a>
          </li>
          <li>
            <a href="/hostel">
              <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 19V6M3 15h18v4M21 15v-2.5A2.5 2.5 0 0 0 18.5 10H11v5"/><circle cx="7" cy="12" r="1.8"/></svg>
              <span><strong>Hostel</strong> On campus</span>
            </a>
          </li>
          <li>
            <a href="/programmes">
              <svg viewBox="0 0 24 24" aria-hidden="true"><rect x="4.5" y="5" width="15" height="10" rx="1"/><path d="M2.5 19h19"/></svg>
              <span><strong>Online</strong> Or on campus</span>
            </a>
          </li>
        </ul>
      </div>

      <div class="wrap hero__foot">
        <dl class="hero__dates">
          <div><dt>Open day</dt><dd>Sat 7 Nov</dd></div>
          <div><dt>Applications close</dt><dd>Mon 30 Nov</dd></div>
          <div><dt>Term begins</dt><dd>Mon 11 Jan</dd></div>
        </dl>
        <a class="hero__scroll" href="#after-hero"><span>Scroll</span></a>
      </div>
    </section>

    <section class="facts" id="after-hero" aria-label="At a glance">
      <ul class="wrap facts__list">
        <li><strong>25</strong> years of teaching</li>
        <li><strong>3,200</strong> graduates in ministry</li>
        <li><strong>41</strong> countries this year</li>
        <li><strong>1 : 12</strong> tutor to student</li>
      </ul>
    </section>

    <section class="section">
      <div class="wrap">
        <div class="section-head">
          <h2>Programmes</h2>
          <a class="link-arrow" href="/programmes">All six programmes</a>
        </div>
{prog_table([PROGRAMMES[0], PROGRAMMES[1], PROGRAMMES[2]])}
      </div>
    </section>

    <section class="section section--tint">
      <div class="wrap">
        <div class="section-head">
          <h2>A home for students from everywhere</h2>
        </div>
        <div class="tiles">
          <a class="tile" href="/hostel">
            <span class="tile__label">Hostel</span>
            <h3>Live where you learn</h3>
            <p>Furnished shared rooms on the church grounds in East Legon, with Wi-Fi, a quiet study room and round-the-clock security. Chapel and classrooms are a short walk away.</p>
            <span class="link-arrow">See the hostel</span>
          </a>
          <a class="tile" href="/admissions#international">
            <span class="tile__label">International</span>
            <h3>Come from anywhere</h3>
            <p>Students join us from across Africa and beyond. We send admission letters for visa applications, meet new arrivals at Kotoka International Airport and help you settle in Accra.</p>
            <span class="link-arrow">For international students</span>
          </a>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="wrap feature">
        <div class="feature__text">
          <h2>Small classes. Serious reading. Real ministry.</h2>
          <p>Most classes meet around a table, not in a lecture hall. From your second term you serve every week with a partner church, so what you learn on Monday is tested by Sunday.</p>
          <a class="link-arrow" href="/about">How we teach</a>
        </div>
        <blockquote class="feature__quote">
          <p>I arrived wanting to preach. I left knowing how to listen to the text first, and to the people in front of me second.</p>
          <footer>Joseph Adebayo <span>Diploma in Pastoral Ministry, 2022</span></footer>
        </blockquote>
      </div>
    </section>

    <section class="section section--tint location" id="location" aria-labelledby="location-title">
      <div class="wrap location__grid">
        <div>
          <h2 id="location-title">Find us in East Legon</h2>
          <address class="location__address">
            Christian Service Church<br>
            East Legon, Accra<br>
            Greater Accra Region, Ghana
          </address>
          <dl class="location__facts">
            <div><dt>From Kotoka Airport</dt><dd>A short drive</dd></div>
            <div><dt>Office hours</dt><dd>Mon – Fri, 08:00 – 16:30 GMT</dd></div>
            <div><dt>Phone</dt><dd><a href="tel:{PHONE_HREF}">{PHONE}</a></dd></div>
          </dl>
          <div class="location__actions">
            <a class="button" href="{MAP_LINK}" rel="noopener">Get directions</a>
            <a class="link-arrow" href="/visit">Plan a visit</a>
          </div>
        </div>
        <div class="map">
          <iframe src="{MAP_EMBED}" title="Map showing Christian Service Church, East Legon, Accra" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="wrap prose-split">
        <h2>Good to know</h2>
        <div class="faq">
{faq_html(HOME_FAQ)}
        </div>
      </div>
    </section>
{CTA}
  </main>
"""

PROGRAMMES_PAGE = page_head("Programmes", "Programmes", "Six programmes, from a twelve-week evening course to a three-year degree. Every one can be started in January or September, on campus in East Legon, Accra, or online.") + f"""
  <main id="main">
    <section class="section section--flush">
      <div class="wrap">
        <div class="filter" role="group" aria-label="Filter by study mode">
          <button type="button" aria-pressed="true" data-mode="all">All</button>
          <button type="button" aria-pressed="false" data-mode="campus">On campus</button>
          <button type="button" aria-pressed="false" data-mode="online">Online</button>
        </div>
{prog_table(PROGRAMMES)}
        <p class="note">Fees are shown in US dollars for international comparison; Ghanaian students can pay in cedis at the current rate. Campus fees include books and lunch. Online students pay 20% less and buy their own textbooks. Hostel rooms are charged separately.</p>
      </div>
    </section>

    <section class="section section--tint">
      <div class="wrap columns">
        <div>
          <h2>Entry requirements</h2>
          <ul class="list">
            <li>A recommendation from your pastor or church leader</li>
            <li>WASSCE or an equivalent secondary qualification for diploma and degree programmes</li>
            <li>English at a level where you can read academic texts comfortably</li>
          </ul>
          <p class="muted">No previous theological study is needed. International qualifications are accepted; if you have studied elsewhere, you may be able to transfer up to a third of a programme.</p>
        </div>
        <div>
          <h2>Studying online</h2>
          <p>Online students follow the same syllabus and are taught by the same faculty. Lectures are recorded; seminars run twice a week at different times so that most time zones are covered.</p>
          <p class="muted">You will need a reliable internet connection and about 15 hours a week for a full-time load.</p>
        </div>
      </div>
    </section>
{CTA}
  </main>
"""

ABOUT = page_head("About", "About the institute", "Ezekiel Bible Institute began in 2001 with eleven students in a borrowed church hall. Today we teach around 400 students a year from Christian Service Church in East Legon, Accra, and online.") + """
  <main id="main">
    <section class="section section--flush">
      <div class="wrap prose-split">
        <h2>What we are for</h2>
        <div class="prose">
          <p>We exist to train people who will teach the Bible faithfully and care for the church well. Most of our graduates go on to serve in local congregations across Ghana and West Africa; others work in mission, chaplaincy, schools and the workplace around the world.</p>
          <p>We are evangelical and interdenominational. Students come from Anglican, Baptist, Pentecostal, Charismatic, Methodist and independent churches, and from many countries. All of them affirm our statement of faith.</p>
        </div>
      </div>
    </section>

    <section class="section section--tint">
      <div class="wrap feature">
        <div class="feature__text">
          <h2>How we teach</h2>
          <p>Classes are small and you will be expected to read a lot, write regularly and explain a passage to people who did not come to hear a lecture.</p>
          <dl class="pillars">
            <div><dt>Scripture</dt><dd>Every student reads the whole Bible in their first year and takes at least one term of Greek.</dd></div>
            <div><dt>Formation</dt><dd>Groups of eight meet weekly with a tutor to pray and talk honestly.</dd></div>
            <div><dt>Practice</dt><dd>From the second term you serve each week with a partner church in Accra.</dd></div>
          </dl>
        </div>
        <figure class="timetable">
          <figcaption>A Tuesday on campus</figcaption>
          <ol>
            <li><time>06:45</time> Morning prayer</li>
            <li><time>08:30</time> Old Testament II</li>
            <li><time>10:15</time> Greek reading class</li>
            <li><time>12:30</time> Lunch</li>
            <li><time>14:00</time> Library</li>
            <li><time>16:30</time> Formation group</li>
            <li><time>19:00</time> Chapel</li>
          </ol>
        </figure>
      </div>
    </section>

    <section class="section" id="faculty">
      <div class="wrap">
        <div class="section-head">
          <h2>Faculty</h2>
          <p>Every full-time teacher also serves in a local church.</p>
        </div>
        <ul class="people">
          <li><h3>Rev. Dr Daniel Adeyemi</h3><p class="people__role">Principal · Old Testament</p><p>Pastored in Ibadan for 18 years before joining the institute.</p></li>
          <li><h3>Dr Grace Mensah</h3><p class="people__role">Academic Dean · New Testament</p><p>Wrote her doctorate on Galatians. Runs the Thursday Greek group.</p></li>
          <li><h3>Pastor Samuel Okafor</h3><p class="people__role">Pastoral Theology</p><p>Planted three churches and now oversees student placements.</p></li>
          <li><h3>Dr Ruth Thompson</h3><p class="people__role">Missions</p><p>Fifteen years in East Africa with a Bible translation team.</p></li>
        </ul>
      </div>
    </section>
""" + CTA + """
  </main>
"""

ADMISSIONS_FAQ = [
    ("Can I study online from another country?", "Yes. Lectures are recorded and seminars run at two times each week so most time zones are covered."),
    ("Do I need to have studied theology before?", "No. The certificate and diploma programmes start from the beginning."),
    ("Can I transfer credit from another college?", "Usually, for up to a third of a programme. Send your transcript with your application and the Dean will review it."),
    ("Can I work while I study?", "Many online and part-time students do. Full-time campus study leaves room for around ten hours of work a week."),
    ("Do international students need a visa to study in Ghana?", "Most do. Once you accept your offer we send an admission letter to support your visa application. Check the requirements for your country with the nearest Ghana embassy or high commission."),
    ("Is there accommodation for students from outside Accra?", "Yes. Our hostel in East Legon has furnished shared rooms for Ghanaian and international students. Rooms are allocated in order of acceptance."),
]

ADMISSIONS = page_head("Admissions", "Admissions", "We look for people who are already serving in their church and want to be better equipped for it. You don’t need a theology background, and you are welcome from any country.") + f"""
  <main id="main">
    <section class="section section--flush">
      <div class="wrap feature">
        <div>
          <h2 class="h3">How to apply</h2>
          <ol class="steps">
            <li><h3>Enquire</h3><p>We send a prospectus and introduce you to an admissions tutor.</p></li>
            <li><h3>Apply</h3><p>A short form, a one-page testimony and your pastor’s letter.</p></li>
            <li><h3>Interview</h3><p>Thirty minutes, in person in East Legon or by video call.</p></li>
            <li><h3>Accept your offer</h3><p>Bursary decisions come with your offer, so you know the full cost first.</p></li>
          </ol>
          <a class="button" href="/enquire">Start with an enquiry</a>
        </div>
        <aside class="intake intake--wide" aria-labelledby="dates-title">
          <h2 id="dates-title">January 2027 intake</h2>
          <dl>
            <div><dt>Open day</dt><dd>Sat 7 Nov</dd></div>
            <div><dt>Applications close</dt><dd>Mon 30 Nov</dd></div>
            <div><dt>Interviews</dt><dd>1 – 11 Dec</dd></div>
            <div><dt>Offers sent</dt><dd>By 18 Dec</dd></div>
            <div><dt>Orientation</dt><dd>Mon 11 Jan</dd></div>
          </dl>
          <p>International applicants: apply by 31 October to leave time for a visa.</p>
        </aside>
      </div>
    </section>

    <section class="section section--dark" id="international">
      <div class="wrap columns">
        <div>
          <h2>International students</h2>
          <p>Students from outside Ghana apply in the same way and are taught alongside Ghanaian classmates. English is the language of teaching.</p>
          <p class="muted">Prefer not to relocate? Every campus programme except the Diploma in Pastoral Ministry can also be taken online.</p>
        </div>
        <div>
          <ul class="list list--light">
            <li>Admission letter to support your student visa application</li>
            <li>Pickup from Kotoka International Airport on arrival</li>
            <li>A room in our East Legon hostel, ready when you land</li>
            <li>Help with a local SIM card, mobile money and banking</li>
            <li>An orientation week covering study, church life and Accra</li>
            <li>Fees quoted in US dollars, so you know the cost in advance</li>
          </ul>
        </div>
      </div>
    </section>

    <section class="section section--tint" id="fees">
      <div class="wrap columns">
        <div>
          <h2>Fees and bursaries</h2>
          <p>Fees are listed with each programme and are charged per year. Campus fees include books and lunch; hostel accommodation is separate.</p>
          <p class="muted">68% of current students receive a bursary. Most awards cover between a quarter and three quarters of fees, and are based on household income and church support.</p>
        </div>
        <div>
          <h2>Accommodation</h2>
          <p>Our hostel on the church grounds in East Legon has furnished shared rooms, Wi-Fi and 24-hour security.</p>
          <a class="link-arrow" href="/hostel">About the hostel</a>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="wrap prose-split">
        <h2>Questions</h2>
        <div class="faq">
{faq_html(ADMISSIONS_FAQ)}
        </div>
      </div>
    </section>
  </main>
"""

HOSTEL_FAQ = [
    ("Who can stay in the hostel?", "Any full-time campus student, from Ghana or abroad. Rooms are allocated in order of acceptance, so apply early if you need one."),
    ("Are men and women housed separately?", "Yes. The hostel has separate wings for men and women, each with its own warden."),
    ("What should I bring?", "Bedding, towels, a reading lamp and personal items. Beds, mattresses, desks and wardrobes are provided."),
    ("Can I stay during the holidays?", "International students can stay over the short breaks by arrangement with the hostel office."),
]

HOSTEL_LD = {
    "@context": "https://schema.org",
    "@type": "Hostel",
    "name": f"{NAME} Student Hostel",
    "description": "Student accommodation for Ezekiel Bible Institute on the grounds of Christian Service Church, East Legon, Accra. Furnished shared rooms for Ghanaian and international students.",
    "url": f"{SITE}/hostel",
    "address": postal_address(),
    "hasMap": MAP_LINK,
    "telephone": PHONE,
    "containedInPlace": {"@id": f"{SITE}/#org"},
    "amenityFeature": [
        {"@type": "LocationFeatureSpecification", "name": n, "value": True}
        for n in ["Furnished rooms", "Wi-Fi", "Study room", "Shared kitchen", "Laundry area", "Running water", "Standby power", "24-hour security"]
    ],
}

HOSTEL = page_head("Hostel", "Hostel accommodation", "A safe, quiet place to live on the grounds of Christian Service Church in East Legon, Accra, a short walk from your classes and the chapel.") + f"""
  <main id="main">
    <section class="section section--flush">
      <div class="wrap feature">
        <div class="feature__text">
          <h2>Live where you learn</h2>
          <p>Most full-time campus students live in the hostel. You eat, pray and study alongside classmates from across Ghana and from other countries, and the first lecture of the day is minutes away.</p>
          <p class="muted">Rooms are shared by two to four students, with separate wings for men and women.</p>
          <a class="button" href="/enquire">Ask about a room</a>
        </div>
        <aside class="intake intake--wide" aria-labelledby="rooms-title">
          <h2 id="rooms-title">At a glance</h2>
          <dl>
            <div><dt>Location</dt><dd>East Legon, Accra</dd></div>
            <div><dt>Rooms</dt><dd>2 – 4 students</dd></div>
            <div><dt>Wings</dt><dd>Men and women</dd></div>
            <div><dt>Open to</dt><dd>Ghanaian and international</dd></div>
            <div><dt>Wardens</dt><dd>Live on site</dd></div>
          </dl>
          <p>Contact admissions for current room rates.</p>
        </aside>
      </div>
    </section>

    <section class="section section--tint">
      <div class="wrap">
        <div class="section-head">
          <h2>Facilities</h2>
        </div>
        <ul class="amenities">
          <li><h3>Furnished rooms</h3><p>Bed, mattress, desk, chair and wardrobe for every student.</p></li>
          <li><h3>Wi-Fi</h3><p>Throughout the hostel, so you can reach lectures and the library online.</p></li>
          <li><h3>Study room</h3><p>A quiet room open late for reading and writing.</p></li>
          <li><h3>Kitchen</h3><p>A shared kitchen for cooking your own meals.</p></li>
          <li><h3>Laundry</h3><p>A washing and drying area for each wing.</p></li>
          <li><h3>Water and power</h3><p>Running water and standby power for outages.</p></li>
          <li><h3>Security</h3><p>Gated grounds with 24-hour security and resident wardens.</p></li>
          <li><h3>Chapel nearby</h3><p>Morning prayer and evening chapel a short walk away.</p></li>
        </ul>
      </div>
    </section>

    <section class="section">
      <div class="wrap prose-split">
        <h2>Hostel questions</h2>
        <div class="faq">
{faq_html(HOSTEL_FAQ)}
        </div>
      </div>
    </section>
{CTA}
  </main>
"""

VISIT = page_head("Visit", "Visit us", "The best way to know whether Ezekiel is right for you is to spend a day with us in East Legon. You are welcome at any of the events below.") + f"""
  <main id="main">
    <section class="section section--flush">
      <div class="wrap">
        <ul class="events events--full">
          <li>
            <time datetime="2026-11-07"><span>Nov</span> 07</time>
            <div><h3>Open day</h3><p>Sit in on a class, see the hostel, have lunch with students and meet the faculty. 10:00 – 15:00 GMT, Christian Service Church, East Legon.</p></div>
            <a class="link-arrow" href="/enquire">Book a place</a>
          </li>
          <li>
            <time datetime="2026-11-21"><span>Nov</span> 21</time>
            <div><h3>Online information evening</h3><p>For anyone considering online study, in Ghana or abroad. On Zoom at 18:00 GMT, about an hour.</p></div>
            <a class="link-arrow" href="/enquire">Register</a>
          </li>
          <li>
            <time datetime="2026-12-05"><span>Dec</span> 05</time>
            <div><h3>Graduation service</h3><p>The class of 2026 is commissioned. Families and churches welcome. 15:00 GMT.</p></div>
          </li>
          <li>
            <time datetime="2027-01-11"><span>Jan</span> 11</time>
            <div><h3>Orientation week</h3><p>For new students starting in January, including international arrivals.</p></div>
          </li>
        </ul>
      </div>
    </section>

    <section class="section section--tint location" id="find-us">
      <div class="wrap location__grid">
        <div>
          <h2>Find us</h2>
          <address class="location__address">Christian Service Church<br>East Legon, Accra<br>Greater Accra Region, Ghana</address>
          <dl class="hours">
            <div><dt>Monday – Friday</dt><dd>08:00 – 16:30</dd></div>
            <div><dt>Saturday</dt><dd>By appointment</dd></div>
            <div><dt>Sunday</dt><dd>Worship with the church</dd></div>
          </dl>
          <p class="muted">East Legon is a short drive from Kotoka International Airport. Parking is available on the church grounds.</p>
          <div class="location__actions">
            <a class="button" href="{MAP_LINK}" rel="noopener">Get directions</a>
          </div>
        </div>
        <div class="map">
          <iframe src="{MAP_EMBED}" title="Map showing Christian Service Church, East Legon, Accra" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe>
        </div>
      </div>
    </section>
  </main>
"""

ENQUIRE = page_head("Enquire", "Request a prospectus", "Tell us a little about yourself and an admissions tutor will reply within two working days, wherever you are in the world.") + f"""
  <main id="main">
    <section class="section section--flush">
      <div class="wrap enquire">
        <form class="form" id="enquiry-form" novalidate>
          <div class="form__pair">
            <div class="field">
              <label for="f-name">Full name</label>
              <input id="f-name" name="name" autocomplete="name" required>
            </div>
            <div class="field">
              <label for="f-email">Email</label>
              <input id="f-email" name="email" type="email" autocomplete="email" required>
            </div>
          </div>
          <div class="form__pair">
            <div class="field">
              <label for="f-country">Country</label>
              <input id="f-country" name="country" autocomplete="country-name" value="Ghana" required>
            </div>
            <div class="field">
              <label for="f-phone">Phone or WhatsApp <span>Optional</span></label>
              <input id="f-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel">
            </div>
          </div>
          <div class="field">
            <label for="f-programme">Programme</label>
            <select id="f-programme" name="programme" required>
              <option value="">Select a programme</option>
              <option>Certificate in Biblical Studies</option>
              <option>Diploma in Pastoral Ministry</option>
              <option>Bachelor of Theology</option>
              <option>Diploma in Missions</option>
              <option>Certificate in Biblical Counselling</option>
              <option>Evening School of Discipleship</option>
              <option>Not sure yet</option>
            </select>
          </div>
          <fieldset class="field field--choice">
            <legend>Study mode</legend>
            <label><input type="radio" name="mode" value="campus" checked> On campus</label>
            <label><input type="radio" name="mode" value="online"> Online</label>
          </fieldset>
          <fieldset class="field field--choice">
            <legend>Hostel room</legend>
            <label><input type="radio" name="hostel" value="yes"> I need a room</label>
            <label><input type="radio" name="hostel" value="no" checked> Not needed</label>
          </fieldset>
          <div class="field">
            <label for="f-message">Message <span>Optional</span></label>
            <textarea id="f-message" name="message" rows="4"></textarea>
          </div>
          <button class="button" type="submit">Send enquiry</button>
          <p class="form__status" role="status"></p>
        </form>

        <aside class="contact">
          <h2>Prefer to talk?</h2>
          <p><a href="tel:{PHONE_HREF}">{PHONE}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p>
          <p class="muted">The admissions office at Christian Service Church, East Legon, is open 08:00 – 16:30 GMT, Monday to Friday.</p>
        </aside>
      </div>
    </section>
  </main>
"""

NOT_FOUND = page_head("Not found", "We couldn’t find that page.", "It may have moved. Try the <a href=\"/\">homepage</a> or <a href=\"/programmes\">programmes</a>.") + """
  <main id="main"></main>
"""

PAGES = {
    "index.html": ("Home", "Ezekiel Bible Institute is a Bible school in East Legon, Accra, Ghana. Certificate, diploma and degree programmes in theology and ministry, on campus with hostel accommodation or online. International students welcome.", "/", HOME,
                   [ORG, WEBSITE, faq_ld(HOME_FAQ), *events_ld()]),
    "programmes.html": ("Programmes", "Bible and theology programmes in Accra, Ghana: Bachelor of Theology, diplomas in Pastoral Ministry and Missions, and certificates. Study on campus in East Legon or online.", "/programmes", PROGRAMMES_PAGE,
                        [breadcrumbs("/programmes", "Programmes"), courses_ld()]),
    "about.html": ("About", "About Ezekiel Bible Institute: an evangelical, interdenominational Bible school training pastors and church leaders at Christian Service Church, East Legon, Accra, since 2001.", "/about", ABOUT,
                   [breadcrumbs("/about", "About"), ORG]),
    "admissions.html": ("Admissions", "How to apply to Ezekiel Bible Institute in Accra, Ghana: key dates, fees, bursaries, hostel accommodation and support for international students.", "/admissions", ADMISSIONS,
                        [breadcrumbs("/admissions", "Admissions"), faq_ld(ADMISSIONS_FAQ)]),
    "hostel.html": ("Hostel", "Student hostel at Ezekiel Bible Institute, East Legon, Accra: furnished shared rooms, Wi-Fi, study room and 24-hour security for Ghanaian and international students.", "/hostel", HOSTEL,
                    [breadcrumbs("/hostel", "Hostel"), HOSTEL_LD, faq_ld(HOSTEL_FAQ)]),
    "visit.html": ("Visit", "Visit Ezekiel Bible Institute at Christian Service Church, East Legon, Accra, Ghana. Open days, events, directions and office hours.", "/visit", VISIT,
                   [breadcrumbs("/visit", "Visit"), *events_ld()]),
    "enquire.html": ("Enquire", "Request a prospectus from Ezekiel Bible Institute, East Legon, Accra. Ghanaian and international applicants welcome.", "/enquire", ENQUIRE,
                     [breadcrumbs("/enquire", "Enquire")]),
    "404.html": ("Page not found", "Page not found.", "/404", NOT_FOUND, []),
}

for name, (title, desc, path, body, schema) in PAGES.items():
    (OUT / name).write_text(head(title, desc, path, schema) + "\n" + header(path) + body + FOOTER)
    print("wrote", name)

today = date.today().isoformat()
urls = [p for _, _, p, _, _ in PAGES.values() if p != "/404"]
(OUT / "sitemap.xml").write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + "".join(f"  <url><loc>{SITE}{u}</loc><lastmod>{today}</lastmod></url>\n" for u in urls)
    + "</urlset>\n"
)
print("wrote sitemap.xml")
