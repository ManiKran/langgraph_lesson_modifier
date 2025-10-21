# tools/llm/modify.py

import os
from openai import OpenAI
from typing import List

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

def modify_lesson_content(text: str, rules: List[str]) -> str:
    """
    Uses GPT‑4o to apply lesson adaptation rules to the input lesson content.
    Produces a structured output: Engager → I Do → We Do → You Do.
    Enforces side-by-side translations or accessibility features if required.
    """
    prompt = f"""
You are an expert inclusive education designer who adapts lessons for multilingual and special‑needs learners.

== Student Profile Rules ==
{chr(10).join(f"- {rule}" for rule in rules)}

== TASK ==
Rewrite the following lesson using the “Engager → I Do → We Do → You Do” framework described below.
Apply *all relevant rules*, including any language‑ or accessibility‑specific adaptations.

== SECTION GUIDELINES ==

1. **Engager**  
   Start with a warm‑up or connection activity that emotionally or intellectually prepares the learner.

2. **I Do**  
   The teacher explains the concept, vocabulary, and key ideas of the lesson.  
   - Summarize the core narrative or concept in simple English.  
   - Define difficult vocabulary words.  
   - **If any rule mentions side‑by‑side translation or dominant language**, then for every complex word or phrase, include a short translation in parentheses in that language.  
     Example (for Hindi):  
     *The word “ingenious” (चतुर / clever) means very smart or inventive.*  
   - Insert `[Insert Image: ...]` or `[Insert Audio: ...]` *only if the rules require visual/audio support.*

3. **We Do**  
   Create an interactive, teacher‑student practice activity (discussion, game, or roleplay).  
   Use the student’s dominant language for scaffolding if rules mention bilingual learning.

4. **You Do**  
   Design an independent activity that allows the student to demonstrate understanding.  
   Include flexible output choices (oral, written, visual) based on rules.

== GENERAL REQUIREMENTS ==
- Maintain logical flow and coherence.
- Use simple, clear English adapted to the learner’s level.
- Only insert media placeholders where the rules demand them.
- Keep translations concise and in parentheses next to difficult words.
- Do not include the list of rules in the output.

== LESSON INPUT ==
\"\"\"{text}\"\"\"

Now produce the modified lesson.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an inclusive education assistant who strictly follows adaptation rules. "
                        "You must always apply bilingual or accessibility modifications when requested."
                    )
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            timeout=60
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        raise RuntimeError(f"Failed to modify lesson with LLM: {str(e)}")