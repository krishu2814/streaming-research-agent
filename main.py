from graph import graph


def handle_event(event):
    # type of event is determined by the "type" key in the event dictionary
    event_type = event.get("type")

    if event_type == "agent_progress":

        agent = event["agent"]
        message = event["message"]

        print(f"\n[{agent.upper()}] {message}")

    elif event_type == "llm_token":

        print(
            event["token"],
            end="",
            flush=True,
        )


def main():
    # code start from here
    input_data = {
        "topic": "Agentic AI",
        "plan": "",
        "research": "",
        "final_answer": "",
    }

    for event in graph.stream(input_data, stream_mode="custom"):
        handle_event(event)

    print("\n")


# execute the main function when the script is run directly
if __name__ == "__main__":
    main()
