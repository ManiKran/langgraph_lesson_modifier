# tools/llm/modify.py

import os
from openai import OpenAI
from typing import List

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

def modify_lesson_content(text: str, rules: List[str]) -> str:
    """
    Uses GPT-4o to apply lesson adaptation rules to the input lesson content.
    Returns modified lesson content with placeholders for visuals and audio.
    """
    prompt = f"""
You are an inclusive education assistant helping to adapt lesson plans for students with special learning needs.

Below are the adaptation rules to be applied. Use them to guide your modifications, but do NOT repeat or list these rules in the output.

Adaptation Rules:
{chr(10).join(f"- {rule}" for rule in rules)}

Now, based on these rules, modify the following lesson content.

Instructions:
- modify the content based on the rules provided.
- Apply all the rules that are mentioned.
- Add [Insert Image: short description] where a visual would help understanding.
- Add [Insert Audio: sentence to narrate] where an audio explanation or read-aloud would benefit the learner.
- Do NOT include actual image or audio content. Only use these placeholders.
- Ensure structure and flow of the lesson remain intact.

Original Lesson:
\"\"\"
{text}
\"\"\"

Modified Lesson:
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that adapts educational lessons for accessibility and inclusion."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        raise RuntimeError(f"Failed to modify lesson with LLM: {str(e)}")