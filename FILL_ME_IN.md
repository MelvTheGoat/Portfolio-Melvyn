# Before you publish — what still needs real content

Most of the original list is done. What's left is below, shortest first.

## 1. Reckon's stack — CV and repo still disagree in part

The CV lists Reckon as *Python, PyTorch, DuckDB, FastAPI, React, Docker,
Railway, PostgreSQL*. Railway and Postgres check out — the live instance is on
Railway, and `RECON_DATABASE_URL` points SQLAlchemy at Postgres. The rest does
not: the repository (`MelvTheGoat/Stack`) has no PyTorch, no DuckDB and no
React. The scoring model is scikit-learn with Platt calibration, the review
pages are Jinja templates, and the last extraction layer calls Claude. The site
follows the repository, because that's the thing an interviewer can open.

Worth reconciling the CV to match — or, if it's describing a newer version,
update `PROJECTS[0]["stack"]` in `build.py`.

## 2. FPL ships from GitHub Pages, not Render

`render.yaml` describes a paid always-on service, but the live site is the
GitHub Actions + Pages path (`melvthegoat.github.io/Fantasy-Premier-League`),
so the project page lists GitHub Pages. If you move it to Render later, change
`FPL_LIVE_URL` and the last entry of that project's `stack`.

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
- **Live URLs** — all five deployed systems are wired up and badged LIVE:
  Reckon (Railway), the Premier League predictor (Vercel), the RAG assistant
  and the credit risk service (both Cloud Run), and the FPL AI Manager
  (GitHub Pages). They live as constants at the top of `build.py`; every page
  reads them from there.
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
