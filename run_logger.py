import json
import os
import sys
import time
from datetime import datetime

from dotenv import load_dotenv

from evoagentx.workflow import SequentialWorkFlowGraph, WorkFlow
from evoagentx.agents import AgentManager
from evoagentx.models import LiteLLMConfig, LiteLLM
from evoagentx.models.model_utils import cost_manager


load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini/gemini-3.8-flash"
LOG_FILE = "debug/run_log.jsonl"
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 20

PROBLEM = "Write a Python function to find the longest palindromic substring in a given string."


def build_workflow():
    llm_config = LiteLLMConfig(
        model=MODEL_NAME,
        gemini_key=GEMINI_API_KEY,
        stream=False,
        output_response=False,
    )
    llm = LiteLLM(config=llm_config)

    tasks = [
        {
            "name": "Planning",
            "description": "Create a detailed plan for code generation",
            "inputs": [{"name": "problem", "type": "str", "required": True, "description": "Problem to solve"}],
            "outputs": [{"name": "plan", "type": "str", "required": True, "description": "Implementation plan"}],
            "prompt": "You are a software architect. Create a short implementation plan for the given problem.\n\nProblem: {problem}\n\nProvide: 1. Approach 2. Implementation steps 3. Edge cases",
            "parse_mode": "str",
        },
        {
            "name": "Coding",
            "description": "Implement the code based on the implementation plan",
            "inputs": [
                {"name": "problem", "type": "str", "required": True, "description": "Problem to solve"},
                {"name": "plan", "type": "str", "required": True, "description": "Plan from the Planning phase"},
            ],
            "outputs": [{"name": "code", "type": "str", "required": True, "description": "Implemented code"}],
            "prompt": "You are a software developer. Implement the code based on the problem and plan.\n\nProblem: {problem}\nImplementation Plan: {plan}\n\nProvide the implementation code with comments.",
            "parse_mode": "str",
        },
    ]

    graph = SequentialWorkFlowGraph(goal="Generate code to solve programming problems", tasks=tasks)
    agent_manager = AgentManager()
    agent_manager.add_agents_from_workflow(graph, llm_config=llm_config)
    return WorkFlow(graph=graph, agent_manager=agent_manager, llm=llm)


def run_once(run_id):
    """Run the workflow once (with retries) and return a telemetry record."""
    start = time.time()
    in_before = sum(cost_manager.input_tokens.values())
    out_before = sum(cost_manager.output_tokens.values())
    cost_before = cost_manager.get_total_cost()
    retries = 0
    status = "failure"
    error = None
    output_chars = 0

    for attempt in range(MAX_RETRIES + 1):
        try:
            workflow = build_workflow()
            result = workflow.execute(inputs={"problem": PROBLEM})
            if result.status == "success":
                status = "success"
                error = None
                output_chars = len(str(result.result))
                break
            error = str(result.displayable_error)[:300]
        except Exception as e:
            error = f"{type(e).__name__}: {str(e)[:300]}"

        if attempt < MAX_RETRIES:
            retries += 1
            print(f"  run {run_id}: failed ({error}). Retry {retries}/{MAX_RETRIES} in {RETRY_DELAY_SECONDS}s...")
            time.sleep(RETRY_DELAY_SECONDS)

    return {
        "run_id": run_id,
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "model": MODEL_NAME,
        "workflow": "sequential_planning_coding",
        "duration_seconds": round(time.time() - start, 1),
        "status": status,
        "retries": retries,
        "error": error,
        "output_chars": output_chars,
        "prompt_tokens": sum(cost_manager.input_tokens.values()) - in_before,
        "completion_tokens": sum(cost_manager.output_tokens.values()) - out_before,
        "total_tokens": cost_manager.total_llm_tokens - (in_before + out_before),
        "cost_usd": round(cost_manager.get_total_cost() - cost_before, 6),
    }


def main():
    n_runs = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    os.makedirs("debug", exist_ok=True)

    for i in range(1, n_runs + 1):
        print(f"Starting run {i}/{n_runs}...")
        record = run_once(i)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
        print("  logged:", record)

    print(f"\nDone. Telemetry saved to {LOG_FILE}")


if __name__ == "__main__":
    main()