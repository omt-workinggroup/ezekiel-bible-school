# Ezekiel Bible School — sample landing page

A fully responsive, mobile-first landing page for a Bible institute. Plain HTML, CSS and JavaScript — no build step.

## Files
- `index.html` — page markup (hero, stats, about, programmes, faculty, testimonials, admissions, events, FAQ, enquiry form, footer)
- `styles.css` — mobile-first styles (breakpoints at 640px, 900px, 1100px)
- `script.js` — mobile menu, scroll reveal, counters, programme filter, swipeable testimonials, form validation
- `vercel.json` — Vercel static hosting config

## Run locally
```bash
npx serve .
```

## Deploy to Vercel
Import this repository at https://vercel.com/new — framework preset **Other**, no build command, output directory `.` (root). Or with the CLI:
```bash
npx vercel --prod
```

> Sample content: names, numbers, events and contact details are placeholders. The enquiry form validates on the client only; connect it to a form service (e.g. Formspree) or a Vercel function to receive submissions.
