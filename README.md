# Episode Finder

Search any TV series and see every episode that has aired, grouped by season.
Built on the free [TVmaze API](https://www.tvmaze.com/api) (no API key needed).

## Features (web page)

- **Series header**: backdrop, poster, years, genres, status, channel, runtime, rating, summary
  and links to TVmaze, IMDb and the official site, followed by a facts panel.
- **Latest, next and continue-watching cards**: jump straight to the episode in its season;
  the next episode shows its local air time and a countdown.
- **Seasons as poster cards**: the show poster stands in when a season has none. Switch seasons
  with the cards, the Previous/Next buttons or the ← and → keys.
- **Episode rows**: still image, air date, runtime, rating, a finale badge and a short summary
  with *Read more*. Sort oldest or newest first.
- **Watched tracking**: tick episodes or whole seasons. Progress shows on the season cards.
  Saved in your browser only, with no account.
- **Hide spoilers**: blurs stills and summaries of episodes you have not watched yet.
- **Main cast** with photos and character names.

This repository has two parts:

| File | What it is |
| --- | --- |
| `index.html` | The web page. One self-contained file (HTML, CSS and JavaScript). The visitor's browser calls TVmaze directly. |
| `tvmaze_episodes.py` | A command-line version in Python, with caching, retries and error handling. |

## Run the web page locally

Open `index.html` in a browser (double-click it). That's all: there is nothing to install.

If your browser blocks anything when opened as a file, serve the folder instead:

```bash
python3 -m http.server 8000
```

then visit <http://localhost:8000>.

## Publish it with GitHub Pages (free hosting)

1. Push this repository to GitHub (steps below).
2. On GitHub open the repository, then **Settings → Pages**.
3. Under **Build and deployment**, choose **Deploy from a branch**, pick the `main` branch and the `/ (root)` folder, and save.
4. After about a minute the page is live at `https://<your-username>.github.io/<repository-name>/`.

### Pushing to GitHub for the first time

Create an empty repository on GitHub (no README, no .gitignore), then in this folder run:

```bash
git init -b main
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/<your-username>/<repository-name>.git
git push -u origin main
```

## Use the Python script

Requires Python 3.10 or newer.

```bash
pip install requests
python tvmaze_episodes.py "big bang theory"
```

Results are cached for 24 hours in a `.tvmaze_cache` folder (ignored by git).

## How it works

- The page searches `GET /search/shows?q=<name>` and lists the best matches.
- Picking a match loads everything in one request:
  `GET /shows/<id>?embed[]=seasons&embed[]=episodes&embed[]=cast&embed[]=nextepisode&embed[]=previousepisode`,
  plus `GET /shows/<id>/images` for the backdrop.
- Only episodes with an air date of today or earlier are listed. Specials are not included.
- The address changes to `#show=<id>&season=<n>` so a series and season can be bookmarked or shared.
- Watched episodes, the sort order and the spoiler setting are kept in the browser's `localStorage`.
  They stay on that device and browser.
- Images are loaded straight from TVmaze's image server, which TVmaze explicitly allows.
- Data coverage varies: popular shows have images, ratings and summaries for nearly every episode,
  while some older or less-watched shows have few. The page hides anything that is missing.

## Data and licence

Show and episode data comes from [TVmaze.com](https://www.tvmaze.com/api) and is licensed
[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). Keep the credit in the page
footer. A commercial licence is available from TVmaze on request.

You still need to choose a licence for your own code (for example MIT) and add a `LICENSE` file.
