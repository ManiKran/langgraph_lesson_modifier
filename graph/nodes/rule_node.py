# graph/nodes/rule_node.py

from agents.rule_agent import generate_cleaned_rules

def rule_node(state: dict) -> dict:
    """
    LangGraph node to extract and filter adaptation rules based on student profile.
    Adds 'rules' to the state for downstream nodes.
    """
    profile = state.get("student_profile")
    if not profile:
        raise ValueError("Missing 'student_profile' in state.")
    
    cleaned_rules = generate_cleaned_rules(profile)
    state.update({"rules" : cleaned_rules})

    return state