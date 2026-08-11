from langgraph.config import get_stream_writer
from langgraph.graph import StateGraph, START, END

# imported from state.py -> class ResearchState
from state import ResearchState

# import llm from llm.py
from llm import llm


def planner(state: ResearchState):

    writer = get_stream_writer()

    # writer() calls handle_event() in main.py to send events to the main function
    writer(
        {
            "type": "agent_progress",
            "agent": "planner",
            "status": "started",
            "message": "Planner started",
        }
    )

    topic = state["topic"]

    plan = (
        f"Research the topic '{topic}' by identifying "
        "the main concepts, important developments, "
        "and practical applications."
    )

    writer(
        {
            "type": "agent_progress",
            "agent": "planner",
            "status": "completed",
            "message": "Planner completed",
        }
    )

    return {"plan": plan}


#
def researcher(state: ResearchState):

    writer = get_stream_writer()

    writer(
        {
            "type": "agent_progress",
            "agent": "researcher",
            "status": "started",
            "message": "Research started",
        }
    )

    topic = state["topic"]
    plan = state["plan"]

    # Simulated research for now.
    research = (
        f"Research findings for '{topic}'.\n\n"
        f"Research plan: {plan}\n\n"
        "The topic is relevant to modern AI engineering. "
        "It involves model orchestration, tools, workflows, "
        "state management, and production infrastructure."
    )

    writer(
        {
            "type": "agent_progress",
            "agent": "researcher",
            "status": "completed",
            "message": "Research completed",
        }
    )

    return {"research": research}


def reviewer(state: ResearchState):

    writer = get_stream_writer()

    writer(
        {
            "type": "agent_progress",
            "agent": "reviewer",
            "status": "started",
            "message": "Reviewer started",
        }
    )

    prompt = f"""
You are a senior research reviewer.

Topic:
{state["topic"]}

Research plan:
{state["plan"]}

Research findings:
{state["research"]}

Create a concise but useful final answer about the topic.

Requirements:
- Be technically accurate.
- Explain the important concepts.
- Avoid unnecessary repetition.
- Use clear sections.
"""

    final_answer = ""

    for chunk in llm.stream(prompt):

        token = chunk.content

        if token:

            final_answer += token

            writer(
                {
                    "type": "llm_token",
                    "agent": "reviewer",
                    "token": token,
                }
            )

    # after loop ends, send a final event to indicate completion
    writer(
        {
            "type": "agent_progress",
            "agent": "reviewer",
            "status": "completed",
            "message": "Reviewer completed",
        }
    )

    return {"final_answer": final_answer}


builder = StateGraph(ResearchState)

builder.add_node("planner", planner)
builder.add_node("researcher", researcher)
builder.add_node("reviewer", reviewer)

builder.add_edge(START, "planner")
builder.add_edge("planner", "researcher")
builder.add_edge("researcher", "reviewer")
builder.add_edge("reviewer", END)

graph = builder.compile()
# print(graph)
