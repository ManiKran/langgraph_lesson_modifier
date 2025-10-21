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
   Ask simple reflection questions, or connect the story theme to their life.

2. **I Do**  
   This section should feel like a teacher reading and guiding the story to students step-by-step.  
   🔸 **DO NOT summarize**. You must **retell the entire story in full detail**, not in brief.  
   🔸 Use simple, engaging English with embedded emotions, pauses, and reactions.  
   🔸 At key moments, ask questions like “What do you think Daedalus felt here?”  
   🔸 For **hard vocabulary**, embed Dominant Language translations in parentheses.  
   🔸 If the rules require **bilingual scaffolding**, also add Dominant Language translations for whole sentences where the English may be too complex.  
   🔸 Use `[Insert Image: ...]` and `[Insert Audio: ...]` only if the rule demands media.  
   🔸 Do not skip any key detail from the original lesson — treat it as a full retelling, not an outline.  
   🔸 Think of it as storytelling for a multilingual classroom, not as summarization.  
   🔸 **Go paragraph by paragraph through the story**, retelling each one in full. For each paragraph:  
       - Retell the events in simple teacher-style English.  
       - Add reactions (“How might Icarus feel here?”).  
       - Translate full sentences if the English is complex.  
       - Embed Hindi translations (in parentheses) next to hard words.  
       - Only insert images if it helps explain that specific part.

3. **We Do**  
   Create a teacher-guided collaborative activity.  
   🔸 Use dominant language for support if required by rules.  
   🔸 Ask comprehension or prediction questions, or design a role-play or discussion.

4. **You Do**  
   Design an independent task that lets the student show understanding.  
   🔸 Include options for writing, drawing, speaking — support multiple learning styles.  
   🔸 Allow students to use both English and their language if rules suggest bilingualism.

== GENERAL REQUIREMENTS ==
- Do not include the rules in the output.
- Maintain clear structure: Engager → I Do → We Do → You Do.
- Use simple but expressive language.
- Insert visuals or audio only where specifically needed by rules.
- Avoid summarizing — this must feel like a teacher leading a full story reading session.

== LESSON INPUT ==
\"\"\"{text}\"\"\"

Now produce the fully modified lesson based on the student profile rules.
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
    
    

def modify_lesson_content_worksheet(text: str, rules: List[str]) -> str:
    """
    Uses GPT‑4o to adapt worksheet content (questions, instructions, or exercises)
    according to the provided student adaptation rules.

    - Simplifies complex vocabulary and sentence structure.
    - Adds bilingual support or translations if rules require.
    - Adds [Insert Image: ...] and [Insert Audio: ...] placeholders only if rules demand media.
    - Keeps the original worksheet’s logical structure (no Engager/I Do/We Do/You Do).
    """

    prompt = f"""
You are an expert inclusive education designer adapting **worksheet content** for multilingual
and special‑needs students.

== Student Profile Rules ==
{chr(10).join(f"- {rule}" for rule in rules)}

== TASK ==
You will rewrite the following worksheet according to these rules.
Your job is to make the content **accessible, bilingual if needed, and engaging** — but
without changing its basic structure.

== GUIDELINES ==

1. **Simplify and Support**
   - Simplify complex words or grammar.
   - If the student’s dominant language is mentioned in the rules (e.g., Hindi, Spanish, etc.),
     include **translations in parentheses** beside hard vocabulary or complex phrases.
   - Maintain question numbering, blanks, and formatting.

2. **Media Placeholders**
   - If rules mention “add visuals” or “use images,” insert `[Insert Image: ...]`
     after the relevant question or section to help comprehension.
   - If rules mention “add audio,” insert `[Insert Audio: ...]`
     where reading or listening support would help the student understand better.
   - Keep placeholders minimal and relevant.

3. **Do NOT:**
   - Summarize or remove any exercise.
   - Add Engager/I Do/We Do/You Do structure.
   - Introduce new unrelated questions.

4. **Tone**
   - Use a friendly, teacher-like tone that guides the student through the worksheet.
   - Use plain, encouraging English with occasional bilingual scaffolding if required.

== WORKSHEET INPUT ==
\"\"\"{text}\"\"\"

Now produce the adapted worksheet following all the student profile rules.
Ensure that placeholders are included only if demanded by the rules.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a multilingual inclusive education assistant. "
                        "You rewrite worksheets for students with diverse learning and language needs, "
                        "keeping the structure unchanged while adding supports and placeholders."
                    )
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            timeout=60
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        raise RuntimeError(f"Failed to modify worksheet with LLM: {str(e)}")