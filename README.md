# Pre-Commitment Impact & Risk Prediction for Self-Evolving Multi-Agent Workflows

Capstone project (PW_25_VSH_01). A pre-commitment layer that predicts the impact
and risk of an evolution change in a self-evolving agent system and outputs
ACCEPT / MODIFY / REJECT. EvoAgentX is the first system under test.

## Setup
1. Clone and install EvoAgentX (https://github.com/EvoAgentX/EvoAgentX) in a venv:
   pip install -r requirements.txt, then pip install -e .
2. Pin these versions (newer ones break EvoAgentX imports):
   pip install "mcp==1.30.0" "fastmcp==2.14.7"
3. Create a .env file with GEMINI_API_KEY=your_key (never commit this file).

## Files
- sequential_workflow_gemini.py - 2-agent (Planning, Coding) EvoAgentX workflow on Gemini
- run_logger.py - runs the workflow N times and logs latency, status, retries, errors
- data/run_log_sample.jsonl - sample telemetry from real runs

## Run
python run_logger.py 2

See PROGRESS.md for status.
