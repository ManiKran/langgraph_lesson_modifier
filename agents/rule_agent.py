import json
from typing import List, Dict, Union
import os
from openai import OpenAI

# Path to the knowledge base
KNOWLEDGE_BASE_PATH = "configs/knowledge_base.json"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

def generate_cleaned_rules(student_profile: Dict[str, Union[str, List[str]]]) -> List[str]:
    """
    Extract rules from the knowledge base using the student profile
    and clean them with LLM filtering.
    """
    rules_to_apply = extract_rules_from_knowledge_base(student_profile)
    cleaned_rules = filter_rules_with_llm(rules_to_apply)
    return cleaned_rules

def extract_rules_from_knowledge_base(student_profile: Dict[str, Union[str, List[str]]]) -> List[str]:
    """
    Extract relevant rules based on the student profile.
    """
    with open(KNOWLEDGE_BASE_PATH, "r") as f:
        rule_base = json.load(f)

    extracted_rules = []

    for key, value in student_profile.items():
        if key in rule_base:
            if isinstance(value, list):
                for item in value:
                    if item in rule_base[key]:
                        extracted_rules.extend(rule_base[key][item])
            elif isinstance(value, str):
                if value in rule_base[key]:
                    extracted_rules.extend(rule_base[key][value])

    return extracted_rules

def filter_rules_with_llm(rules: List[str]) -> List[str]:
    """
    Filter out duplicates and resolve conflicts using GPT-4o.
    """
    prompt = f"""
You are a rule optimization assistant for lesson planning.
Here is a list of adaptation rules extracted based on a student's profile:

{rules}

Your task:
- Remove duplicate or nearly identical rules.
- If there is a direct conflict (e.g. 'include visuals' and 'don't include visuals'), keep the more restrictive/explicit one (e.g. 'don't include visuals').
- Ensure the final list contains only meaningful, non-conflicting rules.
- Return only a valid Python list of strings.

Optimized Rule List:
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    raw_output = response.choices[0].message.content.strip()

    if raw_output.startswith("```"):
        # remove ``` at start and end
        raw_output = raw_output.strip("`")
        # split off lines
        lines = raw_output.splitlines()
        # remove language tag like 'python'
        lines = [line for line in lines if not line.strip().startswith("python")]
        raw_output = "\n".join(lines).strip()

    try:
        cleaned_rules = eval(raw_output)
        if not isinstance(cleaned_rules, list):
            raise ValueError("LLM did not return a list.")
        return cleaned_rules
    except Exception as e:
        raise ValueError(f"Failed to parse LLM response: {raw_output} — {str(e)}")