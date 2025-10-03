# graph/nodes/audio_node.py

from tools.audio.generate import split_text_for_audio, generate_audio_for_text_chunks

def audio_node(state: dict) -> dict:
    """
    Generates audio narration based on modified lesson and rules.
    Adds audio paths and inline placeholders to the lesson.
    """
    rules = state.get("rules", [])
    lesson_text = state.get("modified_lesson_text", "")

    if not any("audio" in r.lower() for r in rules):
        print("[AudioNode] No audio-related rule. Skipping.")
        state["audio_paths"] = []
        return state

    chunks = split_text_for_audio(lesson_text)
    audio_results = generate_audio_for_text_chunks(chunks)

    # Insert [AUDIO:filename.mp3] markers inline
    for path, text in audio_results:
        filename = os.path.basename(path)
        lesson_text = lesson_text.replace(text, f"{text}\n\n[AUDIO:{filename}]")

    # Update state
    state["modified_lesson_text"] = lesson_text
    state["audio_paths"] = [path for path, _ in audio_results]
    return state