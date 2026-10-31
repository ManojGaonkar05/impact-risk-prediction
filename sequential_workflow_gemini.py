import os
from dotenv import load_dotenv

from evoagentx.workflow import SequentialWorkFlowGraph, WorkFlow
from evoagentx.agents import AgentManager
from evoagentx.models import LiteLLMConfig, LiteLLM

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def build_sequential_workflow():

    # configure the LLM (Gemini through LiteLLM)
    llm_config = LiteLLMConfig(
        model="gemini/gemini-3.8-flash",
        gemini_key=GEMINI_API_KEY,
        stream=False,
        output_response=True,
    )
    llm = LiteLLM(config=llm_config)

    # Two sequential tasks: Planning, then Coding
    tasks = [
        {
            "name": "Planning",
            "description": "Create a detailed plan for code generation",
            "inputs": [
                {"name": "problem", "type": "str", "required": True, "description": "Description of the problem to be solved"},
            ],
            "outputs": [
                {"name": "plan", "type": "str", "required": True, "description": "Detailed plan with steps, components, and architecture"}
            ],
            "prompt": "You are a software architect. Create a short implementation plan for the given problem.\n\nProblem: {problem}\n\nProvide: 1. Approach 2. Implementation steps 3. Edge cases",
            "parse_mode": "str",
        },
        {
            "name": "Coding",
            "description": "Implement the code based on the implementation plan",
            "inputs": [
                {"name": "problem", "type": "str", "required": True, "description": "Description of the problem to be solved"},
                {"name": "plan", "type": "str", "required": True, "description": "Implementation plan from the Planning phase"},
            ],
            "outputs": [
                {"name": "code", "type": "str", "required": True, "description": "Implemented code with explanations"}
            ],
            "prompt": "You are a software developer. Implement the code based on the problem and plan.\n\nProblem: {problem}\nImplementation Plan: {plan}\n\nProvide the implementation code with comments.",
            "parse_mode": "str",
        },
    ]

    graph = SequentialWorkFlowGraph(
        goal="Generate code to solve programming problems",
        tasks=tasks,
    )

    graph.save_module("debug/tool/sequential_workflow.json")

    agent_manager = AgentManager()
    agent_manager.add_agents_from_workflow(graph, llm_config=llm_config)

    workflow = WorkFlow(graph=graph, agent_manager=agent_manager, llm=llm)

    result = workflow.execute(
        inputs={
            "problem": "Write a Python function to find the longest palindromic substring in a given string."
        }
    )

    if result.status == "success":
        print("Workflow completed!")
        print("Workflow output:\n", result.result)
    else:
        print("Workflow failed:\n", result.displayable_error)


if __name__ == "__main__":
    build_sequential_workflow()