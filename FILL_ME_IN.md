# Before you publish — what still needs real content

Most of the original list is done. What's left is below, shortest first.

## 1. Two live URLs (2 one-line edits)

Open `build.py` and look at the constants near the top:

```python
FPL_LIVE_URL = None
RECKON_LIVE_URL = None
```

Set either to its public URL and re-run `python3 build.py`. The project page
picks it up on its own — an "Open live demo" button appears in the hero, and
the project can be given `"status": "LIVE"` in the `PROJECTS` list so the card
shows the live badge too. Left as `None`, the page just shows its GitHub link
rather than claiming a demo that isn't there.

Everything else with a live URL is already wired: the RAG assistant and the
credit risk service (both Cloud Run) and the Premier League predictor
(`https://premier-league-black.vercel.app`, read off the repo's own homepage
field).

## 2. Reckon's stack — CV and repo disagree

The CV lists Reckon as *Python, PyTorch, DuckDB, FastAPI, React, Docker,
Railway, PostgreSQL*. The repository (`MelvTheGoat/Stack`) actually builds on
FastAPI + SQLAlchemy + Pydantic with Jinja review pages, scikit-learn for the
scoring model, Claude for the last prose-extraction layer, and a `cloudbuild.yaml`
pointing at Cloud Run. The site follows the repository, because that's the thing
an interviewer can open. Worth reconciling the CV to match — or, if the CV is
describing a newer version, update `PROJECTS[0]["stack"]` in `build.py`.

## 3. Writing page

Both posts are drafted but unpublished, and the page now says exactly that
instead of showing placeholder dates and dead links. Publish them wherever
you're writing (Medium, a static blog, this same site), then edit
`build_writing()` in `build.py` with the real date and link.

## 4. Contact — optional scheduling link

A Calendly link is already on `contact.html`
(`https://calendly.com/mlvyn-t`). Check it still resolves to the right
calendar before you send the site to anyone.

---

## Already done

- **Repo links** — every project points at its real repository.
- **Resume PDF** — `assets/resume.pdf` is the current ML Engineer CV, and
  `resume.html` now also renders experience, education, skills and certificates
  as HTML so nothing depends on the embed loading.
- **Photo** — `about.html` uses the real image.

---

## Deploying

No build step required after `python3 build.py` has run once — the output
is plain static HTML/CSS/JS. Fastest paths:

**Netlify / Vercel (drag-and-drop):** drag this whole folder onto
netlify.com/drop, or run `vercel` from inside this folder if you have the
Vercel CLI installed. Either gives you a live URL in under a minute.

**GitHub Pages:** push this folder to a repo, enable Pages in repo settings,
point it at the root of the `main` branch (or a `docs/` folder if you prefer
to nest it inside an existing repo).

Either way — re-run `python3 build.py` locally after any content edit, then
redeploy the regenerated files. The Python script is a convenience for
editing consistently across all 14 pages; it is not a runtime dependency of
the deployed site.
