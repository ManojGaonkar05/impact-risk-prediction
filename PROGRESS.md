# Progress Tracker (updated: 31 Oct 2026)

Project: Pre-Commitment Impact & Risk Prediction for Self-Evolving Multi-Agent Workflows (PW_25_VSH_01)
Next milestone: Capstone Review 2 on 3 Nov 2026

| #  | Task                                          | Status    | Notes                                                        |
|----|-----------------------------------------------|-----------|--------------------------------------------------------------|
| 1  | Install EvoAgentX                             | Done      | venv, version 0.1.4                                          |
| 2  | Connect free LLM (Gemini via LiteLLM)         | Done      | model gemini/gemini-3.8-flash                                |
| 3  | Run example multi-agent workflow              | Done      | Planning + Coding agents (FileToolkit removed)               |
| 4  | Telemetry logger (latency, status, retries)   | Done      | run_logger.py; also logs tokens and estimated cost (from run 3) |
| 5  | Common adapter schema                         | Done      | schema.py: telemetry record, adapter interface, evolution change, outcome labels. Change/outcome classes are defined only; no labeled data yet |
| 6  | Save token and cost in telemetry log          | Done      | difference of EvoAgentX cost_manager totals before/after a run; whole run including retries; cost is an estimate |
| 7  | Feature extraction + demo script              | Prototype | features.py and demo.py; descriptive features only, no prediction |
| 8  | README and docs (architecture, requirements)  | Done      | README.md, docs/architecture.md, docs/requirements.md (drafts) |
| 9  | Literature survey                             | To do     | 4 papers shortlisted; verify authors/venue/year from the papers |
| 10 | Review 2 PPT                                  | To do     | due 3 Nov 2026                                               |
| 11 | Evolution dataset (change -> effect)          | Later     | Phase I                                                      |
| 12 | Prediction models, decision engine, dashboard | Later     | Phase I/II                                                   |

## Observed so far

Real runs of the Planning + Coding workflow (data/run_log_sample.jsonl):

| Run | Status  | Duration | Retries | Tokens / est. cost                     | Notes                                  |
|-----|---------|----------|---------|----------------------------------------|----------------------------------------|
| 1   | failure | 639.0 s  | 3       | not logged                             | retry limit reached; generic API error ("An unexpected error occurred... contact support"), output_chars 0 |
| 2   | success | 584.9 s  | 2       | not logged                             | Gemini 503 high-demand errors, then OK |
| 3   | success | 302.3 s  | 1       | 2127 tokens (885 in, 1242 out), est. $0.005321 | first run with token/cost logging |

- Only 3 runs so far, so no statistics and no trends yet.
- Duration includes the 20 s waits between retries.
- Token and cost logging was added after runs 1 and 2, so only run 3 has those fields.
- Package pitfall: mcp 2.x and fastmcp 4.x break EvoAgentX; pinned mcp 1.30.0, fastmcp 2.14.7.
- Never run pip install --upgrade. Always check that (venv) shows in the terminal first.

## Housekeeping

- [ ] Create a new Gemini key in Google AI Studio, update .env, delete "api key.txt" (old key appeared in screenshots)
- [ ] Make the GitHub repo private (currently public)
- [ ] Check .gitignore contains only ignore patterns (no PowerShell wrapper lines)
- [ ] Collect the panel's Review 1 remarks
- [ ] Show the draft to the guide before 3 Nov

## Blockers

- Panel's Review 1 remarks not yet collected
- Survey papers not yet verified
