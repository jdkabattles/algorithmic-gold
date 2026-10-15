from __future__ import annotations

from .client import OpenAICompatibleClient
from .scorer import StyleScorer


class BossLoop:
    def __init__(self, client: OpenAICompatibleClient, scorer: StyleScorer, threshold: float = 0.85, max_iters: int = 5):
        if not 0 <= threshold <= 1:
            raise ValueError("threshold must be between 0 and 1")
        if max_iters <= 0:
            raise ValueError("max_iters must be positive")
        self.client = client
        self.scorer = scorer
        self.threshold = threshold
        self.max_iters = max_iters

    def run(self, user_input: str, style_instruction: str) -> dict:
        if not isinstance(user_input, str) or not user_input.strip():
            raise ValueError("user_input must be a non-empty string")
        if not isinstance(style_instruction, str) or not style_instruction.strip():
            raise ValueError("style_instruction must be a non-empty string")

        best = None
        history = []
        feedback = "Revise to be concise, precise, high quality. Return only revised answer."
        for i in range(self.max_iters):
            candidates = []
            base_msgs = [
                {"role": "system", "content": style_instruction},
                {"role": "user", "content": user_input},
            ]
            r0 = self.client.chat(base_msgs)
            candidates.append(r0.text)
            if best is not None:
                rev_msgs = [
                    {"role": "system", "content": style_instruction},
                    {"role": "user", "content": user_input},
                    {"role": "assistant", "content": best["text"]},
                    {"role": "user", "content": feedback},
                ]
                r1 = self.client.chat(rev_msgs)
                candidates.append(r1.text)
            for cand in candidates:
                score = self.scorer.score(cand)
                toks = cand.lower().split()
                rep = 0.0 if not toks else (len(toks) - len(set(toks))) / len(toks)
                composite = score.total - 0.25 * rep
                entry = {
                    "iter": i + 1,
                    "text": cand,
                    "score": score.total,
                    "composite": composite,
                    "details": score.details,
                    "usage": {},
                }
                history.append(entry)
                if best is None or composite > best.get("composite", -1.0):
                    best = entry
            missing = [m for m in self.scorer.required_markers if m.lower() not in (best["text"].lower())]
            if missing:
                feedback = "Revise to include naturally: " + ", ".join(missing) + ". Return only revised answer."
            else:
                feedback = "Revise to be concise, precise, high quality. Return only revised answer."
            if best["score"] >= self.threshold:
                break
        return {"best": best, "history": history, "threshold_met": best["score"] >= self.threshold}
