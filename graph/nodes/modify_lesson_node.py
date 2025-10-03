# graph/nodes/modify_lesson_node.py

from tools.llm.modify import modify_lesson_content

def modify_lesson_node(state: dict) -> dict:
    """
    Applies adaptation rules to the lesson content using GPT-4o.
    Adds structured placeholders for visuals and audio.
    """
    rules = state.get("rules")
    lesson_content = state.get("lesson_content")

    if not rules:
        raise ValueError("Missing 'rules' in state.")
    if not lesson_content:
        raise ValueError("Missing 'lesson_content' in state.")

    # Apply LLM-based modifications
    try:
        modified_text = modify_lesson_content(lesson_content, rules)
    except Exception as e:
        raise RuntimeError(f"Failed to modify lesson: {str(e)}")

    # Store output in state
    state["modified_lesson_text"] = modified_text
    return state