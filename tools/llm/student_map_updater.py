from openai import OpenAI
import os
import re

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

def clean_llm_code_block(raw_output: str) -> str:
    """
    Removes triple backticks and language identifier from LLM response if present.
    """
    pattern = r"^```(?:\w+)?\n([\s\S]*?)\n```$"
    match = re.match(pattern, raw_output.strip())
    if match:
        return match.group(1).strip()
    return raw_output.strip()

def update_rule_file_based_on_feedback(rule_file: list[str], feedback: str) -> list[str]:
    prompt = f"""
You are a lesson adaptation assistant. Given the current list of adaptation rules used for a student, and the student's feedback on the lesson, suggest an updated list of adaptation rules to improve future lessons.

- Keep useful rules from the original list.
- Add new rules if needed based on the feedback.
- Do not include duplicates.
- Respond ONLY with a Python list of rule strings.
- Do NOT wrap the list in triple backticks or any markdown formatting.

Current Rule File:
{rule_file}

Student Feedback:
"{feedback}"

Updated Rule File:
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    raw_output = response.choices[0].message.content.strip()
    clean_output = clean_llm_code_block(raw_output)

    try:
        updated_rules = eval(clean_output)
        if not isinstance(updated_rules, list):
            raise ValueError("Model output is not a list.")
        return updated_rules
    except Exception as e:
        raise ValueError(f"Failed to parse LLM response: {raw_output} — {str(e)}")