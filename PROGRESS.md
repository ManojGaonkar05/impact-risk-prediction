# Progress Tracker (updated: 31 Oct 2026)

Project: Pre-Commitment Impact & Risk Prediction for Self-Evolving Multi-Agent Workflows (PW_25_VSH_01)
Next milestone: Capstone Review 2 on 3 Nov 2026

| #  | Task                                          | Status | Notes                                                        |
|----|-----------------------------------------------|--------|--------------------------------------------------------------|
| 1  | Install EvoAgentX                             | Done   | venv, version 0.1.4                                          |
| 2  | Connect free LLM (Gemini via LiteLLM)         | Done   | model gemini/gemini-3.8-flash                                |
| 3  | Run example multi-agent workflow              | Done   | Planning + Coding agents (FileToolkit removed)               |
| 4  | Telemetry logger (latency, status, retries)   | Done   | run_logger.py; tokens and cost are NOT logged yet            |
| 5  | Common adapter schema                         | Done   | schema.py: telemetry record, adapter interface, evolution change, outcome labels. Change/outcome classes are defined only; no labeled data yet |
| 6  | Save token and cost in telemetry log          | Next   | find where EvoAgentX exposes cost, then update run_logger.py |
| 7  | Requirements and architecture diagram         | To do  | Review 2 slides                                              |
| 8  | Literature survey                             | To do  | 2-4 papers, categorized; verify authors/venue/year from the papers |
| 9  | Review 2 PPT                                  | To do  | due 3 Nov 2026                                               |
| 10 | Evolution dataset (change -> effect)          | Later  | Phase I                                                      |
| 11 | Prediction models, decision engine, dashboard | Later  | Phase I/II                                                   |

## Observed so far

Real runs of the Planning + Coding workflow (data/run_log_sample.jsonl):

| Run | Status  | Duration | Retries | Notes                                  |
|-----|---------|----------|---------|----------------------------------------|
| 1   | failure | 639.0 s  | 3       | retry limit reached; error text: (add from log) |
| 2   | success | 584.9 s  | 2       | Gemini 503 high-demand errors, then OK |

- Only 2 runs so far, so no statistics yet.
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
- Survey papers not yet chosen or verified