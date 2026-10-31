# Requirements (draft for Review 2)

## Functional (inputs -> processing -> outputs)

| # | Requirement | Status |
|---|---|---|
| FR1 | Telemetry capture: run a workflow with retries and record duration, status, retries, error, output size, tokens, estimated cost as one JSONL record per run | Done |
| FR2 | Common adapter: convert framework-specific telemetry into the common TelemetryRecord | Done (EvoAgentX) |
| FR3 | Evolution change representation {type: model/memory/tools/workflow, description, before, after} | Defined, no data yet |
| FR4 | Evolution dataset: run baseline and candidate versions and label actual outcomes | Planned |
| FR5 | Feature extraction from common records and changes | Prototype |
| FR6 | Predict impact (Quality, Cost, Latency, Reliability) and risk (Regression, Failure, Cascade, Safety drift) | Planned |
| FR7 | Decision engine: ACCEPT / MODIFY / REJECT with reason and mitigation | Planned |
| FR8 | Dashboard for candidate analysis, predictions and risk | Planned |
| FR9 | Controlled validation and feedback (predicted vs actual) | Planned |

## Non-functional

- Framework independence: a new framework needs one adapter, no change to the core.
- Reproducibility: pinned package versions; each record stores model and workflow.
- Data integrity: failed runs are kept; "not measured" is stored as None, never 0.
- Explainability: every decision carries a reason that points to evidence.
- Low cost: free Gemini key and local Python for the first setup.
- Security: API keys only in .env, which is git-ignored.
- Extensibility: models and algorithms behind the prediction core can change.
- Accuracy and performance targets: to be defined after dataset collection (no data yet).
