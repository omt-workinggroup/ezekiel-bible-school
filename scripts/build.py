"""Assemble the static pages with a shared header and footer."""
import pathlib, sys

OUT = pathlib.Path(sys.argv[1])

NAV = [("/about", "About"), ("/programmes", "Programmes"), ("/admissions", "Admissions"), ("/visit", "Visit")]

def head(title, desc, path):
    full = "Ezekiel Bible Institute" if path == "/" else f"{title} · Ezekiel Bible Institute"
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>{full}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="https://ezekiel-bible-school.vercel.app{path}">
  <meta name="theme-color" content="#fbf9f4">
  <meta property="og:title" content="{full}">
  <meta property="og:description" content="{desc}">
  <meta property="og:type" content="website">
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
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,opsz,wght@0,8..60,300;0,8..60,400;0,8..60,600;1,8..60,300;1,8..60,400&family=Cinzel:wght@500;600&family=Public+Sans:wght@400;500;600&display=swap">
  <link rel="stylesheet" href="/styles.css">
  <script src="/main.js" defer></script>
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
          <a href="tel:+10000000000">+1 (000) 000-0000</a>
          <a href="mailto:admissions@example.com">admissions@example.com</a>
        </p>
      </div>
    </div>
  </div>
"""

FOOTER = """
  <footer class="footer">
    <div class="wrap footer__grid">
      <div class="footer__about">
        <a class="footer__logo" href="/">
          <svg class="logo__mark" aria-hidden="true"><use href="#mark"/></svg>
          <span class="logo__word">Ezekiel<span>Bible Institute</span></span>
        </a>
        <p>12 Covenant Avenue<br>Hope City</p>
        <p><a href="tel:+10000000000">+1 (000) 000-0000</a><br><a href="mailto:office@example.com">office@example.com</a></p>
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

HOME = f"""
  <main id="main">
    <section class="hero" aria-labelledby="hero-title">
      <div class="hero__media" aria-hidden="true">
{hero_slides()}
        <svg class="hero__mark"><use href="#mark"/></svg>
        <svg class="hero__rings" viewBox="0 0 600 600"><circle cx="300" cy="300" r="298"/><circle cx="300" cy="300" r="236"/><circle cx="300" cy="300" r="174"/></svg>
      </div>

      <div class="wrap hero__body">
        <p class="hero__kicker">Ezekiel Bible Institute <span aria-hidden="true">·</span> Since 2001</p>
        <h1 id="hero-title" class="hero__title">
          <span class="line"><span>Study Scripture</span></span>
          <span class="line"><span>closely.</span></span>
          <span class="line"><span><em>Serve the church well.</em></span></span>
        </h1>
        <p class="hero__lede">Theological training for pastors, missionaries and church leaders. On campus in Hope City or online from anywhere.</p>
        <div class="hero__actions">
          <a class="button button--gold" href="/enquire">Request a prospectus</a>
          <a class="link-arrow link-arrow--light" href="/programmes">Explore programmes</a>
        </div>
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

    <section class="section">
      <div class="wrap">
        <div class="section-head">
          <h2>Coming up</h2>
          <a class="link-arrow" href="/visit">All events</a>
        </div>
        <ul class="events">
          <li>
            <time datetime="2026-11-07"><span>Nov</span> 07</time>
            <div><h3>Open day</h3><p>Sit in on a class, have lunch with students and meet the faculty.</p></div>
          </li>
          <li>
            <time datetime="2026-11-21"><span>Nov</span> 21</time>
            <div><h3>Online information evening</h3><p>For anyone considering online study. On Zoom, 18:00.</p></div>
          </li>
        </ul>
      </div>
    </section>
{CTA}
  </main>
"""

PROGRAMMES_PAGE = page_head("Programmes", "Programmes", "Six programmes, from a twelve-week evening course to a three-year degree. Every one can be started in January or September.") + f"""
  <main id="main">
    <section class="section section--flush">
      <div class="wrap">
        <div class="filter" role="group" aria-label="Filter by study mode">
          <button type="button" aria-pressed="true" data-mode="all">All</button>
          <button type="button" aria-pressed="false" data-mode="campus">On campus</button>
          <button type="button" aria-pressed="false" data-mode="online">Online</button>
        </div>
{prog_table(PROGRAMMES)}
        <p class="note">Campus fees include books and lunch. Online students pay 20% less and buy their own textbooks.</p>
      </div>
    </section>

    <section class="section section--tint">
      <div class="wrap columns">
        <div>
          <h2>Entry requirements</h2>
          <ul class="list">
            <li>A recommendation from your pastor or church leader</li>
            <li>Secondary school completion for diploma and degree programmes</li>
            <li>English at a level where you can read academic texts comfortably</li>
          </ul>
          <p class="muted">No previous theological study is needed. If you have studied elsewhere, you may be able to transfer up to a third of a programme.</p>
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

ABOUT = page_head("About", "About the institute", "Ezekiel Bible Institute began in 2001 with eleven students in a borrowed church hall. Today we teach around 400 students a year on campus and online.") + """
  <main id="main">
    <section class="section section--flush">
      <div class="wrap prose-split">
        <h2>What we are for</h2>
        <div class="prose">
          <p>We exist to train people who will teach the Bible faithfully and care for the church well. Most of our graduates go on to serve in local congregations; others work in mission, chaplaincy, schools and the workplace.</p>
          <p>We are evangelical and interdenominational. Students come from Anglican, Baptist, Pentecostal, Methodist and independent churches, and all of them affirm our statement of faith.</p>
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
            <div><dt>Practice</dt><dd>From the second term you serve each week with a partner church.</dd></div>
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

ADMISSIONS = page_head("Admissions", "Admissions", "We look for people who are already serving in their church and want to be better equipped for it. You don’t need a theology background.") + """
  <main id="main">
    <section class="section section--flush">
      <div class="wrap feature">
        <div>
          <h2 class="h3">How to apply</h2>
          <ol class="steps">
            <li><h3>Enquire</h3><p>We send a prospectus and introduce you to an admissions tutor.</p></li>
            <li><h3>Apply</h3><p>A short form, a one-page testimony and your pastor’s letter.</p></li>
            <li><h3>Interview</h3><p>Thirty minutes, in person or by video call.</p></li>
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
          <p>The September intake opens for applications in March.</p>
        </aside>
      </div>
    </section>

    <section class="section section--tint" id="fees">
      <div class="wrap columns">
        <div>
          <h2>Fees and bursaries</h2>
          <p>Fees are listed with each programme and are charged per year. Campus fees include books and lunch; accommodation is separate.</p>
          <p class="muted">68% of current students receive a bursary. Most awards cover between a quarter and three quarters of fees, and are based on household income and church support.</p>
        </div>
        <div>
          <h2>Accommodation</h2>
          <p>Shared rooms on campus cost $90 a month with meals. We have six flats for married students, allocated in order of acceptance.</p>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="wrap prose-split">
        <h2>Questions</h2>
        <div class="faq">
          <details>
            <summary>Can I study online from another country?</summary>
            <p>Yes. Lectures are recorded and seminars run at two times each week.</p>
          </details>
          <details>
            <summary>Do I need to have studied theology before?</summary>
            <p>No. The certificate and diploma programmes start from the beginning.</p>
          </details>
          <details>
            <summary>Can I transfer credit from another college?</summary>
            <p>Usually, for up to a third of a programme. Send your transcript with your application and the Dean will review it.</p>
          </details>
          <details>
            <summary>Can I work while I study?</summary>
            <p>Many online and part-time students do. Full-time campus study leaves room for around ten hours of work a week.</p>
          </details>
        </div>
      </div>
    </section>
  </main>
"""

VISIT = page_head("Visit", "Visit us", "The best way to know whether Ezekiel is right for you is to spend a day here. You are welcome at any of the events below.") + """
  <main id="main">
    <section class="section section--flush">
      <div class="wrap">
        <ul class="events events--full">
          <li>
            <time datetime="2026-11-07"><span>Nov</span> 07</time>
            <div><h3>Open day</h3><p>Sit in on a class, have lunch with students and meet the faculty. 10:00 – 15:00, Main Hall.</p></div>
            <a class="link-arrow" href="/enquire">Book a place</a>
          </li>
          <li>
            <time datetime="2026-11-21"><span>Nov</span> 21</time>
            <div><h3>Online information evening</h3><p>For anyone considering online study. On Zoom at 18:00, about an hour.</p></div>
            <a class="link-arrow" href="/enquire">Register</a>
          </li>
          <li>
            <time datetime="2026-12-05"><span>Dec</span> 05</time>
            <div><h3>Graduation service</h3><p>The class of 2026 is commissioned. Families and churches welcome. 15:00, Chapel.</p></div>
          </li>
          <li>
            <time datetime="2027-01-11"><span>Jan</span> 11</time>
            <div><h3>Orientation week</h3><p>For new students starting in January.</p></div>
          </li>
        </ul>
      </div>
    </section>

    <section class="section section--tint" id="find-us">
      <div class="wrap columns">
        <div>
          <h2>Find us</h2>
          <address>12 Covenant Avenue<br>Hope City</address>
          <p class="muted">Ten minutes’ walk from Central Station. Parking is free on campus.</p>
        </div>
        <div>
          <h2>Office hours</h2>
          <dl class="hours">
            <div><dt>Monday – Friday</dt><dd>08:00 – 16:30</dd></div>
            <div><dt>Saturday</dt><dd>By appointment</dd></div>
            <div><dt>Sunday</dt><dd>Closed</dd></div>
          </dl>
        </div>
      </div>
    </section>
  </main>
"""

ENQUIRE = page_head("Enquire", "Request a prospectus", "Tell us a little about yourself and an admissions tutor will reply within two working days.") + """
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
          <div class="field">
            <label for="f-message">Message <span>Optional</span></label>
            <textarea id="f-message" name="message" rows="4"></textarea>
          </div>
          <button class="button" type="submit">Send enquiry</button>
          <p class="form__status" role="status"></p>
        </form>

        <aside class="contact">
          <h2>Prefer to talk?</h2>
          <p><a href="tel:+10000000000">+1 (000) 000-0000</a><br><a href="mailto:admissions@example.com">admissions@example.com</a></p>
          <p class="muted">The admissions office is open 08:00 – 16:30, Monday to Friday.</p>
        </aside>
      </div>
    </section>
  </main>
"""

NOT_FOUND = page_head("Not found", "We couldn’t find that page.", "It may have moved. Try the <a href=\"/\">homepage</a> or <a href=\"/programmes\">programmes</a>.") + """
  <main id="main"></main>
"""

PAGES = {
    "index.html": ("Home", "Certificate, diploma and degree programmes in Bible, theology and ministry, on campus or online.", "/", HOME),
    "programmes.html": ("Programmes", "Six programmes in Bible, theology and ministry, from a twelve-week course to a three-year degree.", "/programmes", PROGRAMMES_PAGE),
    "about.html": ("About", "Training pastors, missionaries and church leaders since 2001.", "/about", ABOUT),
    "admissions.html": ("Admissions", "How to apply, key dates, fees and bursaries.", "/admissions", ADMISSIONS),
    "visit.html": ("Visit", "Open days, events and how to find us.", "/visit", VISIT),
    "enquire.html": ("Enquire", "Request a prospectus from Ezekiel Bible Institute.", "/enquire", ENQUIRE),
    "404.html": ("Page not found", "Page not found.", "/404", NOT_FOUND),
}

for name, (title, desc, path, body) in PAGES.items():
    (OUT / name).write_text(head(title, desc, path) + "\n" + header(path) + body + FOOTER)
    print("wrote", name)
