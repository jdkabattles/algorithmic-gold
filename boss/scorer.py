from __future__ import annotations

import json
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path


@dataclass(frozen=True)
class Score:
    total: float
    details: dict[str, int | bool | float]


class StyleScorer:
    def __init__(self, spec: dict[str, object]):
        if not isinstance(spec, dict):
            raise ValueError("spec must be a dictionary")
        self.spec = spec
        self.required_markers = _string_list(spec.get("required_markers", []))
        self.forbidden_markers = _string_list(spec.get("forbidden_markers", []))
        self.min_chars = _positive_int(spec.get("min_chars", 40), "min_chars")
        self.max_chars = _positive_int(spec.get("max_chars", 4000), "max_chars")
        if self.min_chars > self.max_chars:
            raise ValueError("min_chars cannot exceed max_chars")

    @classmethod
    def from_file(cls, path: str | Path) -> "StyleScorer":
        with Path(path).open(encoding="utf-8") as source:
            return cls(json.load(source))

    def score(self, text: str) -> Score:
        normalized = text.lower()
        required_hits = sum(1 for marker in self.required_markers if marker.lower() in normalized)
        forbidden_hits = sum(1 for marker in self.forbidden_markers if marker.lower() in normalized)
        length_ok = self.min_chars <= len(text) <= self.max_chars

        components: list[Fraction] = []
        if self.required_markers:
            components.append(Fraction(required_hits, len(self.required_markers)))
        if self.forbidden_markers:
            components.append(Fraction(len(self.forbidden_markers) - forbidden_hits, len(self.forbidden_markers)))
        components.append(Fraction(1 if length_ok else 0, 1))
        toks = text.lower().split()
        repetition_ratio = 0.0 if not toks else (len(toks) - len(set(toks))) / len(toks)
        components.append(Fraction(1, 1) - Fraction(repetition_ratio).limit_denominator(10000))

        total = float(sum(components, Fraction(0)) / len(components)) if components else 0.0
        details = {
            "required_hits": required_hits,
            "required_total": len(self.required_markers),
            "forbidden_hits": forbidden_hits,
            "forbidden_total": len(self.forbidden_markers),
            "length_ok": length_ok,
        }
        return Score(total=total, details=details)


def _string_list(value: object) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ValueError("markers must be lists of strings")
    return value


def _positive_int(value: object, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{name} must be a non-negative integer")
    return value
