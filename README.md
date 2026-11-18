# Episode Finder

Search any TV series and see every episode that has aired, grouped by season.
Built on the free [TVmaze API](https://www.tvmaze.com/api) (no API key needed).

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
- Picking a match loads `GET /shows/<id>/episodes`.
- Only episodes with an air date of today or earlier are shown.
- The address changes to `#show=<id>` so a series can be bookmarked or shared.

## Data and licence

Show and episode data comes from [TVmaze.com](https://www.tvmaze.com/api) and is licensed
[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). Keep the credit in the page
footer. A commercial licence is available from TVmaze on request.

You still need to choose a licence for your own code (for example MIT) and add a `LICENSE` file.
