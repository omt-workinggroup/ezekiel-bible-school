"""Assemble the static pages with a shared header and footer.

Usage: python3 scripts/build.py .
"""
import json, pathlib, sys
from datetime import date
from urllib.parse import quote

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import curriculum as C  # noqa: E402

OUT = pathlib.Path(sys.argv[1])

SITE = "https://ezekiel-bible-school.vercel.app"
NAME = "Ezekiel Bible Institute"
PHONE = "+233 24 398 0162"
PHONE_HREF = "+233243980162"
WHATSAPP = "https://wa.me/233243980162?text=" + quote("Hello, I'd like to know more about Ezekiel Bible Institute.")
# Further lines from the institute's ordination flyer.
OTHER_PHONES = [("024 887 8817", "+233248878817"), ("024 483 8620", "+233244838620"), ("024 371 4862", "+233243714862")]
EMAIL = "admissions@example.com"    # TODO: real address
ADDRESS = {
    "street": "Christian Service Church, Christian Centre, Last Stop",
    "locality": "East Legon",
    "city": "Accra",
    "region": "Greater Accra",
    "country": "GH",
}
ADDRESS_LINE = "Christian Service Church, Christian Centre, Last Stop, East Legon, Accra, Ghana"
ADDRESS_HTML = "Christian Service Church<br>Christian Centre, Last Stop<br>East Legon, Accra, Ghana"
# TODO: set to (latitude, longitude) of the church gate once confirmed.
GEO = None

MAP_QUERY = quote(ADDRESS_LINE)
MAP_EMBED = f"https://maps.google.com/maps?q={MAP_QUERY}&z=15&output=embed"
MAP_LINK = f"https://www.google.com/maps/search/?api=1&query={MAP_QUERY}"

NAV = [("/about", "About"), ("/programmes", "Programmes"), ("/curriculum", "Curriculum"), ("/admissions", "Admissions"), ("/hostel", "Hostel"), ("/visit", "Visit")]


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
    "description": "Ezekiel Bible Institute is an evangelical, interdenominational Bible school in East Legon, Accra, Ghana. It offers six levels of study in Bible, theology and ministry, from a Certificate in Christian Foundations to a PhD, with hostel accommodation. Ghanaian and international students are welcome.",
    "slogan": "Study Scripture closely. Serve the church well.",
    "disambiguatingDescription": C.AIM,
    "foundingDate": "2001",
    "address": postal_address(),
    "hasMap": MAP_LINK,
    "telephone": [PHONE] + [href for _, href in OTHER_PHONES],
    "email": EMAIL,
    "contactPoint": [{
        "@type": "ContactPoint",
        "contactType": "admissions",
        "telephone": PHONE,
        "availableLanguage": ["English"],
        "areaServed": ["GH", "Worldwide"],
    }],
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
        for i, (href, label) in enumerate([("/", "Home")] + NAV + [("/gallery", "Gallery"), ("/enquire", "Enquire")])
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
          <a href="{WHATSAPP}" rel="noopener">Chat on WhatsApp</a>
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
        <address>{ADDRESS_HTML}</address>
        <p><a href="tel:{PHONE_HREF}">{PHONE}</a><br>{"<br>".join(f'<a href="tel:{h}">{n}</a>' for n, h in OTHER_PHONES)}<br><a href="{WHATSAPP}" rel="noopener">WhatsApp</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></p>
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
            <li><a href="/gallery">Gallery</a></li>
            <li><a href="/admissions#international">International students</a></li>
            <li><a href="/visit#find-us">Find us</a></li>
          </ul>
        </div>
      </nav>
    </div>
    <p class="wrap footer__statement" aria-hidden="true">Serve the church <em>well.</em></p>
    <div class="wrap footer__base">
      <p>&copy; <span data-year>2026</span> Ezekiel Bible Institute</p>
      <p class="footer__verse">“I will give you a new heart.” <span>Ezekiel 36:26</span></p>
    </div>
  </footer>
</body>
</html>
"""

RINGS = '<svg class="rings" viewBox="0 0 600 600" aria-hidden="true"><circle cx="300" cy="300" r="298"/><circle cx="300" cy="300" r="236"/><circle cx="300" cy="300" r="174"/></svg>'


def page_head(crumb, title, intro, photo=None):
    bg = f'\n      <div class="page-head__photo" style="background-image: url(/img/photos/{photo}.webp)" aria-hidden="true"></div>' if photo else ""
    return f"""
    <header class="page-head{' page-head--photo' if photo else ''}">{bg}
      {RINGS}
      <div class="wrap">
        <p class="crumb"><a href="/">Home</a> <span aria-hidden="true">/</span> {crumb}</p>
        <h1>{title}</h1>
        <p class="page-head__intro">{intro}</p>
      </div>
    </header>
"""

CTA = f"""
    <section class="cta">
      <svg class="cta__mark" aria-hidden="true"><use href="#mark"/></svg>
      {RINGS}
      <div class="wrap cta__inner">
        <h2>Applications for January close on 30 November.</h2>
        <div class="cta__actions">
          <a class="button button--light" href="/enquire">Request a prospectus</a>
          <a class="link-arrow link-arrow--light" href="/visit">Come to open day</a>
        </div>
      </div>
    </section>
"""

STAGE_LABEL = {"undergraduate": "Undergraduate", "postgraduate": "Postgraduate"}


def semesters_text(lv):
    return f'{lv["semesters"]} semesters' if lv["semesters"] else "Research-led"


def prog_rows(levels):
    return "\n".join(f"""            <tr data-group="{lv['stage']}">
              <th scope="row"><a href="/curriculum#{lv['slug']}"><span class="programmes__level">Level {lv['n']}</span>{lv['name']}</a><span>{lv['purpose']}</span></th>
              <td>{lv['length']}</td>
              <td>{semesters_text(lv)}</td>
              <td>{STAGE_LABEL[lv['stage']]}</td>
            </tr>""" for lv in levels)


def prog_table(levels):
    return f"""        <table class="programmes">
          <thead>
            <tr>
              <th scope="col">Programme</th>
              <th scope="col">Length</th>
              <th scope="col">Structure</th>
              <th scope="col">Stage</th>
            </tr>
          </thead>
          <tbody>
{prog_rows(levels)}
          </tbody>
        </table>"""


def ladder():
    steps = "\n".join(f"""          <li>
            <a href="/curriculum#{lv['slug']}">
              <span class="ladder__n">0{lv['n']}</span>
              <span class="ladder__short">{lv['short']}</span>
              <span class="ladder__len">{lv['length']}</span>
            </a>
          </li>""" for lv in C.LEVELS)
    return f"""        <ol class="ladder">
{steps}
        </ol>"""


def pathway():
    return "\n".join(f'          <li>{step}</li>' for step in C.PATHWAY)


# Hero background photos, in order. Files live in img/. Leave empty for the
# plain navy background.
HERO_IMAGES = ["photos/hero-bishop-wide.webp", "photos/procession.webp", "photos/graduates-in-prayer.webp", "photos/worship.webp", "photos/altar-prayer.webp", "photos/graduating-class.webp"]

def hero_slides():
    return "\n".join(
        f'        <div class="hero__slide{" is-active" if i == 0 else ""}" style="background-image: url(/img/{name})"></div>'
        for i, name in enumerate(HERO_IMAGES)
    )

# ---------------------------------------------------------------- pages

# Photos from the graduation and ordination service at Christian Service Church.
# (file slug, caption). Files live in img/photos/.
PHOTOS = [
    ("graduating-class", "The graduating class with the leadership"),
    ("procession", "The procession into the auditorium"),
    ("graduates-in-prayer", "Graduates in prayer"),
    ("worship", "Worship during the service"),
    ("laying-on-of-hands", "Prayer and laying on of hands"),
    ("altar-prayer", "Graduates kneeling at the altar"),
    ("anointing-horn", "Anointing of a graduate"),
    ("anointing", "Prayer over a graduate"),
    ("addressing-graduates", "A charge to the graduates"),
    ("graduates-seated", "Graduates during the service"),
    ("graduates-seated-2", "Graduates of every age"),
    ("graduate-detail", "Ready for the ceremony"),
    ("graduates-in-line", "Graduates awaiting their certificates"),
    ("graduates-standing", "The class in line"),
    ("graduates-in-prayer-2", "A moment of prayer"),
    ("graduate-portrait", "A graduate with the leadership"),
    ("ministers-before-congregation", "Ministers before the congregation"),
    ("preaching", "The Word preached"),
    ("address", "An address to the congregation"),
    ("address-2", "Teaching from the pulpit"),
    ("lectern", "At the lectern"),
    ("leadership-seated", "Leadership at the service"),
    ("leadership-seated-2", "Leadership at the service"),
    ("leadership-conversation", "Leadership in conversation"),
    ("minister-seated", "A minister at the service"),
    ("ministers-greeting", "Ministers greeting one another"),
]


def figure(slug, caption, cls="", link=None):
    href = link or f"/img/photos/{slug}.webp"
    attr = "" if link else " data-lightbox"
    return f"""<figure class="photo {cls}"><a href="{href}"{attr}><img src="/img/photos/{slug}.webp" alt="{caption}" loading="lazy" decoding="async"></a><figcaption>{caption}</figcaption></figure>"""


def mosaic():
    picks = ["graduating-class", "laying-on-of-hands", "graduates-in-prayer", "worship", "graduates-seated"]
    caps = dict(PHOTOS)
    return "\n".join(f"          {figure(slug, caps[slug], f'mosaic__{i + 1}', link="/gallery")}" for i, slug in enumerate(picks))


COUNTRIES = ['Ghana', 'Nigeria', 'Liberia', 'Sierra Leone', 'Togo', 'Côte d’Ivoire', 'Cameroon', 'Kenya', 'Uganda', 'South Africa', 'Zambia', 'United Kingdom', 'United States', 'Germany']


def countries_band():
    items = "".join(f"<li>{c}</li>" for c in COUNTRIES)
    return f"""
    <section class="nations" aria-label="Where our students come from">
      <p class="wrap nations__label">Our students come from</p>
      <div class="nations__track">
        <ul class="nations__list">{items}</ul>
        <ul class="nations__list" aria-hidden="true">{items}</ul>
      </div>
    </section>
"""


VOICES = [
    ("I arrived wanting to preach. I left knowing how to listen to the text first, and to the people in front of me second.",
     "Joseph Adebayo", "Lagos, Nigeria", "Diploma in Christian Ministry & Biblical Studies, 2022"),
    ("I studied online around a full-time job in Kumasi. My tutor replied to every email, usually the same day, and the seminars felt like a real classroom.",
     "Ama Owusu", "Kumasi, Ghana", "Bachelor of Theology, 2024"),
    ("I had never left Liberia. Someone was waiting for me at Kotoka, my room was ready, and by the second week the hostel felt like family.",
     "Samuel Kollie", "Monrovia, Liberia", "Certificate in Christian Foundations, 2025"),
]


def voices():
    slides = "\n".join(f"""          <figure class="voices__slide{' is-active' if i == 0 else ''}" id="voice-{i + 1}" aria-roledescription="slide" aria-label="{i + 1} of {len(VOICES)}"{'' if i == 0 else ' hidden'}>
            <blockquote><p>{q}</p></blockquote>
            <figcaption><strong>{n}</strong> <span>{place}</span> <span>{prog}</span></figcaption>
          </figure>""" for i, (q, n, place, prog) in enumerate(VOICES))
    return f"""
    <section class="voices" aria-roledescription="carousel" aria-label="Student stories">
      {RINGS}
      <div class="wrap voices__inner">
        <p class="voices__label">Student stories</p>
        <div class="voices__slides" aria-live="polite">
{slides}
        </div>
        <div class="voices__controls">
          <button type="button" class="voices__btn" data-dir="-1" aria-label="Previous story"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg></button>
          <span class="voices__count"><span data-current>01</span> / {len(VOICES):02d}</span>
          <button type="button" class="voices__btn" data-dir="1" aria-label="Next story"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 5l7 7-7 7"/></svg></button>
          <span class="voices__progress" aria-hidden="true"><span></span></span>
        </div>
      </div>
    </section>
"""

HOME_FAQ = [
    ("Where is Ezekiel Bible Institute located?",
     "Ezekiel Bible Institute meets at Christian Service Church in East Legon, Accra, in the Greater Accra Region of Ghana. Online students can study from anywhere in the world."),
    ("Does Ezekiel Bible Institute accept international students?",
     "Yes. Students from outside Ghana are welcome on every programme, on campus in Accra or online. We issue admission letters for visa applications and can arrange airport pickup from Kotoka International Airport."),
    ("Is there hostel accommodation?",
     "Yes. The institute runs a student hostel on site in East Legon, with furnished shared rooms, Wi-Fi, study space and security. Rooms are open to Ghanaian and international students."),
    ("What programmes are offered?",
     "Six levels of study: a Certificate in Christian Foundations, a Diploma in Christian Ministry & Biblical Studies, a Bachelor of Theology / Christian Ministry, a Master of Theology / Christian Ministry, a Doctor of Ministry (DMin) and a PhD in Biblical & Theological Studies."),
    ("What is the teaching approach?",
     "Ezekiel Bible Institute aims for formation, not just information. Every programme develops four dimensions: knowledge, character, competence and calling, and includes supervised ministry practice."),
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
                "position": lv["n"],
                "item": {
                    "@type": "Course",
                    "@id": f"{SITE}/curriculum#{lv['slug']}",
                    "url": f"{SITE}/curriculum#{lv['slug']}",
                    "name": lv["name"],
                    "description": lv["purpose"],
                    "educationalLevel": STAGE_LABEL[lv["stage"]],
                    "timeRequired": lv["length"],
                    "provider": {"@id": f"{SITE}/#org"},
                    "inLanguage": "en",
                    "hasCourseInstance": {
                        "@type": "CourseInstance",
                        "courseMode": "Onsite",
                        "location": {"@type": "Place", "name": ADDRESS_LINE, "address": postal_address()},
                    },
                    "syllabusSections": [
                        {"@type": "Syllabus", "name": term, "description": "; ".join(f"{code} {title}" for code, title, _ in courses)}
                        for term, courses in lv["terms"]
                    ],
                },
            }
            for lv in C.LEVELS
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

      <figure class="hero__portrait">
        <img src="/img/photos/hero-bishop.webp" alt="Speaking at the graduation and ordination service, Christian Service Church, East Legon" width="1440" height="1080" fetchpriority="high">
      </figure>

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
        <li><strong data-count="25">25</strong> years of teaching</li>
        <li><strong data-count="3200">3,200</strong> graduates in ministry</li>
        <li><strong data-count="41">41</strong> countries this year</li>
        <li><strong>1 : 12</strong> tutor to student</li>
      </ul>
    </section>

    <section class="section">
      <div class="wrap">
        <div class="section-head">
          <h2>From Certificate to PhD</h2>
          <a class="link-arrow" href="/curriculum">See the full curriculum</a>
        </div>
        <p class="section-lede">Six levels of study, each building on the last. Start where you are and keep going as far as God calls you.</p>
{ladder()}
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
      <div class="wrap feature feature--statement">
        <h2>Formation, not just information.</h2>
        <div class="feature__text">
          <p>{C.PHILOSOPHY}</p>
          <a class="link-arrow" href="/curriculum#formation">Our formation philosophy</a>
        </div>
      </div>
      <div class="wrap">
        <ol class="pathway" aria-label="The formation pathway">
{pathway()}
        </ol>
      </div>
    </section>
{voices()}
{countries_band()}

    <section class="section" aria-labelledby="life-title">
      <div class="wrap">
        <div class="section-head">
          <h2 id="life-title">Graduation &amp; ordination</h2>
          <a class="link-arrow" href="/gallery">See all photos</a>
        </div>
        <p class="section-lede">Every year our graduates are prayed for, anointed and sent out from Christian Service Church, East Legon.</p>
        <div class="mosaic">
{mosaic()}
        </div>
      </div>
    </section>

    <section class="section section--tint location" id="location" aria-labelledby="location-title">
      <div class="wrap location__grid">
        <div>
          <h2 id="location-title">Find us in East Legon</h2>
          <address class="location__address">{ADDRESS_HTML}</address>
          <dl class="location__facts">
            <div><dt>From Kotoka Airport</dt><dd>A short drive</dd></div>
            <div><dt>Office hours</dt><dd>Mon – Fri, 08:00 – 16:30 GMT</dd></div>
            <div><dt>Call</dt><dd><a href="tel:{PHONE_HREF}">{PHONE}</a></dd></div>
            <div><dt>Also</dt><dd>{" · ".join(f'<a href="tel:{h}">{n}</a>' for n, h in OTHER_PHONES)}</dd></div>
            <div><dt>WhatsApp</dt><dd><a href="{WHATSAPP}" rel="noopener">Send a message</a></dd></div>
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

PROGRAMMES_PAGE = page_head("Programmes", "Programmes", "Six levels of study, from a one-year Certificate in Christian Foundations to a PhD in Biblical &amp; Theological Studies, taught at Christian Service Church in East Legon, Accra.", photo="graduates-seated") + f"""
  <main id="main">
    <section class="section section--flush">
      <div class="wrap">
        <div class="filter" role="group" aria-label="Filter by stage">
          <button type="button" aria-pressed="true" data-group="all">All levels</button>
          <button type="button" aria-pressed="false" data-group="undergraduate">Undergraduate</button>
          <button type="button" aria-pressed="false" data-group="postgraduate">Postgraduate</button>
        </div>
{prog_table(C.LEVELS)}
        <p class="note">Every course, semester by semester, is on the <a href="/curriculum">curriculum page</a>. Contact admissions for current fees; hostel rooms are charged separately.</p>
      </div>
    </section>

    <section class="section section--tint">
      <div class="wrap columns">
        <div>
          <h2>Entry requirements</h2>
          <ul class="list">
            <li>A recommendation from your pastor or church leader, for every level</li>
            <li>Certificate: open to new and growing believers</li>
            <li>Diploma and Bachelor: WASSCE or an equivalent secondary qualification</li>
            <li>Master: a bachelor’s degree, usually in theology or ministry</li>
            <li>DMin: a master’s degree and active ministry experience</li>
            <li>PhD: a master’s degree with a research component</li>
          </ul>
          <p class="muted">International qualifications are accepted. Teaching is in English.</p>
        </div>
        <div>
          <h2>Ministry practicum</h2>
          <p>At every level, students show what they can do, not just what they know. Practicum work includes:</p>
          <ul class="list">
{chr(10).join(f"            <li>{item}</li>" for item in C.PRACTICUM)}
          </ul>
        </div>
      </div>
    </section>
{CTA}
  </main>
"""

ABOUT = page_head("About", "About the institute", "Ezekiel Bible Institute began in 2001 with eleven students in a borrowed church hall. Today we teach around 400 students a year from Christian Service Church in East Legon, Accra, and online.", photo="graduating-class") + f"""
  <main id="main">
    <section class="section section--flush">
      <div class="wrap prose-split">
        <h2>What we are for</h2>
        <div class="prose">
          <p class="prose__lead">{C.AIM}</p>
          <p>Most of our graduates go on to serve in local congregations across Ghana and West Africa; others work in mission, chaplaincy, schools and the workplace around the world.</p>
          <p>We are evangelical and interdenominational. Students come from Anglican, Baptist, Pentecostal, Charismatic, Methodist and independent churches, and from many countries. All of them affirm our statement of faith.</p>
        </div>
      </div>
      <div class="wrap">
        {figure("graduating-class", "The graduating class with the leadership, Christian Service Church, East Legon", "photo--wide", link="/gallery")}
      </div>
    </section>

    <section class="section section--tint">
      <div class="wrap feature">
        <div class="feature__text">
          <h2>How we form students</h2>
          <p>{C.PHILOSOPHY}</p>
          <dl class="pillars pillars--four">
{chr(10).join(f"            <div><dt>{d}</dt><dd>{q}</dd></div>" for d, q in C.DIMENSIONS)}
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
{CTA}
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

ADMISSIONS = page_head("Admissions", "Admissions", "We look for people who are already serving in their church and want to be better equipped for it. You don’t need a theology background, and you are welcome from any country.", photo="procession") + f"""
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
          <p class="muted">Prefer not to relocate? Ask admissions which courses can currently be followed online.</p>
        </div>
        <div>
          <ul class="list list--light">
            <li>Admission letter to support your student visa application</li>
            <li>Pickup from Kotoka International Airport on arrival</li>
            <li>A room in our East Legon hostel, ready when you land</li>
            <li>Help with a local SIM card, mobile money and banking</li>
            <li>An orientation week covering study, church life and Accra</li>
            <li>Fees confirmed in writing before you travel</li>
          </ul>
        </div>
      </div>
    </section>

    <section class="section section--tint" id="fees">
      <div class="wrap columns">
        <div>
          <h2>Fees and bursaries</h2>
          <p>Fees are charged per semester and depend on the level of study. Ask admissions for the current schedule; hostel accommodation is charged separately.</p>
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
          <li><svg class="amenities__icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M3 19V6M3 15h18v4M21 15v-2.5A2.5 2.5 0 0 0 18.5 10H11v5"/><circle cx="7" cy="12" r="1.8"/></svg><h3>Furnished rooms</h3><p>Bed, mattress, desk, chair and wardrobe for every student.</p></li>
          <li><svg class="amenities__icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M2.5 9a14 14 0 0 1 19 0M5.5 12.5a9.5 9.5 0 0 1 13 0M8.6 16a5 5 0 0 1 6.8 0"/><circle cx="12" cy="19" r="1"/></svg><h3>Wi-Fi</h3><p>Throughout the hostel, so you can reach lectures and the library online.</p></li>
          <li><svg class="amenities__icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H12v16H6.5A2.5 2.5 0 0 0 4 21.5ZM20 5.5A2.5 2.5 0 0 0 17.5 3H12v16h5.5a2.5 2.5 0 0 1 2.5 2.5Z"/></svg><h3>Study room</h3><p>A quiet room open late for reading and writing.</p></li>
          <li><svg class="amenities__icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 3v8M5 3v5a2 2 0 0 0 4 0V3M7 11v10M17 21V3c-2 0-3.5 2.5-3.5 6v4H17"/></svg><h3>Kitchen</h3><p>A shared kitchen for cooking your own meals.</p></li>
          <li><svg class="amenities__icon" viewBox="0 0 24 24" aria-hidden="true"><rect x="4" y="3" width="16" height="18" rx="2"/><circle cx="12" cy="13" r="4.5"/><path d="M7.5 6.5h.01M10.5 6.5h.01"/></svg><h3>Laundry</h3><p>A washing and drying area for each wing.</p></li>
          <li><svg class="amenities__icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3s-5.5 6.2-5.5 10a5.5 5.5 0 0 0 11 0C17.5 9.2 12 3 12 3Z"/><path d="m12.8 10-2.3 3.5h3l-2.3 3.5"/></svg><h3>Water and power</h3><p>Running water and standby power for outages.</p></li>
          <li><svg class="amenities__icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3 4.5 6v5.5c0 4.6 3.2 8.3 7.5 9.5 4.3-1.2 7.5-4.9 7.5-9.5V6Z"/><path d="m9 12 2 2 4-4"/></svg><h3>Security</h3><p>Gated grounds with 24-hour security and resident wardens.</p></li>
          <li><svg class="amenities__icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2v5M9.5 4.5h5M6 21v-9l6-5 6 5v9ZM10.5 21v-4a1.5 1.5 0 0 1 3 0v4"/></svg><h3>Chapel nearby</h3><p>Morning prayer and evening chapel a short walk away.</p></li>
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

VISIT = page_head("Visit", "Visit us", "The best way to know whether Ezekiel is right for you is to spend a day with us in East Legon. You are welcome at any of the events below.", photo="ministers-before-congregation") + f"""
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
          <address class="location__address">{ADDRESS_HTML}</address>
          <p class="phones">{" · ".join([f'<a href="tel:{PHONE_HREF}">{PHONE}</a>'] + [f'<a href="tel:{h}">{n}</a>' for n, h in OTHER_PHONES])}</p>
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
{chr(10).join(f"              <option>{lv['name']}</option>" for lv in C.LEVELS)}
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
          <p><a href="tel:{PHONE_HREF}">{PHONE}</a><br>{"<br>".join(f'<a href="tel:{h}">{n}</a>' for n, h in OTHER_PHONES)}<br><a href="mailto:{EMAIL}">{EMAIL}</a></p>
          <a class="button button--whatsapp" href="{WHATSAPP}" rel="noopener"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm5.3 14c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .2-3.3-.7-2.8-1.1-4.5-3.9-4.7-4.1-.1-.2-1.1-1.5-1.1-2.8 0-1.3.7-2 1-2.3.2-.3.5-.3.6-.3h.5c.1 0 .3 0 .5.4l.7 1.6c.1.1.1.3 0 .5l-.3.5-.3.3c-.1.1-.2.3-.1.5.2.3.7 1.1 1.4 1.7 1 .9 1.7 1.1 2 1.2.2.1.4.1.5-.1l.7-.8c.2-.2.3-.2.5-.1l1.5.7c.2.1.3.2.4.3 0 .1 0 .7-.2 1.3Z"/></svg>Chat on WhatsApp</a>
          <p class="muted">The admissions office at Christian Service Church, Christian Centre, Last Stop, East Legon, is open 08:00 – 16:30 GMT, Monday to Friday.</p>
        </aside>
      </div>
    </section>
  </main>
"""

PDF = "/ezekiel-bible-institute-curriculum.pdf"


def course_rows(courses):
    return "\n".join(f"""                <li>
                  <span class="course__code">{code}</span>
                  <span class="course__title">{title}{f'<small>{topics}</small>' if topics else ''}</span>
                </li>""" for code, title, topics in courses)


def level_article(lv):
    terms = "\n".join(f"""            <details class="term"{' open' if i == 0 else ''}>
              <summary><span>{term}</span><span class="term__count">{len(courses)} {'courses' if len(courses) != 1 else 'course'}</span></summary>
              <ul class="courses">
{course_rows(courses)}
              </ul>
            </details>""" for i, (term, courses) in enumerate(lv["terms"]))
    return f"""
        <article class="level" id="{lv['slug']}" aria-labelledby="{lv['slug']}-title">
          <header class="level__head">
            <p class="level__n">Level 0{lv['n']} <span>{STAGE_LABEL[lv['stage']]}</span></p>
            <h2 id="{lv['slug']}-title">{lv['name']}</h2>
            <dl class="level__meta">
              <div><dt>Length</dt><dd>{lv['length']}</dd></div>
              <div><dt>Structure</dt><dd>{semesters_text(lv)}</dd></div>
            </dl>
            <p class="level__purpose">{lv['purpose']}</p>
            <p class="level__outcome">“{lv['outcome']}”</p>
          </header>
          <div class="level__terms">
{terms}
          </div>
        </article>"""


CURRICULUM = page_head("Curriculum", "The curriculum", f"“{C.MOTTO[0]}” {C.MOTTO[1]}. Six levels of study, every course listed semester by semester.", photo="altar-prayer") + f"""
  <main id="main">
    <section class="section section--flush" id="formation">
      <div class="wrap feature feature--statement">
        <h2>Knowledge that becomes conviction, character and service.</h2>
        <div class="feature__text">
          <p>{C.PHILOSOPHY}</p>
          <a class="button" href="{PDF}" download>Download the curriculum (PDF)</a>
        </div>
      </div>
      <div class="wrap">
        <ol class="pathway" aria-label="The formation pathway">
{pathway()}
        </ol>
        <dl class="dimensions">
{chr(10).join(f'          <div><dt>{d}</dt><dd>{q}</dd></div>' for d, q in C.DIMENSIONS)}
        </dl>
      </div>
    </section>

    <section class="section section--tint">
      <div class="wrap curriculum">
        <nav class="curriculum__nav" aria-label="Levels">
          <p>Levels</p>
          <ol>
{chr(10).join(f'            <li><a href="#{lv["slug"]}"><span>0{lv["n"]}</span>{lv["short"]}</a></li>' for lv in C.LEVELS)}
          </ol>
        </nav>
        <div class="curriculum__levels">
{"".join(level_article(lv) for lv in C.LEVELS)}
        </div>
      </div>
    </section>

    <section class="section">
      <div class="wrap columns">
        <div>
          <h2>Ministry practicum &amp; portfolio</h2>
          <p>Students demonstrate ministry competence, not just knowledge, through:</p>
          <ul class="list">
{chr(10).join(f"            <li>{item}</li>" for item in C.PRACTICUM)}
          </ul>
        </div>
        <div>
          <h2>Programme progression</h2>
          <ol class="progression">
{chr(10).join(f'            <li><strong>{lv["short"]}</strong> {lv["outcome"]}</li>' for lv in C.LEVELS)}
          </ol>
        </div>
      </div>
    </section>

    <section class="voices voices--static" aria-labelledby="profile-title">
      {RINGS}
      <div class="wrap voices__inner">
        <p class="voices__label" id="profile-title">The graduate we pray for</p>
        <blockquote class="profile"><p>{C.GRADUATE_PROFILE}</p></blockquote>
        <div class="profile__actions">
          <a class="button button--gold" href="/enquire">Start your application</a>
          <a class="link-arrow link-arrow--light" href="{PDF}" download>Download the curriculum</a>
        </div>
      </div>
    </section>
  </main>
"""

GALLERY = page_head("Gallery", "Gallery", "Graduation and ordination at Christian Service Church, Christian Centre, East Legon. Tap any photo to see it larger.", photo="laying-on-of-hands") + f"""
  <main id="main">
    <section class="section section--flush">
      <div class="wrap gallery">
{chr(10).join(f"        {figure(slug, cap)}" for slug, cap in PHOTOS)}
      </div>
    </section>
{CTA}
  </main>
  <dialog class="lightbox" aria-label="Photo">
    <button class="lightbox__close" type="button" aria-label="Close">×</button>
    <button class="lightbox__nav lightbox__prev" type="button" aria-label="Previous photo">‹</button>
    <img alt="">
    <button class="lightbox__nav lightbox__next" type="button" aria-label="Next photo">›</button>
    <p class="lightbox__caption"></p>
  </dialog>
"""

NOT_FOUND = page_head("Not found", "We couldn’t find that page.", "It may have moved. Try the <a href=\"/\">homepage</a> or <a href=\"/programmes\">programmes</a>.") + """
  <main id="main"></main>
"""

PAGES = {
    "index.html": ("Home", "Ezekiel Bible Institute is a Bible school in East Legon, Accra, Ghana, offering six levels of study from Certificate to PhD in theology and ministry, with hostel accommodation. International students welcome.", "/", HOME,
                   [ORG, WEBSITE, faq_ld(HOME_FAQ), *events_ld()]),
    "programmes.html": ("Programmes", "Bible and theology programmes in Accra, Ghana, from Certificate to PhD: Certificate in Christian Foundations, Diploma in Christian Ministry, Bachelor and Master of Theology, DMin and PhD.", "/programmes", PROGRAMMES_PAGE,
                        [breadcrumbs("/programmes", "Programmes"), courses_ld()]),
    "about.html": ("About", "About Ezekiel Bible Institute: an evangelical, interdenominational Bible school training pastors and church leaders at Christian Service Church, East Legon, Accra, since 2001.", "/about", ABOUT,
                   [breadcrumbs("/about", "About"), ORG]),
    "curriculum.html": ("Curriculum", "The Ezekiel Bible Institute curriculum: Certificate in Christian Foundations, Diploma, Bachelor and Master of Theology, Doctor of Ministry and PhD. Every course, semester by semester.", "/curriculum", CURRICULUM,
                        [breadcrumbs("/curriculum", "Curriculum"), courses_ld()]),
    "admissions.html": ("Admissions", "How to apply to Ezekiel Bible Institute in Accra, Ghana: key dates, fees, bursaries, hostel accommodation and support for international students.", "/admissions", ADMISSIONS,
                        [breadcrumbs("/admissions", "Admissions"), faq_ld(ADMISSIONS_FAQ)]),
    "hostel.html": ("Hostel", "Student hostel at Ezekiel Bible Institute, East Legon, Accra: furnished shared rooms, Wi-Fi, study room and 24-hour security for Ghanaian and international students.", "/hostel", HOSTEL,
                    [breadcrumbs("/hostel", "Hostel"), HOSTEL_LD, faq_ld(HOSTEL_FAQ)]),
    "visit.html": ("Visit", "Visit Ezekiel Bible Institute at Christian Service Church, East Legon, Accra, Ghana. Open days, events, directions and office hours.", "/visit", VISIT,
                   [breadcrumbs("/visit", "Visit"), *events_ld()]),
    "gallery.html": ("Gallery", "Photos from graduation and ordination at Ezekiel Bible Institute, Christian Service Church, East Legon, Accra.", "/gallery", GALLERY,
                     [breadcrumbs("/gallery", "Gallery")]),
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
