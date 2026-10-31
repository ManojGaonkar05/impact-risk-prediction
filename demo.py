"""
demo.py - end-to-end demo of what is implemented so far.

    python demo.py                       # uses data/run_log_sample.jsonl
    python demo.py debug/run_log.jsonl   # or your own log

Stages shown:  log file -> Common Adapter -> common records -> validation
               -> prototype features -> summary -> (illustrative) evolution change
               -> (hypothetical) ACCEPT / MODIFY / REJECT output format
Everything is read-only except data/run_features.csv, which is regenerated.
"""

import csv
import json
import sys
from dataclasses import asdict

from schema import EvolutionChange, load_jsonl
from features import run_features, summarize
from decision import decide


def title(text):
    print("\n" + "=" * 70)
    print(text)
    print("=" * 70)


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "data/run_log_sample.jsonl"

    title("1. Common Adapter Interface: raw EvoAgentX log -> common records")
    records = load_jsonl(path)
    print(f"source file : {path}")
    print(f"records     : {len(records)}")

    title("2. Validation of each common record")
    for r in records:
        problems = r.validate()
        print(f"run {r.run_id}: {r.status:7s} {r.duration_seconds:7.1f}s "
              f"retries={r.retries} -> {'valid' if not problems else problems}")

    title("3. Feature extraction PROTOTYPE (common representation only)")
    rows = [run_features(r) for r in records]
    cols = list(rows[0].keys()) if rows else []
    print(" | ".join(cols))
    for row in rows:
        print(" | ".join("None" if row[c] is None else str(row[c]) for c in cols))
    with open("data/run_features.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    print("\nsaved: data/run_features.csv   (None = not measured, never 0)")

    title("4. Summary of real runs (descriptive only, NOT predictions)")
    for k, v in summarize(records).items():
        print(f"{k:34s}: {v}")
    print("\nNote: duration includes retry waiting time (20 s between retries).")
    print("Note: token/cost logging started at run 3, so older runs have None.")
    print(f"Note: only {len(records)} runs, so no statistical conclusions.")

    title("5. Evolution change schema (ILLUSTRATIVE EXAMPLE, not measured data)")
    ex = EvolutionChange(
        type="model",
        description="[ILLUSTRATIVE] switch Coding agent to a larger model",
        before="gemini/gemini-3.8-flash",
        after="<candidate model>",
    )
    print(json.dumps(asdict(ex), indent=2))

    title("6. Decision output PROTOTYPE (rule-based skeleton, HYPOTHETICAL inputs)")
    print("These inputs are made up to show the output format. They are NOT predicted")
    print("from data: no prediction model or evolution dataset exists yet.")
    print("Thresholds are placeholders (cost <= +20%, latency <= +25%).\n")
    no_risk = {"regression": False, "failure": False, "cascade": False, "safety_drift": False}
    cases = [
        ("Case A", "small safe change",
         {"quality_delta": 0.02, "cost_delta_pct": 5, "latency_delta_pct": 8, "reliability_delta": 0.0}, no_risk),
        ("Case B", "quality +8% but cost +22%",
         {"quality_delta": 0.08, "cost_delta_pct": 22, "latency_delta_pct": 10, "reliability_delta": 0.0}, no_risk),
        ("Case C", "quality +8%, cost +22%, weaker safety",
         {"quality_delta": 0.08, "cost_delta_pct": 22, "latency_delta_pct": 10, "reliability_delta": 0.0},
         dict(no_risk, safety_drift=True)),
    ]
    for name, label, impact, risks in cases:
        d = decide(impact, risks)
        print(f"{name} ({label}) [HYPOTHETICAL]")
        print(f"  decision  : {d.decision}")
        print(f"  reason    : {d.reason}")
        print(f"  mitigation: {d.mitigation}\n")

    title("7. Pipeline status")
    status = [
        ("Run logger + telemetry (tokens, est. cost)", "DONE"),
        ("Common Adapter Interface + schema", "DONE"),
        ("Feature extraction", "PROTOTYPE"),
        ("Evolution dataset (change -> effect)", "PLANNED"),
        ("Impact / risk prediction models", "PLANNED"),
        ("Decision engine ACCEPT / MODIFY / REJECT (rule-based skeleton, no model)", "PROTOTYPE"),
        ("Dashboard, controlled validation, feedback", "PLANNED"),
    ]
    for name, st in status:
        print(f"[{st:9s}] {name}")


if __name__ == "__main__":
    main()
