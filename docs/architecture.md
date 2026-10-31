# Architecture (draft for Review 2)

```
 Agent system (EvoAgentX)           [Done]       2-agent workflow runs end to end
        | raw telemetry + evolution info
        v
 Observability / run logger         [Done]       run_logger.py -> JSONL (tokens + est. cost)
        v
 Common Adapter Interface           [Done]       CommonAdapter, EvoAgentXAdapter (schema.py)
        v
 Common representation              [Done]       TelemetryRecord
                                    [Defined]    EvolutionChange, OutcomeLabel, Decision
        v
 Evolution dataset                  [Planned]    baseline vs candidate runs, labeled outcomes
        v
 Feature extraction                 [Prototype]  features.py
        v
 ML prediction                      [Planned]    Impact: Quality, Cost, Latency, Reliability
                                                 Risk:   Regression, Failure, Cascade, Safety drift
        v
 Decision engine                    [Prototype]  decision.py: rule-based skeleton, placeholder thresholds;
                                                 final version needs the prediction models
        v
 Dashboard -> Controlled validation -> Feedback   [Planned]  predicted vs actual
```

Everything below the adapter uses only the common representation, so the prediction and decision
core stays framework-independent. A new agent framework needs one new adapter class.
