"""algorithmic_gold.py

ALGORITHMIC GOLD = a procedure whose gains are verified by a signal it can't
game, and which still wins against a strong, fair baseline.

Domain-agnostic: plug in sample() + truth() and two procedures. Stdlib only.
Runs on Termux.
"""
import hashlib
import inspect
import os
import random
import time
from dataclasses import dataclass
from typing import Any, Callable, Optional, Sequence


@dataclass
class Domain:
    name: str
    # draw a fresh instance for a slice -> (public, hidden). Procedures see public only.
    sample: Callable[[random.Random, str], tuple]
    # SEALED signal: (public, hidden, output) -> float, higher is better.
    truth: Callable[[Any, Any, Any], float]
    slices: Sequence[str] = ("iid",)
    budget: int = 100  # identical for candidate and baseline
    # optional proxy the procedure may optimize (for the Goodhart check)
    proxy: Optional[Callable[[Any, Any, Any], float]] = None


def _fingerprint(f) -> str:
    try:
        src = inspect.getsource(f)
    except (OSError, TypeError):
        src = repr(f)
    return hashlib.sha256(src.encode()).hexdigest()


def _boot_lb(diffs, rng, alpha, B=2000):
    """Lower/upper confidence bounds of the mean paired difference (bootstrap)."""
    n = len(diffs)
    means = sorted(sum(rng.choice(diffs) for _ in range(n)) / n for _ in range(B))
    return means[int(alpha * B)], means[int((1 - alpha) * B) - 1]


def judge(cand, base, dom: Domain, n=300, alpha=0.05, min_effect=0.0,
          time_slack=3.0, goodhart_tol=0.25, entropy: bytes = None):
    report = {"domain": dom.name, "checks": {}}

    # 1. COMMIT: freeze both procedures BEFORE the sealed seed exists.
    commit = _fingerprint(cand) + _fingerprint(base)
    ent = entropy or os.urandom(32)
    seed = hashlib.sha256(commit.encode() + ent).hexdigest()
    report["commit"] = hashlib.sha256(commit.encode()).hexdigest()[:16]
    report["entropy"] = ent.hex()  # pass back in via entropy= to reproduce a run

    a = alpha / len(dom.slices)  # Bonferroni across slices
    all_slices_win, t_c, t_b = True, 0.0, 0.0
    proxy_gain, truth_gain = [], []
    spec_all = []

    for sl in dom.slices:
        rng = random.Random(seed + sl)  # fresh, unseen instances
        diffs, pdiffs, plac = [], [], []
        insts = [dom.sample(rng, sl) for _ in range(n)]
        for pub, hid in insts:  # 2. PARITY: same instance, same budget
            t0 = time.perf_counter()
            oc = cand(pub, dom.budget, random.Random(1))
            t_c += time.perf_counter() - t0
            t0 = time.perf_counter()
            ob = base(pub, dom.budget, random.Random(1))
            t_b += time.perf_counter() - t0
            diffs.append(dom.truth(pub, hid, oc) - dom.truth(pub, hid, ob))
            if dom.proxy:
                pdiffs.append(dom.proxy(pub, hid, oc) - dom.proxy(pub, hid, ob))
            # 3. PLACEBO: score against a mismatched hidden truth (prior-only gain)
            _, other = insts[len(diffs) % n]
            plac.append(dom.truth(pub, other, oc) - dom.truth(pub, other, ob))

        # 4. PAIRED, CORRECTED, EFFECT-SIZED win on this slice
        lb, _ = _boot_lb(diffs, rng, a)
        win = lb > min_effect
        spec_all += [d - p for d, p in zip(diffs, plac)]
        all_slices_win &= win
        mean = sum(diffs) / n
        truth_gain.append(mean)
        proxy_gain.append(sum(pdiffs) / n if pdiffs else mean)
        report["checks"][f"slice:{sl}"] = {
            "mean_gain": round(mean, 4),
            "lower_bound": round(lb, 4),
            "win": win,
        }

    # gain must beat placebo (pooled): it comes from the instance, not just the prior
    slb, _ = _boot_lb(spec_all, random.Random(seed), alpha)
    placebo_ok = slb > 0

    # 5. GOODHART: gain on the optimizable proxy must not outrun gain on truth
    tg = sum(truth_gain) / len(truth_gain)
    pg = sum(proxy_gain) / len(proxy_gain)
    goodhart_ok = (pg - tg) <= goodhart_tol * max(abs(tg), 1e-9) if dom.proxy else True

    # 6. COST: not "winning" by burning more compute than the baseline
    cost_ok = t_c <= time_slack * t_b + 0.001 * n * len(dom.slices)

    report["checks"].update({
        "placebo_clean": placebo_ok,
        "goodhart_ok": goodhart_ok,
        "cost_parity": cost_ok,
    })
    report["GOLD"] = bool(all_slices_win and placebo_ok and goodhart_ok and cost_ok)
    return report


# ---------------- demo: forecasting (swap in ANY domain) ----------------

def _sample(rng, sl):
    slope = rng.uniform(0.5, 1.5) if sl == "trend" else 0.0
    xs = [slope * t + rng.gauss(0, 1.0) for t in range(20)]
    return xs, slope * 20 + rng.gauss(0, 1.0)  # (history, next value)


def _truth(pub, hid, out):
    return -abs(out - hid)


def baseline_ewma(xs, budget, rng):  # smoother with fixed alpha=0.5 (NOT tuned)
    s = xs[0]
    for x in xs[1:]:
        s = 0.5 * s + 0.5 * x
    return s


def candidate_trend(xs, budget, rng):  # adaptive: trend when significant else mean
    n = len(xs)
    mx = (n - 1) / 2
    my = sum(xs) / n
    sx = sum((i - mx) ** 2 for i in range(n))
    b = sum((i - mx) * (x - my) for i, x in enumerate(xs)) / sx
    res = sum((x - (my + b * (i - mx))) ** 2 for i, x in enumerate(xs)) / (n - 2)
    se = (res / sx) ** 0.5
    t = abs(b) / se if se > 0 else 0.0
    if t < 3.0:
        return my
    return my + b * (n - mx)


if __name__ == "__main__":
    dom = Domain("forecast", _sample, _truth, slices=("trend", "flat"))
    r = judge(candidate_trend, baseline_ewma, dom)
    for k, v in r["checks"].items():
        print(k, v)
    print("GOLD:", r["GOLD"])
