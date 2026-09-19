# Generates the static site from the templates + content below.
# Run: python3 build.py
# Output: sibling HTML files, ready to deploy as-is (no build step needed
# after this — the generator is a convenience for editing, not a dependency
# of the deployed site).

import os

ROOT = os.path.dirname(os.path.abspath(__file__))

NAME = "Mayungbo Oluwatobi Melvyn"
EMAIL = "mlvyn.t@gmail.com"
LINKEDIN = "https://linkedin.com/in/oluwatobi-mayungbo-3a567026b"
GITHUB_PROFILE = "https://github.com/MelvTheGoat"
LOCATION = "Lagos, Nigeria"
RAG_LIVE_URL = "https://nigerian-fintech-regulation-assistant-474115007874.europe-west1.run.app"
CREDIT_LIVE_URL = "https://credit-risk-decisioning-702657773047.europe-west1.run.app/"
PL_LIVE_URL = "https://premier-league-black.vercel.app"
# Set these to the public URL once the deployment is up; every page picks it up
# automatically and the "Open live demo" button appears. Left as None, the
# project simply shows its GitHub link instead of claiming a demo that isn't there.
FPL_LIVE_URL = "https://melvthegoat.github.io/Fantasy-Premier-League/"
RECKON_LIVE_URL = "https://stack-production-d2a4.up.railway.app/review"

FONT_LINK = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&'
    'family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">'
)

NAV_ITEMS = [
    ("Home", "/index.html", "home"),
    ("Projects", "/projects.html", "projects"),
    ("Writing", "/writing.html", "writing"),
    ("About", "/about.html", "about"),
    ("Resume", "/resume.html", "resume"),
    ("Contact", "/contact.html", "contact"),
]


def nav(active, depth=""):
    items = []
    for label, href, key in NAV_ITEMS:
        h = (depth + href.lstrip("/"))
        current = ' aria-current="page"' if key == active else ""
        items.append(f'<li><a href="{h}"{current}>{label}</a></li>')
    return "\n        ".join(items)


def head(title, desc, depth=""):
    return f"""<meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  {FONT_LINK}
  <link rel="stylesheet" href="{depth}css/style.css">
"""


def header(active, depth=""):
    return f"""  <nav class="site-nav">
    <div class="wrap">
      <a class="brand" href="{depth}index.html">{NAME.split()[0]}<span class="dot">.</span>ml</a>
      <button class="nav-toggle" aria-label="Toggle navigation" aria-expanded="false">
        <span></span>
      </button>
      <ul class="nav-links">
        {nav(active, depth)}
      </ul>
    </div>
  </nav>
"""


def footer(depth=""):
    return f"""  <footer>
    <div class="wrap">
      <span class="copy">&copy; 2026 {NAME} &mdash; built with calibration in mind.</span>
      <div class="foot-links">
        <a href="mailto:{EMAIL}">Email</a>
        <a href="{GITHUB_PROFILE}" target="_blank" rel="noopener">GitHub</a>
        <a href="{LINKEDIN}" target="_blank" rel="noopener">LinkedIn</a>
      </div>
    </div>
  </footer>
  <script src="{depth}js/main.js"></script>
"""


def page(title, desc, active, body, depth=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
{head(title, desc, depth)}</head>
<body>
{header(active, depth)}
{body}
{footer(depth)}
</body>
</html>
"""


def reading(label, value, unit="", small=False):
    cls = "reading sm" if small else "reading"
    unit_html = f'<span class="unit">{unit}</span>' if unit else ""
    return f"""<div class="{cls}">
              <span class="r-label">{label}</span>
              <span class="r-value">{value}{unit_html}</span>
              <span class="r-axis"></span>
            </div>"""


# ---------------------------------------------------------------------------
# Project data — every number here comes from the CV or from the project's own
# repository (its README, its evaluation output, its backtest table). Repo URLs
# are the real ones. Live URLs live in the constants at the top of this file:
# set FPL_LIVE_URL / RECKON_LIVE_URL once those deployments have a public
# address and the "Open live demo" button appears on its own.
# ---------------------------------------------------------------------------

PROJECTS = [
    {
        "slug": "reckon",
        "name": "Reckon &mdash; Payment Reconciliation &amp; Review System",
        "short": "Matches incoming payments to invoices and hands a person only the cases it cannot prove. Certain rules first, a calibrated model second, and a threshold drawn from what each mistake actually costs in naira. Deployed, with the review queue open.",
        "tags": ["Payments", "Calibration", "Human-in-the-loop", "Deployed"],
        "status": "LIVE",
        "headline_label": "CLOSED WITHOUT A PERSON",
        "headline_value": "76.1",
        "headline_unit": "%",
        "github": "https://github.com/MelvTheGoat/Stack",
        "live": RECKON_LIVE_URL,
        "problem": (
            "Money arrives through card, dedicated virtual accounts, bank transfer and cash, and most "
            "of it does not say what it is for &mdash; a bank credit reads <span class=\"mono\">NIP/GTB/OKONKWO "
            "ADA/PAYMENT</span> and nothing more. Somebody sits down every evening and matches payments "
            "to invoices by hand, and it fails the same ways every time: the name is spelled differently, "
            "somebody underpaid, one transfer covers three invoices, the same payment was entered twice, "
            "or two invoices are for the same amount and either one fits."
        ),
        "result": (
            "On 439 payments over one month worth &#8358;37,181,750: 76.1% closed without a person "
            "&mdash; rules 69.9%, the model 6.2% &mdash; at 100% precision on that corpus and 80.1% "
            "recall. Not one duplicate and not one payment from a stranger was closed unattended. The "
            "105 cases that do reach a person are the part payments, overpayments, splits and "
            "duplicates, which is the correct answer for them rather than a failure."
        ),
        "flow": "payment in → duplicate check → three exact rules (our reference / dedicated account / amount + time window)\n  → scored candidates (name, amount, timing, channel, payer history) → Platt-calibrated probability\n  → close above 0.85, otherwise → review queue ranked by money at risk",
        "hardest_title": "Where the 0.85 threshold came from, and why it was not chosen by eye",
        "hardest": (
            "The two mistakes cost different amounts. Checking a match that was fine anyway costs "
            "&#8358;60 &mdash; three minutes of a bookkeeper's time. Closing a match that was wrong costs "
            "about &#8358;5,000: two hours to notice, trace and reverse it, plus chasing a customer for "
            "money they had already paid. That is 83 to 1, which means unattended closing only pays if "
            "it is wrong less than roughly 1.2% of the time &mdash; and that is what puts the line at "
            "0.85 and holds the model to 6% of the month. Six percent that is right beats twenty "
            "percent that is mostly right. Change the two cost constants and the line moves on its own."
        ),
        "measured_title": "What the results actually showed",
        "measured": (
            "A threshold policy is only as good as the probability behind it, so the scores were "
            "calibrated and then checked on 390 candidate comparisons the model never trained on: "
            "Brier 0.0219, expected calibration error 0.024. Platt scaling and isotonic regression were "
            "both fitted and compared &mdash; Platt won, and both beat leaving the raw scores alone "
            "(0.093 &rarr; 0.052). The prose-intake layer is reported separately and deliberately "
            "under-claimed: 94.4% of 40 hand-labelled payment reports read completely right, but they "
            "were written by the same person who wrote the parser, so the honest description is "
            "&ldquo;it has not failed on these yet&rdquo;, not an accuracy rate. The ten written "
            "afterwards and never used for tuning immediately found four real bugs."
        ),
        "next": "Widen the prose-report evaluation well beyond 40 examples written in-house &mdash; the number that most needs an independent set behind it &mdash; and re-fit the threshold against a second month of real payments to check the 83:1 cost ratio holds outside the corpus it was drawn from.",
        # Stack follows the repository and the live instance, which is what an
        # interviewer can open. The CV additionally credits PyTorch, DuckDB and
        # React; none of the three are in MelvTheGoat/Stack, where the scoring
        # model is scikit-learn with Platt calibration, the review pages are
        # Jinja, and the last extraction layer calls Claude. Railway and
        # Postgres do check out (RECON_DATABASE_URL points SQLAlchemy at it).
        "stack": ["Python", "FastAPI", "SQLAlchemy", "PostgreSQL", "scikit-learn", "Pydantic", "Jinja", "Docker", "Railway", "Claude API"],
    },
    {
        "slug": "premier-league",
        "name": "Premier League Match Predictor",
        "short": "A self-retraining match predictor that publishes three-way probabilities and a scoreline for every fixture, keeps every prediction it has ever made on the record, and retrains after each gameweek. Deployed and live.",
        "tags": ["Forecasting", "Calibration", "Deployed", "LightGBM"],
        "status": "LIVE",
        "headline_label": "OUTCOME ACCURACY",
        "headline_value": "52.1",
        "headline_unit": "%",
        "github": "https://github.com/MelvTheGoat/Premier-League",
        "live": PL_LIVE_URL,
        "problem": (
            "A league table describes what happened; it does not describe the situation a match is "
            "played in, and the situation often decides it. A club four days after a European tie "
            "fields a different side. A club that changed manager last month is not the team that "
            "finished last season. The tempting fix is a checklist &mdash; <em>if new manager, add "
            "5%</em> &mdash; hand-tuned per fixture. This project refuses that entirely."
        ),
        "result": (
            "Walk-forward backtest over 2023-24, 2024-25 and 2025-26 from gameweek 4 onward "
            "(1,050 matches): 52.1% outcome accuracy against 43.2% for always backing the home side, "
            "log loss 0.9948 against 1.0061 for a tuned Elo-only baseline, 8.2% of exact scorelines, "
            "and goals MAE of 0.93 per side. Live on Vercel, republished by a scheduled retrain."
        ),
        "flow": "openfootball ingest → 204-column point-in-time feature table (one chronological pass)\n  → LightGBM + multinomial logistic blend (outcome) · Dixon-Coles bivariate Poisson (scoreline)\n  → predict next gameweek → store as an immutable run → export 1.4MB serving DB → Vercel",
        "hardest_title": "Every contextual signal becomes a feature, never an adjustment",
        "hardest": (
            "Congestion, manager tenure, availability, squad quality and table pressure all go into the "
            "feature table as numbers and are left for the model to weigh. Nothing anywhere applies a "
            "hand-tuned bump to a prediction. Where a signal resists measurement the answer is a better "
            "proxy, not a rule: &ldquo;new manager bounce&rdquo; becomes days since the appointment, "
            "matches played under the new manager, and the points-per-game difference either side of "
            "the change. If those matter the model finds them; if not, it ignores them. The same "
            "discipline drives the cross-division Elo &mdash; rated over the Premier League, the "
            "Championship, League One and the cups on one scale &mdash; which is the only thing that "
            "stops three promoted clubs a season starting as blanks."
        ),
        "measured_title": "What the results actually showed",
        "measured": (
            "Calibration is the number that matters here, because the site publishes probabilities "
            "rather than picks: when the model says 65% it happens about 65% of the time, across every "
            "band from 0.16 to 0.74. That came from the linear half of the ensemble and from "
            "early-stopping the boosting rounds &mdash; a fixed 400 rounds produced visible "
            "over-confidence in the 0.5&ndash;0.8 band and cost about 0.03 nats. Two things are "
            "reported rather than smoothed over: draws are almost never the argmax, so they are "
            "expressed as probability mass (typically 25&ndash;30%) instead of being forced into picks; "
            "and per-season accuracy ranges 57.1% / 52.0% / 47.1%, mostly a property of the seasons "
            "&mdash; 2025-26 had eleven managerial changes &mdash; not of the model."
        ),
        "next": "Automate team news. The injury and suspension file ships empty, and a club with no row is treated as unknown rather than fully fit &mdash; so the feature removes itself instead of biasing the model. Filling it reliably is the single largest gain left on the table.",
        "stack": ["Python", "LightGBM", "scikit-learn", "Dixon-Coles Poisson", "SQLite", "Flask", "GitHub Actions", "Vercel"],
    },
    {
        "slug": "fraud",
        "name": "Sequence-Based Transaction Fraud Detection",
        "short": "Three deep sequence architectures benchmarked against gradient boosting under an explicit cost model, with the sequence models' advantage isolated to robustness under drift specifically.",
        "tags": ["Deep Learning", "PyTorch", "Fraud", "Calibration"],
        "status": None,
        "headline_label": "P99 LATENCY",
        "headline_value": "5.1",
        "headline_unit": "ms",
        "github": "https://github.com/MelvTheGoat/Fraud-Detection-With-Sequence-Models",
        "live": None,
        "problem": (
            "Real-time transaction fraud detection needs to catch adaptive fraud patterns &mdash; card "
            "testing, account takeover, merchant compromise &mdash; while staying inside a strict "
            "latency budget and remaining honest about whether the added complexity of deep sequence "
            "models is actually earning its cost over a much simpler baseline."
        ),
        "result": (
            "Sequence models cut expected cost per transaction by 27% (0.0665 vs 0.0906) under an "
            "explicit cost model &mdash; but the margin came entirely from robustness to injected "
            "adversarial drift. Pre-drift, gradient boosting was marginally ahead (0.956 vs 0.950 "
            "PR-AUC). Served via ONNX Runtime at 5.1ms p99 end-to-end latency against a 50ms budget."
        ),
        "flow": "GRU / TCN / causal Transformer (<115k params each)\n  vs LightGBM baseline → focal loss / weighted sampling → temperature + isotonic calibration\n  → ONNX export → FastAPI serving",
        "hardest_title": "Why the honest pre-drift number matters more than the headline 27%",
        "hardest": (
            "Reporting only the post-drift 27% cost reduction would have been a true but misleading "
            "framing &mdash; it implies the sequence models are simply better. The pre-drift comparison "
            "(0.956 vs 0.950 PR-AUC, effectively a tie) is what actually locates <em>why</em> they win: "
            "not raw predictive power, but robustness when the fraud pattern itself shifts. That "
            "distinction changes the real recommendation &mdash; it's an argument for the added "
            "complexity specifically in a non-stationary threat environment, not a blanket "
            "'deep learning wins' claim."
        ),
        "measured_title": "What the results actually showed",
        "measured": (
            "Focal loss and weighted sampling, the two standard fixes for class imbalance, failed in "
            "<em>different</em> ways rather than both simply helping: focal loss degraded probability "
            "calibration (ECE 0.0063) while weighted sampling instead cost ranking quality "
            "(&minus;0.042 PR-AUC). Neither fix was free, and knowing which one costs what let calibration "
            "be corrected surgically afterward &mdash; temperature scaling and isotonic regression "
            "brought ECE down to 0.0005 &mdash; rather than accepting whichever trade-off the first "
            "technique happened to introduce."
        ),
        "next": "Test against a wider set of injected drift patterns to check whether the robustness advantage generalizes beyond the specific drift mechanism used in evaluation.",
        "stack": ["Python", "PyTorch", "LightGBM", "ONNX Runtime", "FastAPI", "Docker", "SHAP"],
    },
    {
        "slug": "rag",
        "name": "Nigerian Fintech Compliance RAG Assistant",
        "short": "A regulatory Q&amp;A system over CBN circulars and the NDPA — hybrid retrieval, citation verification, and a refusal mechanism engineered as a first-class feature. Deployed and live.",
        "tags": ["RAG", "LLM Evaluation", "Deployed", "GCP"],
        "status": "LIVE",
        "headline_label": "RECALL@5",
        "headline_value": "0.96",
        "headline_unit": "",
        "github": "https://github.com/MelvTheGoat/Nigerian-Fintech-Compliance-RAG",
        "live": RAG_LIVE_URL,
        "problem": (
            "Compliance officers and engineers at Nigerian fintechs were manually cross-referencing "
            "hundred-page CBN circulars and the NDPA to answer specific regulatory questions — a Tier "
            "1 KYC threshold, a breach-notification window — that should take seconds, not an afternoon "
            "of document search."
        ),
        "result": (
            "0.96 recall@5 and 0.842 MRR against a labelled 50-question golden set, with zero retrieval "
            "misses in the top 10. Deployed live on GCP Cloud Run within a ~225MB peak memory footprint."
        ),
        "flow": "ingest → section-aware chunk → hybrid index (BM25 + ONNX embeddings)\n  → reciprocal rank fusion → grounded generation → citation guardrail",
        "hardest_title": "Why reciprocal rank fusion, not naive score-blending",
        "hardest": (
            "BM25 scores are unbounded and can exceed 15 for a rare term; cosine similarities from a "
            "normalized embedder sit in a narrow 0.3&ndash;0.7 band. Adding them directly lets BM25 "
            "dominate every ranking purely because its numbers are bigger, not because it's more "
            "trustworthy. Min-max normalization looked like a fix but introduces its own problem: it's "
            "per-query, so one weak BM25 match on a thin-result query gets rescaled to a false 1.0. "
            "Reciprocal rank fusion keeps only each retriever's <em>rank</em>, discarding the raw score "
            "entirely &mdash; rank 1 means the same thing regardless of which retriever produced it, "
            "which sidesteps the scale mismatch instead of patching around it."
        ),
        "measured_title": "What the results actually showed",
        "measured": (
            "The refusal-correctness metric came back at 0.40 in the offline evaluation &mdash; and "
            "tracing it down, the failure was in the <em>stub judge's</em> lexical-overlap heuristic, "
            "not the retrieval or guardrail logic: a question about Kenyan data-protection rules "
            "retrieved the NDPA's cross-border-transfer clause, which shares real vocabulary with the "
            "question purely by topical adjacency. That's a documented limitation of the offline stub, "
            "not a claim about the deployed system's real refusal rate &mdash; re-validating against a "
            "live provider is the explicit next step, not something papered over."
        ),
        "next": "Re-run the evaluation harness against a live provider instead of the offline stub, and expand the golden set with more adversarial and contradictory-source cases.",
        "stack": ["Python", "Streamlit", "BM25", "ONNX Runtime", "Reciprocal Rank Fusion", "FastAPI", "Docker", "GCP Cloud Run"],
    },
    {
        "slug": "credit-risk",
        "name": "Credit Risk Decisioning &amp; Fairness Audit",
        "short": "A full credit decisioning system prioritizing calibration over ranking, with reject inference correcting for approval-only observed outcomes and fairness treated as an explicit policy tradeoff.",
        "tags": ["Credit Risk", "Calibration", "Fairness", "Deployed"],
        "status": "LIVE",
        "headline_label": "PRIORITIZED METRIC",
        "headline_value": "ECE",
        "headline_unit": "",
        "github": "https://github.com/MelvTheGoat/Credit-Risk-Decisioning",
        "live": CREDIT_LIVE_URL,
        "problem": (
            "A lending decision needs a true probability of default, not just a well-ranked score "
            "&mdash; expected loss is a function of a calibrated probability multiplied by exposure, "
            "and a model that ranks applicants correctly but reports overconfident probabilities "
            "produces systematically wrong loss estimates even when its AUC looks strong."
        ),
        "result": (
            "Benchmarked gradient boosting against a traditional WOE-binned logistic scorecard on "
            "calibration quality specifically &mdash; Brier score, reliability diagrams, expected "
            "calibration error &mdash; rather than defaulting to whichever model had the higher AUC. "
            "Ships cost-optimal approve/decline cutoffs, adverse-action reason codes, and an "
            "append-only audit trail that lets any single decision be reconstructed months later."
        ),
        "flow": "WOE scorecard vs. LightGBM → calibration diagnostics\n  → reject inference on approval-only outcomes → fairness audit across protected groups\n  → adverse-action reason codes → audit trail",
        "hardest_title": "Why calibration was prioritized over ranking metrics",
        "hardest": (
            "AUC and similar ranking metrics answer 'does the model order applicants correctly' &mdash; "
            "they say nothing about whether a stated 8% default probability is actually an 8% real-world "
            "rate. Expected loss calculations need the second property, not the first. A model can have "
            "excellent AUC and be badly miscalibrated, producing confidently wrong loss estimates that "
            "look statistically sound until you check them against reality."
        ),
        "measured_title": "What the results actually showed",
        "measured": (
            "Outcomes are only observed for previously <em>approved</em> applicants &mdash; a structural "
            "selection bias that a naive model trained only on approved-applicant data inherits "
            "silently. Reject inference corrections were validated against simulated data specifically "
            "because the true outcome for a rejected applicant is, by definition, never observed in real "
            "data &mdash; there is no ground truth to check the correction against outside of a "
            "simulation built to contain one. Fairness was audited across sex, age, education and "
            "marital status using demographic parity, equal-opportunity difference and within-group "
            "calibration, and the accuracy&ndash;fairness tradeoff curve is presented as a policy "
            "decision rather than silently optimized away."
        ),
        "next": "Extend the fairness audit to intersectional subgroups rather than single protected attributes evaluated independently.",
        "stack": ["Python", "LightGBM", "scikit-learn", "SHAP", "WOE Scorecards", "FastAPI", "Docker"],
    },
    {
        "slug": "fpl",
        "name": "FPL AI Manager",
        "short": "Two models play the 2026/27 Fantasy Premier League season side by side &mdash; one under the real constraints, one with perfect freedom &mdash; to measure what continuity actually costs. Scored with real FPL points against the official gameweek average, and published live each gameweek.",
        "tags": ["Optimization", "Sequential Decisions", "No-Leakage", "Deployed"],
        "status": "LIVE",
        "headline_label": "COST OF CONTINUITY",
        "headline_value": "25",
        "headline_unit": "pts",
        "github": "https://github.com/MelvTheGoat/Fantasy-Premier-League",
        "live": FPL_LIVE_URL,
        "problem": (
            "Every FPL manager pays for continuity &mdash; one free transfer a week, &minus;4 for each "
            "extra, and a squad in January shaped by what was bought in August &mdash; and nobody can "
            "see the bill, because you only ever get to play one of the two possible seasons. "
            "<strong>The Manager</strong> carries one squad all year under the real constraints; "
            "<strong>Best XI of the Week</strong> rebuilds the best legal squad from scratch every "
            "gameweek. They are not competing. The gap between them is the measurement."
        ),
        "result": (
            "Both models are scored with real FPL points pulled from the API and never recalculated, "
            "tracked against the official gameweek average &mdash; the same yardstick every human "
            "manager is measured by. Nothing is graded against a simulation of itself. 574 tests, "
            "weighted toward the rules engine and the projection, where a silent error does the most damage."
        ),
        "flow": "FPL API (cached, rate-limited) → rules engine as pure logic → component-built expected points\n  → ILP squad + lineup + captaincy optimiser (PuLP/CBC)\n  → Best XI (one gameweek) vs The Manager (transfers, hits, chips) → locked picks, never regenerated",
        "hardest_title": "The no-leakage rule is enforced by the schema, not by discipline",
        "hardest": (
            "The season was already under way, so gameweek 1 onward had to be reconstructed &mdash; and "
            "a reconstruction that peeks is worse than no reconstruction, because it still looks fine. "
            "Three structures carry the rule: prices are snapshotted per gameweek so a GW7 decision is "
            "costed at GW7 prices; projections are keyed by the deadline they were made before; and "
            "writing picks for a gameweek that already has them <em>raises</em> rather than overwrites. "
            "That last refusal is the load-bearing one &mdash; regenerating a past gameweek with "
            "hindsight would quietly invalidate every result after it. The one honest leak is stated "
            "outright: backfilled gameweeks read injury status as it is now, because the API does not "
            "publish its history."
        ),
        "measured_title": "What the results actually showed",
        "measured": (
            "After the first four gameweeks: the Manager on 171 points, Best XI on 196 &mdash; the "
            "25-point gap the project exists to measure &mdash; and, less comfortably, "
            "<em>neither model has beaten the FPL average yet</em> (0/4 each). Small sample, but that "
            "is reported as it stands rather than explained away. Four bugs also reached the published "
            "site, and all four shared one shape worth naming: <strong>they produced plausible output "
            "instead of an error.</strong> A season published as zeros reads as a season that went "
            "badly, not as a broken deployment &mdash; which is why setup stages now gate on results "
            "before picks, and why stale-score detection re-scores whenever the results behind a score "
            "are newer than the score."
        ),
        "next": "A real backtest against a held-out prior season. The projection's component weights are currently reasoned rather than fitted, and only a held-out season says whether it is good or merely sensible.",
        # The repo also carries a render.yaml for an always-on paid instance,
        # but the live site is the GitHub Actions + Pages path, so that is what
        # is listed. Move the deployment and this entry moves with it.
        "stack": ["Python", "FastAPI", "PuLP / CBC", "SQLite", "React", "Docker", "GitHub Actions", "GitHub Pages"],
    },
    {
        "slug": "forecasting",
        "name": "Self-Operating Demand Forecasting Platform",
        "short": "An orchestrated, end-to-end forecasting pipeline for NYC taxi zones with asymmetric cost modeling, rolling-origin backtesting, and drift-triggered retraining gated on real cost improvement.",
        "tags": ["Forecasting", "MLOps", "Drift Monitoring"],
        "status": None,
        "headline_label": "COST REDUCTION",
        "headline_value": "25",
        "headline_unit": "%",
        "github": "https://github.com/MelvTheGoat/nyc-taxi-demand-forecast",
        "live": None,
        "problem": (
            "Point forecasts and symmetric error metrics don't reflect the real cost structure of "
            "demand planning, where under-forecasting (unmet demand) and over-forecasting (idle supply) "
            "have genuinely different costs &mdash; optimizing for the wrong metric produces a forecast "
            "that's statistically accurate and operationally expensive."
        ),
        "result": (
            "Modeled unmet demand at 3&times; the cost of idle supply and shipped the cost-optimal "
            "quantile rather than the median, cutting expected cost 25% against an identical model "
            "optimized on a symmetric metric, and beating a seasonal-naive baseline by 32%."
        ),
        "flow": "ingest → dbt/DuckDB transforms → rolling-origin backtest (6 folds)\n  → asymmetric cost-optimal quantile selection → drift monitoring (PSI/KS/MASE)\n  → champion/challenger promotion",
        "hardest_title": "Why asymmetric cost instead of MASE alone",
        "hardest": (
            "A model chosen purely to minimize MASE optimizes the wrong objective if the two error "
            "directions cost differently in the real system it feeds. Shipping the cost-optimal quantile "
            "&mdash; not the median, and not the metric-minimizing point forecast &mdash; means the "
            "model is trained toward the actual business objective rather than a proxy metric that "
            "happens to be convenient to optimize."
        ),
        "measured_title": "What the results actually showed",
        "measured": (
            "Automated leakage tests were built to fail the CI build if any feature reads past the "
            "forecast origin &mdash; a structural guardrail rather than a one-time manual check, because "
            "leakage in a forecasting pipeline produces backtests that look excellent and fail silently "
            "in production. Champion/challenger promotion is gated on a 2% out-of-sample cost margin "
            "specifically so a retrained model has to prove real improvement before replacing the "
            "one in production, not just look different."
        ),
        "next": "Extend the drift-triggered retraining to detect covariate shift in the raw ingestion data itself, ahead of it surfacing in downstream forecast error.",
        "stack": ["Python", "Prefect", "dbt-core", "DuckDB", "LightGBM", "MLflow", "Evidently", "FastAPI", "Docker", "GitHub Actions"],
    },
    {
        "slug": "uplift",
        "name": "Uplift Modeling &amp; Causal Targeting Study",
        "short": "Heterogeneous treatment effect estimation on a randomized marketing trial, validated against simulated ground truth, with a placebo-test null result reported rather than shipped as a win.",
        "tags": ["Causal Inference", "Experiment Design", "Uplift"],
        "status": None,
        "headline_label": "SAMPLE SIZE",
        "headline_value": "64,000",
        "headline_unit": "",
        "github": "https://github.com/MelvTheGoat/Uplift-Modelling-Decision",
        "live": None,
        "problem": (
            "Standard propensity models identify customers likely to convert &mdash; not customers who "
            "convert <em>because of</em> an intervention. Targeting on propensity alone wastes spend on "
            "customers who would have converted regardless, and misses the customers an intervention "
            "would actually move."
        ),
        "result": (
            "S-, T-, and X-learners plus a causal forest, each validated against simulated data with "
            "known individual treatment effects &mdash; since true counterfactuals are unobservable and "
            "no accuracy metric exists to check an uplift model against on real data alone."
        ),
        "flow": "randomized trial (n=64,000) → S/T/X-learners + causal forest\n  → Qini curves, AUUC, decile uplift tables → placebo, covariate-balance, seed-stability tests\n  → budget-constrained targeting policy",
        "hardest_title": "Why the placebo test mattered enough to report a null result",
        "hardest": (
            "The placebo test &mdash; assigning a fake treatment and checking whether the model finds a "
            "spurious effect &mdash; showed the ranking was indistinguishable from noise on the primary "
            "arm. That's the test that actually tells you whether an uplift model is finding a real "
            "signal or an artifact of the estimator. Reporting it, rather than quietly moving on to a "
            "more flattering result, is what makes the rest of the analysis trustworthy."
        ),
        "measured_title": "What the results actually showed",
        "measured": (
            "18.6% of customers were flagged as negative-uplift &mdash; predicted to respond "
            "<em>worse</em> to the intervention &mdash; and that segment measured +0.44 percentage "
            "points against the randomized holdout when checked. A negative result, reported plainly "
            "rather than shipped as a targeting win, because a decision memo that hides its own "
            "estimator's failure mode is worse than useless to whoever has to act on it."
        ),
        "next": "Re-run with a larger trial to check whether the placebo-test noise floor shrinks with more data, or reflects a genuine ceiling on detectable heterogeneity in this population.",
        "stack": ["Python", "EconML", "CausalML", "LightGBM", "scikit-learn", "Experiment Design"],
    },
]

# ---------------------------------------------------------------------------
# Writing — each post is rendered to writing/<slug>.html and listed on
# writing.html from this one list.
# ---------------------------------------------------------------------------

POSTS = [
    {
        "slug": "rag-refusal",
        "title": "Building a RAG system that refuses on purpose",
        "date": "19 September 2026",
        "summary": (
            "Hybrid retrieval, a citation guardrail that strips any marker the model cited but never "
            "actually retrieved, and a refusal-correctness score of 0.40 that turned out to be measuring "
            "the judge rather than the system."
        ),
        "lede": (
            "A compliance assistant that answers every question is worse than one that answers most of "
            "them. This is the reasoning behind the refusal mechanism in the "
            "<a href=\"../projects/rag.html\">Nigerian Fintech Compliance RAG Assistant</a>, and what "
            "happened when I tried to measure whether it worked."
        ),
        "body": """
        <h2>The failure mode that matters here</h2>
        <p>A retrieval-augmented system over CBN circulars and the NDPA has one job that outranks all
        the others: when the corpus does not contain the answer, say so. A confident paraphrase of an
        adjacent clause is not a partial success. Somebody acts on it, and the thing they act on has a
        regulator attached.</p>

        <p>That reframes refusal. It is not an error path bolted on at the end &mdash; it is a
        first-class output with the same standing as an answer, which means it needs to be enforced in
        more than one place and measured on its own terms.</p>

        <h2>Enforced in three places, not one</h2>
        <p>A refusal that lives only in the prompt is a suggestion. The system uses a sentinel token
        carried through three layers that do not trust each other:</p>

        <div class="flow">prompt      → emit the sentinel when context is insufficient
guardrail   → a sentinel response never renders as prose
evaluation  → the same sentinel is what the metric counts</div>

        <p>The third one is the part that is easy to skip and expensive to skip. If the harness scores
        refusals by looking for phrases like &ldquo;I don't know&rdquo;, then the metric and the system
        disagree about what a refusal <em>is</em>, and every number after that is measuring the gap
        between two definitions rather than the behaviour.</p>

        <p>On top of that sits post-generation citation verification: every marker in the output is
        checked against what retrieval actually returned, and any marker the model cited but never
        retrieved is stripped. Models invent citations that look exactly like real ones. The only
        reliable defence is to not take the model's word for what it read.</p>

        <h2>Why reciprocal rank fusion instead of blending scores</h2>
        <p>Retrieval is hybrid: BM25 for the terms a regulation actually uses &mdash; section numbers,
        &ldquo;Tier 1&rdquo;, defined phrases &mdash; and dense embeddings served through ONNX for
        everything phrased differently from the source.</p>

        <p>The obvious way to combine them is to add the scores. It does not work. BM25 is unbounded
        and will happily exceed 15 on a rare term; cosine similarity from a normalised embedder lives
        in a narrow 0.3&ndash;0.7 band. Add them and BM25 wins every ranking, not because it is more
        trustworthy but because its numbers are bigger.</p>

        <p>Min-max normalisation looks like the fix and introduces a subtler bug: it is computed
        per-query, so on a query where BM25 found nothing good, its best weak match gets rescaled to a
        confident 1.0. The normalisation manufactures confidence out of an empty result set.</p>

        <p>Reciprocal rank fusion sidesteps the whole problem by discarding the scores and keeping only
        the ranks. Rank 1 means the same thing regardless of which retriever produced it. Against a
        50-question labelled golden set the fused retriever reaches 0.96 recall@5 and 0.842 MRR, with
        no question missing its answer entirely in the top 10.</p>

        <h2>Chunking that cannot straddle a clause</h2>
        <p>Chunking is where citation integrity is won or lost. A fixed-window chunker will happily
        span the boundary between two clauses, and the moment it does, a citation points at a chunk
        that belongs to two different rules. The answer might still be right; the attribution cannot
        be.</p>

        <p>So chunking is section-aware and never merges across a document's own structural
        boundaries, which keeps every citation attributable to exactly one clause. That claim was then
        checked against a structure-blind fixed-window baseline rather than asserted &mdash; the
        cheapest way to find out that a principled-sounding design decision bought nothing is to build
        the unprincipled version and compare.</p>

        <h2>The number that was measuring the wrong thing</h2>
        <p>Refusal correctness came back at 0.40. Four in ten. On the system's single most important
        behaviour.</p>

        <p>The instinct is to start tuning &mdash; a stricter prompt, a higher retrieval threshold. I
        went looking for a specific failing case first, and found this one: a question about Kenyan
        data-protection rules retrieved the NDPA's cross-border-transfer clause. The retrieval is
        defensible; those texts genuinely share vocabulary. The system's own guardrail handled it. What
        failed was the offline stub judge, which decides correctness by lexical overlap and therefore
        reads real shared vocabulary as evidence that the question was answerable.</p>

        <p>So 0.40 is a measurement of the stub, not of the deployed system. That distinction is the
        whole result. It gets reported as a documented limitation of the offline harness, with
        re-validation against a live provider named as the next step &mdash; rather than as a claim
        about the real refusal rate in either direction. Reporting it as a system weakness would be
        false; quietly dropping it because it looked bad would be worse.</p>

        <h2>What the constraint bought</h2>
        <p>The whole thing runs on GCP Cloud Run inside roughly a 225MB peak footprint against a 2GB
        budget, with per-session and daily request caps enforced in application code so a public
        endpoint cannot run up an API bill. ONNX instead of eager PyTorch, brute-force search instead
        of a vector database, single-threaded inference: each one is a decision that a
        memory-constrained target forced, and each one turned out to be simpler to operate than the
        thing it replaced.</p>

        <p>The useful lesson is not about memory. It is that a real constraint does the work an
        architecture review is supposed to do &mdash; it deletes options before you get attached to
        them.</p>
        """,
    },
    {
        "slug": "evaluate-before-you-model",
        "title": "Why I evaluate before I model",
        "date": "19 September 2026",
        "summary": (
            "Decide the metric and the split before training anything, build the honest baseline first "
            "and report it even when it wins, and publish the number that did not flatter the project. "
            "The argument running through all eight."
        ),
        "lede": (
            "Every project on this site was built in the same order, and the order is the point. This "
            "is the argument for it, made with the numbers that came out of following it &mdash; "
            "including the ones I would rather not have had to write down."
        ),
        "body": """
        <h2>The metric is a design decision, not a reporting decision</h2>
        <p>Choosing a metric after training is choosing the metric that flatters what you already
        built. Choosing it first is choosing what the system is for.</p>

        <p>In <a href=\"../projects/credit-risk.html\">credit risk</a> that decision is calibration
        over ranking, and it is not a preference. Expected loss is a probability multiplied by an
        exposure. AUC tells you the applicants are in the right order; it says nothing about whether a
        stated 8% default probability corresponds to an 8% real-world rate. A model can have an
        excellent AUC and produce confidently wrong loss estimates that look statistically sound right
        up until somebody checks them against reality. So the benchmark against a WOE-binned logistic
        scorecard was run on Brier score, reliability diagrams and expected calibration error, and the
        model with the better AUC was not automatically the one that shipped.</p>

        <p>In <a href=\"../projects/forecasting.html\">demand forecasting</a> the same reasoning lands
        somewhere different. Unmet demand and idle supply do not cost the same, so a symmetric error
        metric optimises the wrong thing. Modelling unmet demand at 3&times; idle supply and shipping
        the cost-optimal quantile rather than the median cut expected cost by 25% on an
        <em>identical</em> model. Nothing about the model improved. The objective stopped being a
        proxy.</p>

        <h2>Build the honest baseline first, and report it when it wins</h2>
        <p>A baseline built after the model exists is built to lose. Built first, it is the thing that
        tells you whether the complicated version is worth operating.</p>

        <p>The <a href=\"../projects/fraud.html\">fraud project</a> is where this bit hardest. Three
        deep sequence architectures &mdash; GRU, temporal convolutional network, causally-masked
        Transformer &mdash; against a LightGBM baseline on engineered velocity and deviation features.
        The headline is that the sequence models cut expected cost per transaction by 27% under an
        explicit cost model. The honest version is that pre-drift, gradient boosting was marginally
        ahead: 0.956 against 0.950 PR-AUC, which is a tie.</p>

        <p>The entire 27% comes from robustness once the fraud pattern shifts. Reporting only the
        headline would be true and misleading, because it implies the sequence models are simply
        better. The pre-drift tie is what locates <em>why</em> they win, and it changes the
        recommendation: this is an argument for sequence models in a non-stationary threat environment
        specifically, not a general claim that deep learning wins.</p>

        <p>The same discipline shows up in the <a href=\"../projects/premier-league.html\">match
        predictor</a>, where 52.1% outcome accuracy means very little on its own and quite a lot next
        to the 43.2% you get by always backing the home side, and next to a tuned Elo-only baseline's
        log loss of 1.0061 against the model's 0.9948.</p>

        <h2>Report the negative result</h2>
        <p>This is the part that costs something, and it is the part that makes the rest of a portfolio
        readable.</p>

        <p>The <a href=\"../projects/uplift.html\">uplift study</a> ran a placebo test &mdash; assign a
        fake treatment, see whether the model finds an effect anyway &mdash; and the ranking came back
        indistinguishable from noise on the primary arm. That is the test that tells you whether an
        uplift model is finding signal or an artifact of the estimator, and it is reported, because a
        decision memo that hides its own estimator's failure mode is worse than useless to whoever has
        to act on it.</p>

        <p>The <a href=\"../projects/fpl.html\">FPL models</a> are currently 0 for 4 against the game's
        own average. That sits on the project page, in the results section, unhedged. The 25-point gap
        between the constrained manager and the unconstrained weekly rebuild is the measurement the
        project exists to take; the fact that neither has beaten the average yet is a small sample and
        also not noise-free good news, and it gets written down as both.</p>

        <p>And in <a href=\"../projects/reckon.html\">Reckon</a>, the prose-intake layer reads 94.4% of
        40 hand-labelled payment reports correctly &mdash; reports written by the same person who wrote
        the parser. The honest description is &ldquo;it has not failed on these yet&rdquo;, not an
        accuracy rate. The ten written afterwards and never used for tuning immediately found four real
        bugs, which is exactly what you would predict and exactly why the number is framed that
        way.</p>

        <h2>Make the guardrail structural</h2>
        <p>Every rule above is a rule somebody has to remember. The ones that survive contact with a
        deadline are the ones a system enforces on your behalf.</p>

        <ul class="cv-points">
          <li><strong>Forecasting:</strong> automated leakage tests fail the build if any feature reads
          past the forecast origin. Leakage produces backtests that look excellent and fail silently;
          a test that fails the build is the only version of that check that keeps working when you are
          busy.</li>
          <li><strong>FPL:</strong> writing picks for a gameweek that already has them raises an error
          rather than overwriting. Regenerating a past gameweek with hindsight would quietly invalidate
          every result after it, and the output would still look fine.</li>
          <li><strong>Match prediction:</strong> the feature table is built in one strictly
          chronological pass, so a feature <em>cannot</em> read a result that has not been fed in yet.
          The guarantee is structural rather than a matter of remembering to filter.</li>
          <li><strong>Reckon:</strong> the close/review threshold is computed from two cost constants
          &mdash; &#8358;60 to check a match that was fine, &#8358;5,000 to close one that was wrong.
          Change the costs and the line moves on its own, instead of a number chosen by eye drifting
          out of date in silence.</li>
        </ul>

        <h2>Why two of these are football projects</h2>
        <p>A portfolio project can be tuned until the backtest looks good and nobody ever finds out.
        That is the structural weakness of the whole genre, mine included.</p>

        <p>Football does not allow it. The match predictor publishes probabilities before kick-off and
        never edits them; the FPL models lock a squad before each deadline and refuse to regenerate a
        past gameweek at all. Both keep a public record that is free to disagree with them, and one of
        them currently does. That is the strongest evidence I can offer that the evaluation discipline
        on the rest of this site is real rather than retrospective &mdash; and it is the reason those
        two projects are here at all.</p>
        """,
    },
]


# ---------------------------------------------------------------------------
# CV data — education, experience, skills and certificates, straight from the
# resume PDF in /assets. Kept here so the resume page stays readable without
# downloading anything, and so both pages can never drift apart.
# ---------------------------------------------------------------------------

EDUCATION = [
    {
        "place": "SQI College of ICT",
        "what": "Professional Diploma in Artificial Intelligence",
        "where": "Ibadan, Nigeria",
        "when": "July 2025 &ndash; Present",
    },
    {
        "place": "University of Ibadan",
        "what": "B.Sc. in Statistics",
        "where": "Oyo, Nigeria",
        "when": "January 2021 &ndash; March 2025",
    },
]

EXPERIENCE = [
    {
        "place": "SQI College of ICT",
        "what": "Machine Learning Instructor",
        "where": "Ibadan, Nigeria",
        "when": "March 2026 &ndash; Present",
        "points": [
            "Teaching machine learning and deep learning to student cohorts, covering statistical "
            "foundations, classical ML algorithms, neural architectures, sequence models, and "
            "production evaluation metrics.",
            "Instructing students on data analysis, feature engineering, and model building with "
            "PyTorch, scikit-learn, Pandas, and NumPy.",
            "Guiding learners through end-to-end ML projects on real-world datasets.",
        ],
    },
    {
        "place": "Nigerian Institute of Social and Economic Research (NISER)",
        "what": "Internal Auditor",
        "where": "Ibadan, Nigeria",
        "when": "May 2024 &ndash; July 2024",
        "points": [
            "Analyzed financial and operational records to identify inconsistencies and "
            "irregularities, performing manual anomaly detection across complex transactional "
            "datasets &mdash; the same problem the Reckon project later automated.",
        ],
    },
]

SKILLS = [
    ("AI &amp; LLM Systems", [
        "Retrieval-Augmented Generation (RAG)", "Hybrid Search (BM25, Dense Embeddings, RRF)",
        "LLM Evaluation &amp; Guardrails", "Prompt Engineering", "Citation Verification",
        "Hugging Face", "ONNX Runtime",
    ]),
    ("Machine Learning", [
        "PyTorch", "scikit-learn", "LightGBM", "XGBoost", "Deep Learning",
        "Sequence Models (GRU, TCN, Transformers)",
        "Model Calibration (Isotonic, Platt, Temperature Scaling)", "SHAP", "Feature Engineering",
    ]),
    ("Statistics &amp; Causal Inference", [
        "Statistical Inference", "Experiment Design", "Power Analysis",
        "Causal Inference (S/T/X-Learners, Causal Forests)", "Uplift Modeling",
        "Time-Series Backtesting", "Logistic Regression", "WOE Scorecards",
    ]),
    ("Engineering &amp; MLOps", [
        "Python", "SQL", "DuckDB", "FastAPI", "Docker", "GCP Cloud Run", "Railway", "Vercel",
        "Prefect", "dbt-core", "MLflow", "Evidently", "CI/CD (GitHub Actions)", "Git", "Pytest",
        "Streamlit", "React",
    ]),
    ("Payments &amp; Domain", [
        "Transaction Fraud Detection", "Credit Risk Decisioning", "Payment Reconciliation",
        "Regulatory Compliance (CBN/NDPA)", "Demand Forecasting",
    ]),
]

CERTIFICATES = [
    "Google Data Analytics Professional Certificate",
    "Google Advanced Data Analytics Professional Certificate",
    "Claude Code In Action",
]


def summary_line():
    return (
        "Machine Learning &amp; AI Engineer with a Statistics background, specializing in "
        "probabilistic ML and production system design &mdash; systems where the probability has to "
        "be trustworthy, not merely the label. Experience spans classical ML and deep learning "
        "&mdash; forecasting, credit risk, and sequence-based fraud pipelines through to "
        "retrieval-augmented generation and financial reconciliation systems &mdash; with consistent "
        "depth in temporally honest validation, calibrated decisioning, evaluation design, "
        "containerized serving, and operational reliability."
    )


# ---------------------------------------------------------------------------
# HOME
# ---------------------------------------------------------------------------

def build_home():
    featured = PROJECTS[:3]  # reckon, premier-league, fraud
    cards = ""
    for p in featured:
        status = f'<span class="card-status">{p["status"]}</span>' if p["status"] else ""
        cards += f"""
        <a class="card" href="projects/{p['slug']}.html" style="text-decoration:none;">
          <div class="tags">
            {''.join(f'<span class="tag">{t}</span>' for t in p['tags'][:3])}
          </div>
          <h3>{p['name']}</h3>
          <p class="card-desc">{p['short']}</p>
          {reading(p['headline_label'], p['headline_value'], p['headline_unit'], small=True)}
          <span class="card-link">{status or 'View project &rarr;'}</span>
        </a>"""

    body = f"""  <main>
    <section class="hero">
      <div class="hero-grid" aria-hidden="true"></div>
      <div class="wrap hero-inner">
        <div class="eyebrow">Lagos, Nigeria &mdash; Open to DS / ML / DL / AI roles</div>
        <h1>I build systems where the probability has to be right, not just plausible.</h1>
        <div class="role">Machine Learning &amp; AI Engineer</div>
        <p class="lede">Payment reconciliation, fraud detection, credit risk, forecasting, causal
        inference, a deployed RAG system, and two football models that publish their predictions
        before the results are known &mdash; each one evaluated the way a production system is
        evaluated, not the way a portfolio project usually is.</p>
        <div class="btn-row">
          <a class="btn btn-primary" href="{RAG_LIVE_URL}" target="_blank" rel="noopener">Try the live demo &rarr;</a>
          <a class="btn" href="projects.html">View all projects</a>
        </div>
        <div class="reading-row">
          {reading('SYSTEMS BUILT', '8', 'projects')}
          {reading('DEPLOYED &amp; LIVE', '5', 'public')}
          {reading('COST REDUCTION', '25&ndash;27', '%')}
        </div>
      </div>
    </section>

    <section>
      <div class="wrap">
        <div class="section-head">
          <h2>Running right now</h2>
          <a href="projects.html">All projects &rarr;</a>
        </div>

        <div class="demo-callout">
          <div>
            <div class="status"><span class="pulse"></span>Live &mdash; Railway</div>
            <h3>Reckon &mdash; Payment Reconciliation</h3>
            <p>The review queue itself: the cases the system could not prove, ranked by money at risk,
            each with a suggested match and the reasons for it written out. 76.1% of a month's payments
            never reach this screen at all.</p>
          </div>
          <a class="btn btn-primary" href="{RECKON_LIVE_URL}" target="_blank" rel="noopener">Open the queue &rarr;</a>
        </div>

        <div class="demo-callout" style="margin-top: 1.5rem;">
          <div>
            <div class="status"><span class="pulse"></span>Live &mdash; Vercel, retrained weekly</div>
            <h3>Premier League Match Predictor</h3>
            <p>Three-way probabilities and a scoreline for every fixture in the current gameweek, plus
            the full record of what it predicted for every gameweek already played &mdash; published
            before kick-off and never edited afterwards.</p>
          </div>
          <a class="btn btn-primary" href="{PL_LIVE_URL}" target="_blank" rel="noopener">Open the site &rarr;</a>
        </div>

        <div class="demo-callout" style="margin-top: 1.5rem;">
          <div>
            <div class="status"><span class="pulse"></span>Live &mdash; GCP Cloud Run</div>
            <h3>Nigerian Fintech Compliance RAG Assistant</h3>
            <p>Ask it a real regulatory question &mdash; CBN circulars, the NDPA &mdash; and get a
            grounded, cited answer. It refuses rather than guesses when the source doesn't support one.</p>
          </div>
          <a class="btn btn-primary" href="{RAG_LIVE_URL}" target="_blank" rel="noopener">Open the demo &rarr;</a>
        </div>

        <p class="also-live">Also live &mdash;
          <a href="{CREDIT_LIVE_URL}" target="_blank" rel="noopener">Credit Risk Decisioning &amp; Fairness Audit</a>
          (GCP Cloud Run) and
          <a href="{FPL_LIVE_URL}" target="_blank" rel="noopener">FPL AI Manager</a>
          (GitHub Pages, republished every gameweek).
        </p>
      </div>
    </section>

    <section>
      <div class="wrap">
        <div class="section-head">
          <h2>Featured work</h2>
          <a href="projects.html">All projects &rarr;</a>
        </div>
        <div class="project-grid">{cards}
        </div>
      </div>
    </section>

    <div class="pattern-strip">
      <div class="wrap">
        <div class="eyebrow">The pattern across all eight</div>
        <h2 style="color:#fff; max-width: 24ch;">Every model earns production through a measured comparison, not a vibe.</h2>
        <div class="pattern-grid">
          <div class="pattern-item"><span class="num">01</span><p>Evaluate before modeling &mdash; the metric and the split get decided before a single model is trained.</p></div>
          <div class="pattern-item"><span class="num">02</span><p>Build the honest baseline first, and report it even when it wins.</p></div>
          <div class="pattern-item"><span class="num">03</span><p>Report the negative result &mdash; a placebo test, a limitation, a number that didn't flatter the project.</p></div>
          <div class="pattern-item"><span class="num">04</span><p>Calibration over ranking, wherever the output feeds a real decision.</p></div>
        </div>
      </div>
    </div>

    <div class="wrap">
      <div class="currently"><span class="pulse"></span>Currently teaching Machine Learning at SQI College of ICT, Ibadan &mdash; open to remote or relocation roles.</div>
    </div>
  </main>
"""
    return page(
        f"{NAME} &mdash; Machine Learning &amp; AI Engineer",
        "Machine Learning and AI Engineer specializing in calibrated, rigorously evaluated systems: payment reconciliation, fraud detection, credit risk, forecasting, causal inference, a deployed RAG assistant, and live football prediction models.",
        "home", body,
    )


# ---------------------------------------------------------------------------
# PROJECTS INDEX
# ---------------------------------------------------------------------------

def build_projects_index():
    cards = ""
    for p in PROJECTS:
        status = f'<span class="card-status">{p["status"]}</span>' if p["status"] else '<span class="card-link">View &rarr;</span>'
        cards += f"""
        <a class="card" href="projects/{p['slug']}.html" style="text-decoration:none;">
          <div class="card-main">
            <div class="tags">
              {''.join(f'<span class="tag">{t}</span>' for t in p['tags'])}
            </div>
            <h3>{p['name']}</h3>
            <p class="card-desc">{p['short']}</p>
          </div>
          <div>
            {reading(p['headline_label'], p['headline_value'], p['headline_unit'])}
            <div style="margin-top:10px;">{status}</div>
          </div>
        </a>"""

    body = f"""  <main>
    <section class="tight">
      <div class="wrap">
        <div class="eyebrow">Eight systems, one evaluation discipline</div>
        <h1>Projects</h1>
        <p class="lede" style="max-width:60ch;">Each page follows the same structure on purpose: the
        problem, the headline result, the architecture, the one decision most worth defending, and
        what the results actually showed &mdash; including the parts that didn't flatter the project.</p>
      </div>
    </section>
    <section class="tight">
      <div class="wrap">
        <div class="project-grid full">{cards}
        </div>
      </div>
    </section>
  </main>
"""
    return page(
        f"Projects &mdash; {NAME}",
        "Eight ML and AI projects: payment reconciliation, football match prediction, fraud detection, a deployed RAG assistant, credit risk, FPL squad optimization, demand forecasting, and causal inference.",
        "projects", body,
    )


# ---------------------------------------------------------------------------
# PROJECT DETAIL PAGES
# ---------------------------------------------------------------------------

def build_project_page(p, idx):
    live_btn = f'<a class="btn btn-primary" href="{p["live"]}" target="_blank" rel="noopener">Open live demo &rarr;</a>' if p["live"] else ""
    github_btn = f'<a class="btn" href="{p["github"]}" target="_blank" rel="noopener">View on GitHub &rarr;</a>'

    next_p = PROJECTS[(idx + 1) % len(PROJECTS)]

    body = f"""  <main>
    <section class="project-hero">
      <div class="wrap">
        <div class="tags">
          {''.join(f'<span class="tag">{t}</span>' for t in p['tags'])}
        </div>
        <h1>{p['name']}</h1>
        <p class="subtitle">{p['short']}</p>
        <div class="meta-row">
          {live_btn}
          {github_btn}
        </div>
      </div>
    </section>

    <section class="detail-section">
      <div class="wrap">
        <h2><span class="num">01</span>The problem</h2>
        <p>{p['problem']}</p>
      </div>
    </section>

    <section class="detail-section">
      <div class="wrap">
        <h2><span class="num">02</span>The result</h2>
        <div class="result-banner">
          <div class="eyebrow">Headline number</div>
          <p>{p['result']}</p>
        </div>
      </div>
    </section>

    <section class="detail-section">
      <div class="wrap">
        <h2><span class="num">03</span>Architecture</h2>
        <div class="flow">{p['flow']}</div>
      </div>
    </section>

    <section class="detail-section">
      <div class="wrap">
        <h2><span class="num">04</span>The hardest decision</h2>
        <div class="decision-block">
          <h4>{p['hardest_title']}</h4>
          <p>{p['hardest']}</p>
        </div>
      </div>
    </section>

    <section class="detail-section">
      <div class="wrap">
        <h2><span class="num">05</span>What the results actually showed</h2>
        <div class="measured-box">
          <div class="eyebrow">Measured, not assumed</div>
          <p>{p['measured']}</p>
        </div>
      </div>
    </section>

    <section class="detail-section">
      <div class="wrap">
        <h2><span class="num">06</span>What's next</h2>
        <p>{p['next']}</p>
      </div>
    </section>

    <section class="detail-section">
      <div class="wrap">
        <h2><span class="num">07</span>Stack</h2>
        <div class="stack-tags">
          {''.join(f'<span class="tag">{s}</span>' for s in p['stack'])}
        </div>
      </div>
    </section>

    <div class="wrap">
      <div class="next-project">
        <span class="eyebrow" style="margin-bottom:0;">Next project</span>
        <a href="{next_p['slug']}.html">{next_p['name']} &rarr;</a>
      </div>
    </div>
  </main>
"""
    return page(
        f"{p['name']} &mdash; {NAME}",
        p['short'],
        "projects", body, depth="../",
    )


# ---------------------------------------------------------------------------
# WRITING
# ---------------------------------------------------------------------------

def build_writing():
    cards = ""
    for p in POSTS:
        cards += f"""
        <div class="post-card">
          <span class="post-date">{p['date']}</span>
          <h3><a href="writing/{p['slug']}.html">{p['title']}</a></h3>
          <p>{p['summary']}</p>
          <a class="card-link" href="writing/{p['slug']}.html">Read the full post &rarr;</a>
        </div>
"""

    body = f"""  <main>
    <section class="tight">
      <div class="wrap">
        <div class="eyebrow">Notes on building this way</div>
        <h1>Writing</h1>
        <p class="lede" style="max-width:60ch;">Longer-form pieces on the reasoning behind these
        projects &mdash; written for anyone deciding whether to trust a number, including future me.</p>
      </div>
    </section>
    <section class="tight">
      <div class="wrap">{cards}
        <div class="empty-note">
          More as each project's evaluation work matures. Every project page carries the same
          reasoning in full, including the section on what the results actually showed.
        </div>
      </div>
    </section>
  </main>
"""
    return page(
        f"Writing &mdash; {NAME}",
        "Notes on evaluation, calibration, and building ML/AI systems that report their own limitations honestly.",
        "writing", body,
    )


def build_post_page(p, idx):
    others = [q for q in POSTS if q["slug"] != p["slug"]]
    more = ""
    if others:
        q = others[0]
        more = f"""
    <div class="wrap">
      <div class="next-project">
        <span class="eyebrow" style="margin-bottom:0;">Next post</span>
        <a href="{q['slug']}.html">{q['title']} &rarr;</a>
      </div>
    </div>"""

    body = f"""  <main>
    <section class="project-hero">
      <div class="wrap">
        <span class="post-date">{p['date']}</span>
        <h1>{p['title']}</h1>
        <p class="subtitle">{p['lede']}</p>
      </div>
    </section>

    <section class="detail-section">
      <div class="wrap">
        <div class="prose">{p['body'].strip()}</div>
      </div>
    </section>
{more}
  </main>
"""
    return page(
        f"{p['title']} &mdash; {NAME}",
        p['summary'],
        "writing", body, depth="../",
    )


# ---------------------------------------------------------------------------
# ABOUT
# ---------------------------------------------------------------------------

def skills_html():
    out = ""
    for group, items in SKILLS:
        out += f"""<div class="skill-group">
            <div class="eyebrow">{group}</div>
            <div class="stack-tags">
              {''.join(f'<span class="tag">{i}</span>' for i in items)}
            </div>
          </div>
          """
    return out.rstrip()


def build_about():
    skills = skills_html()
    body = f"""  <main>
    <section class="tight">
      <div class="wrap">
        <div class="eyebrow">About</div>
        <h1>{NAME}</h1>
      </div>
    </section>
    <section class="tight">
      <div class="wrap two-col">
        <div>
          <div class="avatar-box"><img src="assets/photo_2026-08-16_14-26-22.jpg" alt="{NAME}" style="width: 100%; height: auto; border-radius: 4px;"></div>
        </div>
        <div>
          <p class="lede">{summary_line()}</p>

          <h3>Path</h3>
          <p>B.Sc. in Statistics from the University of Ibadan (2021&ndash;2025), then a deliberate,
          self-directed move into machine learning and AI &mdash; now formalized through a Professional
          Diploma in Artificial Intelligence at SQI College of ICT. Not the traditional CS-degree route
          into ML, and I don't treat that as something to explain away &mdash; the eight projects on
          this site are the actual evidence of whether it worked.</p>

          <h3>Why Statistics shapes how I build</h3>
          <p>Every project on this site prioritizes calibration &mdash; a true probability, not just a
          well-ranked score &mdash; over a flashier ranking metric wherever the output feeds a real
          decision. That instinct traces directly back to a Statistics background, not something picked
          up from an ML tutorial. It shows up as reliability diagrams in the credit risk project,
          temperature scaling in the fraud model, and a placebo test reported honestly, even when it
          came back null, in the uplift study.</p>

          <h3>Teaching</h3>
          <p>Currently a Machine Learning Instructor at SQI College of ICT, teaching statistical
          foundations, classical ML, neural architectures, sequence models, and production evaluation
          metrics to student cohorts. Teaching has sharpened something specific: the ability to explain
          a technical decision clearly to someone who wasn't in the room when it was made &mdash; which
          is exactly what every project writeup on this site is trying to do.</p>

          <h3>Building from Lagos</h3>
          <p>Every architectural decision in the RAG project &mdash; ONNX over PyTorch, brute-force
          search instead of a vector database, single-threaded inference &mdash; traces back to
          designing for a genuinely constrained memory budget rather than assuming unlimited cloud
          resources by default. That's not a workaround; it's an engineering instinct that's harder to
          develop when infrastructure is never actually the constraint.</p>

          <h3>Why two of these are football projects</h3>
          <p>A portfolio project can be tuned until the backtest looks good, and nobody ever finds out.
          Football does not allow that. The <a href="projects/premier-league.html">match predictor</a>
          publishes its probabilities before kick-off and never edits them afterwards; the
          <a href="projects/fpl.html">FPL models</a> lock their squads before each deadline and refuse
          to regenerate a past gameweek at all. Both keep a public record that can disagree with them
          &mdash; and currently does: neither FPL model has beaten the game's average yet. That is the
          strongest available evidence that the evaluation discipline on the rest of this site is real
          and not retrospective.</p>
        </div>
      </div>
    </section>

    <section class="tight">
      <div class="wrap">
        <div class="section-head">
          <h2>Technical skills</h2>
          <a href="resume.html">Full CV &rarr;</a>
        </div>
        <div class="skill-groups">
          {skills}
        </div>
      </div>
    </section>
  </main>
"""
    return page(
        f"About &mdash; {NAME}",
        f"Statistics background, self-directed path into ML/AI, currently teaching at SQI College of ICT, based in {LOCATION}.",
        "about", body,
    )


# ---------------------------------------------------------------------------
# RESUME
# ---------------------------------------------------------------------------

def cv_entries(rows):
    out = ""
    for r in rows:
        points = ""
        if r.get("points"):
            points = "<ul class=\"cv-points\">" + "".join(f"<li>{p}</li>" for p in r["points"]) + "</ul>"
        out += f"""<div class="cv-entry">
            <div class="cv-head">
              <h3>{r['place']}</h3>
              <span class="cv-when">{r['when']}</span>
            </div>
            <div class="cv-role">{r['what']} &mdash; {r['where']}</div>
            {points}
          </div>
          """
    return out.rstrip()


def build_resume():
    education = cv_entries(EDUCATION)
    experience = cv_entries(EXPERIENCE)
    skills = skills_html()
    certs = "".join(f"<li>{c}</li>" for c in CERTIFICATES)

    body = f"""  <main>
    <section class="tight">
      <div class="wrap">
        <div class="eyebrow">Resume</div>
        <h1>CV</h1>
        <p class="lede" style="max-width:62ch;">{summary_line()}</p>
        <div class="btn-row" style="margin-top:18px;">
          <a class="btn btn-primary" href="assets/resume.pdf" download>Download PDF</a>
          <a class="btn" href="projects.html">See the projects &rarr;</a>
        </div>
      </div>
    </section>

    <section class="tight">
      <div class="wrap">
        <div class="section-head"><h2>Experience</h2></div>
        {experience}
      </div>
    </section>

    <section class="tight">
      <div class="wrap">
        <div class="section-head"><h2>Education</h2></div>
        {education}
      </div>
    </section>

    <section class="tight">
      <div class="wrap">
        <div class="section-head">
          <h2>Technical skills</h2>
          <a href="projects.html">Where each one is used &rarr;</a>
        </div>
        <div class="skill-groups">
          {skills}
        </div>
      </div>
    </section>

    <section class="tight">
      <div class="wrap">
        <div class="section-head"><h2>Awards &amp; certificates</h2></div>
        <ul class="cv-points">{certs}</ul>
      </div>
    </section>

    <section class="tight">
      <div class="wrap">
        <div class="section-head"><h2>The PDF</h2></div>
        <div class="resume-embed">
          <iframe src="assets/resume.pdf" title="Resume"></iframe>
        </div>
        <p class="resume-fallback">
          If the embed doesn't load in your browser,
          <a href="assets/resume.pdf" download>download the PDF</a> instead.
        </p>
      </div>
    </section>
  </main>
"""
    return page(
        f"Resume &mdash; {NAME}",
        f"CV for {NAME} &mdash; Machine Learning &amp; AI Engineer: experience, education, technical skills, and certificates.",
        "resume", body,
    )


# ---------------------------------------------------------------------------
# CONTACT
# ---------------------------------------------------------------------------

def build_contact():
    body = f"""  <main>
    <section class="tight">
      <div class="wrap">
        <div class="eyebrow">Get in touch</div>
        <h1>Contact</h1>
        <p class="lede" style="max-width:56ch;">Happy to talk about a role, a project, or just the
        reasoning behind any of the evaluation decisions on this site.</p>
        <div class="contact-grid">
          <div class="contact-card">
            <div class="eyebrow">Email</div>
            <a href="mailto:{EMAIL}">{EMAIL}</a>
          </div>
          <div class="contact-card">
            <div class="eyebrow">LinkedIn</div>
            <a href="{LINKEDIN}" target="_blank" rel="noopener">oluwatobi-mayungbo</a>
          </div>
          <div class="contact-card">
            <div class="eyebrow">GitHub</div>
            <a href="{GITHUB_PROFILE}" target="_blank" rel="noopener">MelvTheGoat</a>
          </div>
        </div>
        <div style="margin-top: 28px;">
          <a class="btn btn-primary" href="https://calendly.com/mlvyn-t" target="_blank" rel="noopener">Book a Chat on Calendly &rarr;</a>
        </div>
      </div>
    </section>
  </main>
"""
    return page(
        f"Contact &mdash; {NAME}",
        f"Get in touch &mdash; {EMAIL}",
        "contact", body,
    )


# ---------------------------------------------------------------------------
# Write everything
# ---------------------------------------------------------------------------

def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", path)


def main():
    write("index.html", build_home())
    write("projects.html", build_projects_index())
    write("writing.html", build_writing())
    write("about.html", build_about())
    write("resume.html", build_resume())
    write("contact.html", build_contact())
    for i, p in enumerate(PROJECTS):
        write(f"projects/{p['slug']}.html", build_project_page(p, i))
    for i, p in enumerate(POSTS):
        write(f"writing/{p['slug']}.html", build_post_page(p, i))
    print("\nDone. Open index.html in a browser, or deploy the whole folder as-is.")


if __name__ == "__main__":
    main()
