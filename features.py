"""
features.py - PROTOTYPE feature extraction on the COMMON representation only.

Works on schema.TelemetryRecord, never on raw EvoAgentX data, so it stays
framework-independent. This is an early prototype: it turns runs into simple
numeric features. It does NOT predict anything yet (prediction models are planned).

Rule: a value that was not measured stays None. It is never replaced by 0.
"""

from typing import Dict, List, Optional
from schema import TelemetryRecord


def run_features(r: TelemetryRecord) -> Dict[str, Optional[float]]:
    """One feature row per run."""
    tokens_per_s = None
    if r.total_tokens is not None and r.duration_seconds > 0:
        tokens_per_s = round(r.total_tokens / r.duration_seconds, 3)
    return {
        "run_id": r.run_id,
        "success": 1 if r.status == "success" else 0,
        "duration_s": r.duration_seconds,
        "retries": r.retries,
        "output_chars": r.output_chars,
        "total_tokens": r.total_tokens,
        "cost_usd": r.cost_usd,
        "tokens_per_s": tokens_per_s,
    }


def _mean(values: List[float], digits: int = 3) -> Optional[float]:
    return round(sum(values) / len(values), digits) if values else None


def summarize(records: List[TelemetryRecord]) -> Dict[str, Optional[float]]:
    """Descriptive statistics over runs (not predictions)."""
    n = len(records)
    ok = [r for r in records if r.status == "success"]
    with_tokens = [r for r in records if r.total_tokens is not None]
    with_cost = [r for r in records if r.cost_usd is not None]
    return {
        "runs": n,
        "successes": len(ok),
        "failures": n - len(ok),
        "success_rate": round(len(ok) / n, 3) if n else None,
        "mean_duration_s": _mean([r.duration_seconds for r in records]),
        "mean_retries": _mean([r.retries for r in records]),
        "runs_with_token_data": len(with_tokens),
        "mean_tokens (runs with data)": _mean([r.total_tokens for r in with_tokens]),
        "mean_cost_usd (runs with data)": _mean([r.cost_usd for r in with_cost], 6),
    }
