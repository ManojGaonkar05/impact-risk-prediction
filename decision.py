"""
decision.py - PROTOTYPE rule-based decision skeleton (ACCEPT / MODIFY / REJECT).

WHAT THIS IS: the output format and the decision logic skeleton of the future decision engine.
WHAT THIS IS NOT: a prediction. There is no trained model and no evolution dataset yet, so the
impact and risk inputs must come from somewhere else. The demo feeds it HYPOTHETICAL examples.
The thresholds below are PLACEHOLDERS, to be calibrated from real data in Phase I.

Inputs use the same names as schema.OutcomeLabel:
  impact: quality_delta, cost_delta_pct, latency_delta_pct, reliability_delta
  risks : regression, failure, cascade, safety_drift  (True = predicted to happen)
A value of None means "not available" and is never treated as 0.
"""

from typing import Dict, List, Optional

from schema import Decision

# PLACEHOLDER thresholds (not calibrated)
MAX_COST_INCREASE_PCT = 20.0
MAX_LATENCY_INCREASE_PCT = 25.0
MIN_QUALITY_DELTA = 0.0
MIN_RELIABILITY_DELTA = -0.05

MITIGATIONS = {
    "cost": "cap tokens per step or use a cheaper model for the low-risk step",
    "latency": "reduce retries or steps, or run independent steps in parallel",
    "quality": "revisit the change; test it on more prompts before committing",
    "reliability": "add a retry/fallback path and collect more runs before committing",
    "evidence": "run more baseline and candidate runs to get the missing measurements",
}


def decide(impact: Dict[str, Optional[float]], risks: Dict[str, Optional[bool]]) -> Decision:
    q = impact.get("quality_delta")
    c = impact.get("cost_delta_pct")
    l = impact.get("latency_delta_pct")
    r = impact.get("reliability_delta")

    # 1) hard rejects: safety drift, cascade, predicted failure, or regression with lower quality
    hard: List[str] = []
    if risks.get("safety_drift"):
        hard.append("predicted safety-alignment drift")
    if risks.get("cascade"):
        hard.append("predicted cascade risk")
    if risks.get("failure"):
        hard.append("predicted failure risk")
    if risks.get("regression") and q is not None and q < 0:
        hard.append("predicted regression with lower quality")
    if hard:
        return Decision(
            "REJECT",
            "Rejected: " + "; ".join(hard) + ".",
            "do not apply as is; isolate the change and add a safety/regression probe, then re-evaluate",
        )

    # 2) missing evidence -> cannot accept safely
    missing = [n for n, v in [("quality", q), ("cost", c), ("latency", l), ("reliability", r)] if v is None]
    if missing:
        return Decision(
            "MODIFY",
            "Not enough evidence: no estimate for " + ", ".join(missing) + ".",
            MITIGATIONS["evidence"],
        )

    # 3) threshold checks
    issues, fixes = [], []
    if c > MAX_COST_INCREASE_PCT:
        issues.append(f"cost +{c:g}% (limit {MAX_COST_INCREASE_PCT:g}%)")
        fixes.append(MITIGATIONS["cost"])
    if l > MAX_LATENCY_INCREASE_PCT:
        issues.append(f"latency +{l:g}% (limit {MAX_LATENCY_INCREASE_PCT:g}%)")
        fixes.append(MITIGATIONS["latency"])
    if q < MIN_QUALITY_DELTA:
        issues.append(f"quality {q:+g}")
        fixes.append(MITIGATIONS["quality"])
    if r < MIN_RELIABILITY_DELTA:
        issues.append(f"reliability {r:+g}")
        fixes.append(MITIGATIONS["reliability"])
    if issues:
        return Decision("MODIFY", "Modify: " + "; ".join(issues) + ".", "; ".join(fixes))

    return Decision(
        "ACCEPT",
        f"All estimates within the placeholder limits (quality {q:+g}, cost {c:+g}%, "
        f"latency {l:+g}%, reliability {r:+g}).",
        None,
    )
