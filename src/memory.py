from langgraph.checkpoint.memory import InMemorySaver


def make_checkpointer() -> InMemorySaver:
    return InMemorySaver()
