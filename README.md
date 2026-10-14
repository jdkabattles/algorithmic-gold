# Algorithmic Gold

**Done is a claim. GOLD is a receipt.**

The verification standard for AI work. A procedure only earns **GOLD** when its
gains are proven by a signal it can't game — and it still beats a strong, fair
baseline. No mocked runs. Real outcomes only.

Live: https://jdkabattles.github.io/algorithmic-gold/

## The six gates

| # | Gate | What it kills |
|---|------|---------------|
| 01 | **Commit** | Post-hoc tuning — both procedures are fingerprinted *before* the sealed seed exists |
| 02 | **Parity** | Resource cheating — identical instances, identical budgets for candidate and baseline |
| 03 | **Placebo** | Gain that's just the prior — scored against mismatched hidden truths |
| 04 | **Paired win** | Luck — bootstrap lower confidence bound + Bonferroni across slices must clear zero |
| 05 | **Goodhart** | Gaming the scoreboard — proxy gain must not outrun truth gain |
| 06 | **Cost** | Victory by brute force — runtime held against a slack multiple of the baseline |

## The seed protocol

A single `GOLD True` never counts. The gate requires:

- **GOLD True on at least 5 independent fresh seeds**, then
- **one final run on a frozen holdout** the procedure has never touched.

The loop — spec → plan → test → build → verify → review → commit — stops only
when that gate passes.

## The pattern

Every gate is a named, published pattern:

- [Goodhart's Law](https://en.wikipedia.org/wiki/Goodhart's_law) → Gate 05
- [Specification gaming](https://deepmind.google/discover/blog/specification-gaming-the-flip-side-of-ai-ingenuity/) (DeepMind) → Gates 03 + 05
- [Test-set contamination](https://arxiv.org/abs/2310.17623) → seeds + holdout
- [Bootstrap confidence bounds](https://en.wikipedia.org/wiki/Bootstrapping_(statistics)) → Gate 04
- [Bonferroni correction](https://en.wikipedia.org/wiki/Bonferroni_correction) → Gate 04
- [Multiple comparisons problem](https://en.wikipedia.org/wiki/Multiple_comparisons_problem) → Gate 04
- [Data dredging / p-hacking](https://en.wikipedia.org/wiki/Data_dredging) → Gate 01
- [Statistical power](https://en.wikipedia.org/wiki/Statistical_power) → all gates
- [Overfitting](https://en.wikipedia.org/wiki/Overfitting) → seeds + holdout

## Prior art

The ecosystem this standard stands on (verified, linked from the site):

- [lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness) (14.2k★)
- [openai/evals](https://github.com/openai/evals) (19.6k★)
- [inspect_ai](https://github.com/UKGovernmentBEIS/inspect_ai) (3.0k★)
- [HELM](https://github.com/stanford-crfm/helm) (2.9k★)
- [SWE-bench](https://github.com/SWE-bench/SWE-bench) (6.0k★)
- [arena-hard-auto](https://github.com/lmarena/arena-hard-auto) (1.1k★)
- [alpaca_eval](https://github.com/tatsu-lab/alpaca_eval) (2.0k★)
- [Prometheus](https://github.com/prometheus-eval/prometheus-eval) (1.1k★)
- [LLMBar](https://github.com/princeton-nlp/LLMBar) — the adversary cite
- [Awesome-LLM-Eval](https://github.com/onejune2018/Awesome-LLM-Eval)

## Repo layout

```
index.html    the landing page (self-contained, zero dependencies)
404.html      custom 404 in the same voice
og-image.png  1200×630 social preview card
robots.txt    crawl rules + sitemap pointer
sitemap.xml   sitemap for search engines
gen_og.py     regenerates og-image.png (stdlib only)
```

## License

Apache License 2.0 — see [LICENSE](LICENSE).
