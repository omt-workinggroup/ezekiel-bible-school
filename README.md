# Ezekiel Bible School

Marketing site for Ezekiel Bible School. Static HTML, CSS and a little JavaScript; no build step.

## Local development

```sh
npx serve .
# or
python3 -m http.server 8000
```

## Structure

| File | Purpose |
| --- | --- |
| `index.html` | Home page |
| `styles.css` | All styles, mobile first |
| `main.js` | Mobile menu, programme filter, enquiry form |
| `404.html` | Not-found page (served automatically by Vercel) |
| `vercel.json` | Clean URLs and security headers |

## Deployment

Hosted on Vercel. Every push to `main` deploys to production; other branches get preview URLs.

## To do

- [ ] Replace placeholder contact details, fees and dates
- [ ] Connect the enquiry form (Formspree or a Vercel function)
- [ ] Add campus photography
