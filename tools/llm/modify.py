# tools/llm/modify.py

import os
from openai import OpenAI
from typing import List

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

def modify_lesson_content(text: str, rules: List[str]) -> str:
    """
    Uses GPT-4o to apply lesson adaptation rules to the input lesson content.
    Returns a modified lesson in the structure: Engager, I Do, We Do, You Do.
    Only inserts placeholders if the rules require it.
    """
    prompt = f"""
You are an expert inclusive education assistant helping teachers adapt lesson plans for diverse learners.

Your task is to rewrite the lesson using the adaptation rules below. Do not copy these rules into the output.

== Adaptation Rules ==
{chr(10).join(f"- {rule}" for rule in rules)}

== Structure the modified lesson into four clearly labeled sections ==

1. **Engager**: A warm-up to spark curiosity. Could be a question, relatable prompt, or quick writing exercise.
2. **I Do**: The teacher explains the key concepts, vocabulary, or skills. Modify this based on the adaptation rules. Use images or audio *only if required by the rules*.
3. **We Do**: A collaborative activity between teacher and student. Can be a game, shared discussion, or practice task. Adapt as needed for the student.
4. **You Do**: An independent task or mini project the student does alone. Make it achievable and reflective of the skills taught.

== Placeholder Rules ==
- Only use placeholders if required by the adaptation rules.
- Use `[Insert Image: short description]` for important visuals that enhance understanding.
- Use `[Insert Audio: sentence to narrate]` for audio narration or instructions where necessary.
- Do NOT include actual media—just the placeholders.

== Guidelines ==
- DO NOT repeat or list the rules in your output.
- Personalize the content to meet the student’s needs based on the rules.
- Maintain structure and clarity.

Original Lesson Content:
\"\"\"
{text}
\"\"\"

Now generate the modified lesson with the four sections clearly labeled.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that rewrites lesson plans for accessibility using Engager–I Do–We Do–You Do format."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            timeout=60
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        raise RuntimeError(f"Failed to modify lesson with LLM: {str(e)}")