# Portfolio — Mayungbo Oluwatobi Melvyn

Static portfolio site. Machine Learning & AI Engineer, Lagos.

Everything is generated from one file. `build.py` holds the content —
projects, posts, CV data, live URLs — and writes every page from it, so a
change lands in one place rather than in fourteen HTML files.

```sh
python3 build.py     # regenerates every page
```

No dependencies, no build step beyond that, no runtime requirement: the
output is plain static HTML/CSS/JS.

## Editing

| What | Where in `build.py` |
| --- | --- |
| A project's copy, numbers, tags, stack | the `PROJECTS` list |
| A project's live demo button | its `"live"` field, or the URL constants at the top |
| A project's LIVE badge | its `"status"` field |
| Which three projects are featured on the home page | the order of `PROJECTS` — the first three |
| A blog post | the `POSTS` list |
| Experience, education, skills, certificates | `EXPERIENCE`, `EDUCATION`, `SKILLS`, `CERTIFICATES` |
| Name, email, links, location | the constants at the top |

Live URLs are constants near the top of the file. Setting one to `None`
drops the "Open live demo" button from that project's page rather than
linking at something that isn't there.

`assets/resume.pdf` is the downloadable CV; `resume.html` also renders the
same information as HTML so nothing depends on the PDF embed loading.

## Deploying

**Netlify / Vercel:** drag this folder onto netlify.com/drop, or run
`vercel` from inside it.

**GitHub Pages:** push and enable Pages against the root of `main`.

Either way, re-run `python3 build.py` after any content edit and redeploy
the regenerated files.
