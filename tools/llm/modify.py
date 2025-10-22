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

5. **Assessment**  
   Create 3 multiple-choice questions that assess the **main concept** or learning goal of the lesson — not just the retelling in “I Do”.  
   🔸 Each question should check the student’s understanding of the key ideas or themes.  
   🔸 Provide 3–4 answer options in a vertical list, with clear line breaks between them and use alphabetical notation for each option.  
   🔸 Do **not** include the correct answer — the student must choose.  
   🔸 include translated versions of each question and option IN THE Dominant Language(e.g., Hindi, Spanish) below the English.  
   🔸 If audio is required, add `[Insert Audio: Question X]` after each question.  
   🔸 Use student-friendly language and keep vocabulary consistent with the rest of the modified lesson.

== GENERAL REQUIREMENTS ==
- Do not include the rules in the output.
- Maintain clear structure: Engager → I Do → We Do → You Do.
- Use simple but expressive language.
- Insert visuals or audio only where specifically needed by rules.
- Maintain clear structure with H1 for title, H2 for sections, H3 for subheadings, and normal text elsewhere.
- Keep the tone teacher-like, expressive, and friendly.
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
Rewrite the following worksheet strictly in **Markdown format** according to the rules below.
Your goal is to make the worksheet **accessible, bilingual if required, and easy to follow**, while keeping
its original structure and question flow.

== OUTPUT FORMAT (Markdown Rules) ==
- Use Markdown headings and text consistently:
  - `##` → for main worksheet sections (e.g., Reading Comprehension, Vocabulary Practice)
  - `###` → for each question number or instruction
  - Regular text → for question content and answer options
- For multiple-choice questions:
  - Do **not** use boxes or ASCII drawings.
  - Use standard **alphabetical notation** for options, formatted as:
    ```
    A) Option one  
    B) Option two  
    C) Option three  
    D) Option four
    ```
- After each **question** and **each option**, if rules mention bilingual or audio support:
  - Include the **translated version** of that question or option in the student's dominant language in parentheses.
  - Then, add an **audio placeholder** below it like:
    ```
    [Insert Audio: Question 1]
    ```
  or
    ```
    [Insert Audio: Option A]
    ```

== CONTENT ADAPTATION RULES ==
1. **Simplify and Support**
   - Simplify complex words and grammar.
   - When applicable, add translations (in parentheses) beside challenging vocabulary or full sentences.
   - Maintain numbering, blanks, and structure.

2. **Multiple Choice and Structured Questions**
   - Preserve numbering and format.
   - Write all options clearly in simple Markdown format.
   - Add bilingual translations and audio placeholders as required by the rules.

3. **Media Placeholders**
   - If visuals are required, include `[Insert Image: ...]` after the related question.
   - If audio is required, use `[Insert Audio: ...]` after questions or options.

4. **Tone**
   - Use a warm, teacher-like tone.
   - Encourage and guide the student gently through the worksheet.

5. **Do NOT:**
   - Summarize or remove exercises.
   - Add new content or alter question meanings.
   - Use any Engager/I Do/We Do/You Do structure — this is a worksheet, not a lesson.

== WORKSHEET INPUT ==
\"\"\"{text}\"\"\"

== OUTPUT REQUIREMENTS ==
- The output must be valid **Markdown**.
- Section titles as `##`, questions as `###`, options and text as normal paragraphs.
- Include translated versions and `[Insert Audio: ...]` placeholders if the rules demand them.
- Do not include the rules or system instructions in the output.

Now produce the fully adapted worksheet in Markdown format following these guidelines.
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
