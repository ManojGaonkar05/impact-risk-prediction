"""
schema.py - Common representation for the Pre-Commitment Impact & Risk Prediction project.

Everything after the adapter (feature extraction, prediction, decision engine) should use
ONLY these classes, never framework-specific data. EvoAgentX is the first adapter.

STATUS (be honest in the review):
  - TelemetryRecord + EvoAgentXAdapter + load_jsonl : WORKING, tested on real run_log.jsonl rows.
  - EvolutionChange / OutcomeLabel / EvolutionExample: DEFINED (schema only). No labeled
    evolution data has been collected yet; that is Phase I work after Review 2.

Usage (from the project folder):
    python schema.py                        # reads data/run_log_sample.jsonl
    python schema.py debug/run_log.jsonl    # or any other file
"""

from __future__ import annotations

import json
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional

# ---- constants -------------------------------------------------------------------------

CHANGE_TYPES = ("model", "memory", "tools", "workflow")   # the 4 evolution pathways
STATUSES = ("success", "failure")                          # what run_logger.py writes
DECISIONS = ("ACCEPT", "MODIFY", "REJECT")


# ---- 1. telemetry record (one workflow run) --------------------------------------------

@dataclass
class TelemetryRecord:
    """One run of an agent workflow, in framework-independent form."""
    run_id: int
    timestamp: str
    model: str
    workflow: str
    duration_seconds: float
    status: str
    retries: int = 0
    error: Optional[str] = None
    output_chars: int = 0
    # Not yet saved by run_logger.py -> None means "not measured" (never 0).
    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None
    total_tokens: Optional[int] = None
    cost_usd: Optional[float] = None
    source_system: str = "EvoAgentX"

    def validate(self) -> List[str]:
        """Return a list of problems (empty list = record is valid)."""
        problems = []
        if self.status not in STATUSES:
            problems.append(f"status must be one of {STATUSES}, got {self.status!r}")
        if self.duration_seconds < 0:
            problems.append("duration_seconds is negative")
        if self.retries < 0:
            problems.append("retries is negative")
        return problems

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "TelemetryRecord":
        """Build from a dict; ignores unknown keys, so old and new log lines both load."""
        known = {k: d[k] for k in cls.__dataclass_fields__ if k in d}
        return cls(**known)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# ---- 2. evolution change (what a self-evolving system proposes) ------------------------

@dataclass
class EvolutionChange:
    """A proposed change to Model, Memory, Tools or Workflow."""
    type: str                      # one of CHANGE_TYPES
    description: str
    before: Any                    # e.g. "gemini/model-A", or a workflow-graph dict
    after: Any

    def validate(self) -> List[str]:
        problems = []
        if self.type not in CHANGE_TYPES:
            problems.append(f"type must be one of {CHANGE_TYPES}, got {self.type!r}")
        if not self.description:
            problems.append("description is empty")
        return problems


# ---- 3. outcome labels (what ACTUALLY happened after the change) -----------------------

@dataclass
class OutcomeLabel:
    """Measured result of applying a change. None = not measured yet."""
    # Impact (signed change vs baseline)
    quality_delta: Optional[float] = None
    cost_delta_pct: Optional[float] = None
    latency_delta_pct: Optional[float] = None
    reliability_delta: Optional[float] = None
    # Risk (did it happen?)
    regression: Optional[bool] = None
    failure: Optional[bool] = None
    cascade: Optional[bool] = None
    safety_drift: Optional[bool] = None


# ---- 4. one training example for the future predictor ----------------------------------

@dataclass
class EvolutionExample:
    """change + baseline run(s) + candidate run(s) + measured outcome."""
    change: EvolutionChange
    baseline_runs: List[TelemetryRecord] = field(default_factory=list)
    candidate_runs: List[TelemetryRecord] = field(default_factory=list)
    outcome: Optional[OutcomeLabel] = None


# ---- 5. decision output (future decision engine) ---------------------------------------

@dataclass
class Decision:
    decision: str                  # ACCEPT / MODIFY / REJECT
    reason: str
    mitigation: Optional[str] = None


# ---- 6. Common Adapter Interface -------------------------------------------------------

class CommonAdapter(ABC):
    """Every agent framework plugs in by implementing this. The core never sees raw data."""

    @abstractmethod
    def to_telemetry(self, raw: Dict[str, Any]) -> TelemetryRecord:
        ...


class EvoAgentXAdapter(CommonAdapter):
    """Converts a line of run_logger.py output (EvoAgentX run) into a TelemetryRecord."""

    def to_telemetry(self, raw: Dict[str, Any]) -> TelemetryRecord:
        rec = TelemetryRecord.from_dict(raw)
        rec.source_system = "EvoAgentX"
        return rec


# ---- helpers ---------------------------------------------------------------------------

def load_jsonl(path: str, adapter: Optional[CommonAdapter] = None) -> List[TelemetryRecord]:
    """Read a .jsonl log into TelemetryRecords. Skips blank lines."""
    adapter = adapter or EvoAgentXAdapter()
    records = []
    with open(path, "r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                records.append(adapter.to_telemetry(json.loads(line)))
            except (json.JSONDecodeError, TypeError) as e:
                print(f"  line {line_no}: skipped ({type(e).__name__}: {e})")
    return records


def main() -> None:
    path = sys.argv[1] if len(sys.argv) > 1 else "data/run_log_sample.jsonl"
    print(f"Loading {path} ...")
    records = load_jsonl(path)
    print(f"Loaded {len(records)} telemetry record(s)\n")
    for r in records:
        issues = r.validate()
        print(f"run {r.run_id} | {r.status} | {r.duration_seconds}s | retries={r.retries} "
              f"| tokens={r.total_tokens} | cost={r.cost_usd} | valid={not issues}")
        for p in issues:
            print("   PROBLEM:", p)

    # Shows the schema shape only. The values below are ILLUSTRATIVE, not measured data.
    example = EvolutionChange(
        type="model",
        description="[ILLUSTRATIVE EXAMPLE - not a real run] switch Coding agent to a larger model",
        before="gemini/gemini-3.8-flash",
        after="<candidate model>",
    )
    print("\nExample EvolutionChange (illustrative only):")
    print(json.dumps(asdict(example), indent=2))
    print("valid =", not example.validate())


if __name__ == "__main__":
    main()