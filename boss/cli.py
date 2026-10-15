from __future__ import annotations
import argparse
import json
import os
import sys
from .client import OpenAICompatibleClient
from .scorer import StyleScorer
from .loop import BossLoop

def main():
    p = argparse.ArgumentParser(prog="theboss")
    p.add_argument("--style-spec", required=True)
    p.add_argument("--threshold", type=float, default=0.85)
    p.add_argument("--iters", type=int, default=5)
    p.add_argument("prompt", nargs="*")
    args = p.parse_args()
    prompt = " ".join(args.prompt) or sys.stdin.read().strip()
    if not prompt:
        p.error("prompt required")
    style_spec = json.loads(open(args.style_spec).read())
    scorer = StyleScorer(style_spec)
    client = OpenAICompatibleClient()
    loop = BossLoop(client, scorer, threshold=args.threshold, max_iters=args.iters)
    instruction = style_spec.get("system_instruction", "Respond helpfully.")
    out = loop.run(prompt, instruction)
    print(json.dumps(out["best"], indent=2))
    return 0 if out["threshold_met"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
