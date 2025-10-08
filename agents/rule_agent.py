import json
from typing import List, Dict, Union
import os, ast
from openai import OpenAI

# Path to the knowledge base
KNOWLEDGE_BASE_PATH = "configs/knowledge_base.json"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

def generate_cleaned_rules(student_profile: Dict[str, Union[str, List[str]]]) -> List[str]:
    print("[RuleAgent] Extracting rules from knowledge base...")
    rules_to_apply = extract_rules_from_knowledge_base(student_profile)
    print(f"[RuleAgent] Found {len(rules_to_apply)} rules")

    cleaned_rules = filter_rules_with_llm(rules_to_apply)
    print(f"[RuleAgent] Final cleaned rules: {cleaned_rules}")
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

import time

def filter_rules_with_llm(rules: List[str]) -> List[str]:
    print("[RuleAgent] Starting LLM filtering of rules...")
    print(f"[RuleAgent] Input rules ({len(rules)}): {rules}")

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

    start = time.time()

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            timeout=60  # Add timeout to avoid infinite hang
        )
    except Exception as e:
        raise ValueError(f"[RuleAgent] LLM call failed: {e}")

    duration = time.time() - start
    print(f"[RuleAgent] LLM responded in {duration:.2f}s")

    raw_output = response.choices[0].message.content.strip()

    if raw_output.startswith("```"):
        raw_output = raw_output.strip("`")
        lines = raw_output.splitlines()
        lines = [line for line in lines if not line.strip().startswith("python")]
        raw_output = "\n".join(lines).strip()

    try:
        cleaned_rules = ast.literal_eval(raw_output)
        if not isinstance(cleaned_rules, list):
            raise ValueError("LLM did not return a list.")
        print(f"[RuleAgent] Cleaned rules: {cleaned_rules}")
        return cleaned_rules
    except Exception as e:
        raise ValueError(f"Failed to parse LLM response: {raw_output} — {str(e)}")