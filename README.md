# Mass Reaction — landing page

The static website for Mass Reaction, an endless balance puzzle for iPhone: a home page, Privacy Policy, Terms & Conditions and a 404 page, published at https://massreaction.app. There is no build step and no dependencies. The font and images are served with the pages. There are two scripts: `assets/contact.js` builds the support address for the contact buttons, and `assets/consent.js` shows the cookie banner and loads Google Analytics only after the visitor accepts.

## Structure

Everything that gets published lives in `dist/`: `index.html`, `privacy.html`, `terms.html`, `404.html`, `robots.txt`, `sitemap.xml` and `assets/`. The site root also has `favicon.ico`. The `assets/` folder holds the stylesheet `site.css`, the laboratory background `laboratory-v2.webp` and the Barlow Condensed ExtraBold font with its OFL licence. It also holds images from the game: screenshots in `screens/`, special balls in `specials/`, the app icon (`app-icon.png`, `apple-touch-icon.png`) and the social share image `og-image.jpg`. Links to the home page point to `/` (never `index.html`), and `404.html` links from the site root because the server returns it for any path; other links are relative. `art-source/` (the full-size PNG original of the background) and `preview-*.png` (page previews) are kept locally and are not part of the repository.

## Local preview

`python3 -m http.server 4173 --bind 127.0.0.1 --directory dist`, then open http://127.0.0.1:4173/.

## Images from the game

The screenshots were taken on the iPhone 17 Pro Max simulator with `tools/device-check/devicecheck.sh` from the game repository (label `after`). The special-ball and app icons come from the game's Alchemy skin resources. After the game changes, capture new shots, then run `python3 scripts/update_assets.py "<path to the game repository>" [label]`. The script rebuilds `screens/` and `specials/` (WebP), the app icons and `og-image.jpg`. It needs Pillow: `pip3 install pillow`. The site mentions 20 kinds of special balls but deliberately does not say which ones are for sale, because the set on sale can change.

## Deployment

Every push to `main` runs `.github/workflows/deploy.yml`. First it checks the site: the required files exist, every local link points to an existing file, and no email address appears in plain text anywhere in the repository. If the variable `CD_DEPLOY_ENABLED` is `true`, it then copies `dist/` to the CDN host over scp and publishes it to `/var/www/massreaction.app` with `rsync --delete`, the same way as the LuxSort landing. The repository needs the secret `CDN_SSH_KEY` and the variables `CDN_SSH_HOST`, `CDN_SSH_USER` and `CD_DEPLOY_ENABLED`. The `/var/www/massreaction.app` directory (owned by the `deploy` user), the nginx vhost with `error_page 404 /404.html`, and TLS for massreaction.app are set up once on the host, like the LuxSort vhost. The domain's DNS is on Cloudflare.

## Legal pages

Privacy and Terms describe the game as its code stood on 9 November 2026: no ads and no server of its own. Analytics is being added to the game; before it ships, add a section to the Privacy Policy naming the provider, the data it collects and how to opt out, and update the App Store Connect privacy labels. Purchases go through Apple. The special-ball stash is stored in the player's iCloud key-value store with a random per-device identifier. Scores are submitted to Game Center. Best score, settings and seen tips stay on the device. If the game adds a new service (analytics, ads, a server, another kind of storage), update these pages before release, together with the App Store Connect privacy labels. The texts have not been reviewed by a lawyer.

## Contact

The support address is never written in plain text, so scrapers cannot pick it up from the pages or from this repository. Contact links are buttons with `data-contact` (and an optional `data-subject`); on click, `assets/contact.js` rebuilds the address from character codes and opens a `mailto:` link, the same approach as the LuxSort landing. Mail is forwarded by Cloudflare Email Routing. To change the address, update `ADDRESS_CODES` in `contact.js`. Public files and commits must not contain personal email addresses or other private data; the workflow fails on any plain email address.

## Cookie banner and analytics

`assets/consent.js` shows a banner on the first visit with two equal buttons, Decline and Accept, and keeps the answer in `localStorage` under `mr-consent`. Nothing is requested from Google before Accept. After Accept it loads Google Analytics 4 (measurement ID `G-BN36B66LGS`, Analytics account "Mass Reaction") with Google signals and ad personalisation off. Every footer has a "Cookie settings" button (`data-cookie-settings`) that reopens the banner; choosing Decline after Accept deletes the `_ga` cookies and reloads the page. The Privacy Policy section `#analytics` describes this setup, so update it together with any change to the script, the measurement ID or the Analytics data settings (retention: event data two months, user data 14 months).
