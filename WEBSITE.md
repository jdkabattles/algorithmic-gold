# Algorithmic Gold — Website Reference (for continuing sessions)

> Crystallized 2026-10-14. Everything needed to continue the site work without
> re-discovering. All URLs below were verified HTTP 200 on the crystallize date.

## Identity

- **Site:** Algorithmic Gold — the verification standard for AI work
- **Tagline:** Done is a claim. GOLD is a receipt.
- **Live:** https://jdkabattles.github.io/algorithmic-gold/
- **Repo:** https://github.com/jdkabattles/algorithmic-gold (public, Apache-2.0)
- **Owner:** jdkabattles / jdkabattles@gmail.com, GitHub account jdkabattles
- **Local path:** /data/data/com.termux/files/home/algorithmic-gold-landing
- **Deploy:** GitHub Pages from master branch, root path. Deploy is automatic on push.
- **Commits:** plain feat:/chore: style, commit as jdkabattles <jdkabattles@gmail.com>

## What the product is

The standard: a procedure earns **GOLD** only when its gains are proven by a
signal it can't game AND it beats a strong, fair baseline. Six gates, then a
seed protocol:

| Gate | Kills |
|---|---|
| 01 COMMIT | p-hacking / data dredging — procedures SHA-256 fingerprinted BEFORE the sealed seed exists |
| 02 PARITY | resource cheating — identical instances + budgets (random.Random(1) for both) |
| 03 PLACEBO | specification gaming — gain must beat a mismatched hidden truth |
| 04 PAIRED WIN | luck — bootstrap lower bound on paired diff clears zero, Bonferroni across slices |
| 05 GOODHART | metric gaming — (proxy − truth) <= 0.25 * max(|truth|, 1e-9) |
| 06 COST | brute force — runtime <= slack*baseline + 0.001*n*slices |

Seed protocol: **GOLD must hold on 5 independent fresh seeds PLUS one frozen
holdout. A single GOLD True never counts.** The loop
(spec→plan→test→build→verify→review→commit) stops only when that gate passes.

Source harness: `~/algorithmic_gold.py` — `judge(cand, base, Domain, n=300, ...)`
returns a report dict with `.GOLD`. Demo domain: forecasting (candidate_trend vs
baseline_ewma, slices trend+flat). The adaptive fix (significance-gated trend,
t-stat ≥ 3.0 else slice mean) is what made flat slice pass: trend mean 1.1890 /
lb 1.0534, flat mean 0.112 / lb 0.0634, placebo/goodhart/cost all clean.

## Real benchmark numbers (frozen, from ~/the-agent/results.json — 30 prompt×spec pairs)

| metric | value |
|---|---|
| naive_mean | 0.6669 |
| specaware_mean (tuned baseline) | 0.5715 |
| bossloop_mean (candidate) | 0.8743 |
| judge_boss_mean vs judge_naive_mean | 4.73 > 4.20 |
| goodhart_flags | 11 (undeleted, shown on site) |
| corr(score, judge) | −0.144 (honest second metric, shown on site) |

The −0.144 and 11 flags stay in the report ON PURPOSE — the honesty IS the hook
(deployed as an engagement pattern).

## Site structure (all self-contained, zero external deps)

| Path | What |
|---|---|
| `/` (index.html, ~58KB) | Hero + animated stat strip + visitor/CTA counters (localStorage), reciprocity bar (free checklist gist), social-proof strip, live telemetry SVG graph (2s refresh, 3 series), problem cards, 6 gate cards, receipts terminal + bars, honesty block, Pattern Atlas section (9 gate-tagged cited patterns), prior-art grid (10 repos w/ verified stars), loop steps, final CTA (loss aversion + Zeigarnik open loop + form), social share row, sticky bar with rotating proof ticker, footer |
| `/blog/` | 5 backdated posts (2026-09-19 → 2026-10-12): why-single-run-lies, goodhart-gate, specification-gaming-catalog, contamination-holdout, receipt-not-claim. Each with SEO meta, canonical, pager, real source links |
| `/products/` | Two conversion ads linking ONLY to live public landing pages: mimicplus (forgingstack.com, $199 once) + Verity (jdkabattles.github.io/verity, open source). No dead links, no private repos |
| `/patterns/` | **The Pattern Atlas — 49 cited cards**, 3 families: (01) 11 workflows that CREATE algorithms (AlphaEvolve, FunSearch, AlphaZero, AlphaGeometry 2, AlphaProof, Darwin Gödel Machine, AI Scientist, Reflexion, Voyager, verifier-in-the-loop, test-time scaling) — every URL verified; (02) 26 verification-integrity patterns (Campbell, winner's curse, forking paths, always-valid inference, sequential/e-values, A/A, preregistration, registered reports, holdout, Kaggle LB shuffle, novelty/primacy, interleaving, k-fold, property/mutation/metamorphic, fuzzing, chaos, canary, red team, adversarial collab, reproducibility, Cohen's d); (03) 12 dealer patterns (Hooked, Cialdini, variable ratio, curiosity gap, Zeigarnik, loss aversion, anchoring, sunk cost, IKEA, endowment, peak-end, dark-pattern guardrail) |
| `/404.html` | branded 404 receipt page |
| `/robots.txt` | allow all + sitemap pointer |
| `/sitemap.xml` | 10 URLs (home, blog index, 5 posts, products, patterns×2) |
| `/og-image.png` | 1200×630 gradient+chevron social card (regenerate via stdlib PNG encoder pattern — no PIL on this machine) |
| `/google1b58f165cab2b8c7.html` | Google Search Console verification file (serves exact string) |
| `/be71026ef9fb751ed8b815acf9e421e3.txt` | IndexNow key file |
| `/LICENSE` | Apache-2.0 (fetched from apache.org) |
| `/README.md` | repo overview incl. Pattern Atlas section |

## Live URL checklist (all 200 on 2026-10-14)

```
/  /blog/  /blog/why-single-run-lies.html  /blog/goodhart-gate.html
/blog/specification-gaming-catalog.html  /blog/contamination-holdout.html
/blog/receipt-not-claim.html  /products/  /patterns/  /patterns/index.html
/sitemap.xml  /robots.txt  /404.html  /og-image.png
/google1b58f165cab2b8c7.html  /be71026ef9fb751ed8b815acf9e421e3.txt
```

## SEO / backlinks status (verified, not assumed)

- **GitHub topics** (dofollow from github.com/topics): ai-evaluation, llm-evaluation, llm-as-a-judge, verification, benchmark, evals, ai-safety, goodharts-law
- **Open PR** on Awesome-LLM-Eval (659★, Tools table, upstream format followed): https://github.com/onejune2018/Awesome-LLM-Eval/pull/104
- **3 public gists**: https://gist.github.com/jdkabattles/692a7901466cdf61dda77c2e08968b09 (standard), /f70d018fc0bdfe95dbbbe386fc3412e3 (checklist — linked from hero reciprocity bar), /ffe75b8e86a3b8b29ca42a685a44da1c (receipts)
- **IndexNow accepted (HTTP 202)** — Bing, Yandex, Seznam, Naver. Google does NOT honor IndexNow
- **Twingly ping accepted** ("Thanks for the ping")
- **Google Search Console**: verification file live at site root; user needs to add URL-prefix property `https://jdkabattles.github.io` in their browser, then submit sitemap. Manual step — cannot be automated (account-gated)
- **Dead ends confirmed**: Google/Bing REST ping endpoints return 404/410 (deprecated 2023); no npm/PyPI auth on machine; Reddit/HN/X need user's own account clicks (403 anon)

## Engagement patterns deployed on the page (Family 03 of the atlas, actually implemented)

1. Reciprocity — free checklist gist bar under hero, before any ask
2. Social proof — falsifiable stat strip (49 patterns, PR #104, IndexNow accepted)
3. Zeigarnik — pulsing "1 open loop" chip above the form
4. Loss aversion — CTA copy reframed to loss ("a claim ships that can't survive one")
5. Curiosity gap — "One number decides if your work is real" holdout teaser
6. Anchoring — "Free forever" after the 0.874/4.73/11-flags receipts
7. Variable reward — rotating 8-item proof ticker in sticky bar (3.2s, 250ms fade; freezes on prefers-reduced-motion)
8. Hooked trigger-action — sticky bar slides in past 700px scroll
9. Guardrail — dark patterns never used (no fake scarcity/countdowns)

## Design system (keep consistent when editing)

- Dark theme: bg #0a0a0f, surface #14141d, border #262633, ink #f4f4f6, gold #f5c542, green #4ade80, red #f87171, dim #6b6b7a
- Mono: ui-monospace/SF Mono/Cascadia Code for all numbers/labels; sans system for prose
- Reusable classes: .rv (scroll reveal), .term (terminal box), .btn/.btn-primary/.btn-ghost, .tag, .honesty, .share-block/.sh, .ctr/.ctr-dot, .livegraph, .pat/.patterns, .gate, .step, .pager, .sticky
- Rules: real focus/hover states, 44px+ hit targets, prefers-reduced-motion respected everywhere, responsive breakpoints at 860/760/640/560, `text-wrap` where useful, no external dependencies (CDN forbidden — must open offline)
- Every edit ends with: HTML tag-balance check + `node --check` on extracted JS + push + curl 200 verify

## Continuing-session workflow

1. Edit files in the local path above
2. Verify: python HTMLParser tag balance; extract <script> to a temp file, `node --check` it
3. Commit with feat:/chore: prefix, push to master
4. Wait ~60s for Pages build, then curl -s -o /dev/null -w '%{http_code}' every changed URL
5. New pages → add to sitemap.xml (10 URLs currently)

## Next candidate improvements (not yet done)

- More awesome-list PRs: Awesome-LLM (27k★), Awesome-LLMs-as-Judges (618★), Awesome-LLM-Ops (6k★) — fork → edit README table in upstream format → PR, same pattern as #104
- Profile README (jdkabattles/jdkabattles) Featured Work table row for Algorithmic Gold — user DENIED the write once; requires explicit re-confirmation before touching
- Products page is the only commercial funnel (mimicplus $199 link) — watch for upgrade paths
- Live telemetry graph currently jitters around frozen values; true live updates would need a backend (GitHub Pages is static)
- No analytics; visitor/click counters are per-browser localStorage only
