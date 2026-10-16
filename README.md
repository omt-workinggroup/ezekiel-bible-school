# Ezekiel Bible School

Marketing site for Ezekiel Bible School. Static HTML, CSS and a little JavaScript; no build step.

## Local development

```sh
npx serve .
# or
python3 -m http.server 8000
```

## Structure

| Path | Page |
| --- | --- |
| `index.html` | Home |
| `programmes.html` | Programmes, entry requirements, online study |
| `about.html` | History, teaching approach, faculty |
| `admissions.html` | How to apply, key dates, fees, FAQ |
| `visit.html` | Events, location, office hours |
| `enquire.html` | Prospectus request form |
| `404.html` | Not found |

`styles.css` holds all styles (mobile first) and `main.js` handles the mobile menu,
programme filter and enquiry form. `vercel.json` turns on clean URLs, so
`/programmes` serves `programmes.html`.

The header and footer are repeated in each page. If you change one, change them all.

## Deployment

Hosted on Vercel. Every push to `main` deploys to production; other branches get preview URLs.

## To do

- [ ] Replace placeholder contact details, fees and dates
- [ ] Connect the enquiry form (Formspree or a Vercel function)
- [ ] Add campus photography
