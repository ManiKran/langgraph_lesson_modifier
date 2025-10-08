# graph/nodes/audio_node.py

from tools.audio.generate import split_text_for_audio, generate_audio_for_text_chunks
import os
import time

def audio_node(state: dict) -> dict:
    """
    Generates up to 5 audio narration files based on the modified lesson and rules.
    Adds audio paths and inline [AUDIO:<filename>] markers to the lesson text.
    """
    start_time = time.time()

    rules = state.get("rules", [])
    lesson_text = state.get("modified_lesson_text", "")

    if not any("audio" in r.lower() for r in rules):
        print("[AudioNode] No audio-related rule found. Skipping audio generation.")
        state.update({"audio_paths": []})
        return state

    if not lesson_text.strip():
        print("[AudioNode] Empty lesson text. Skipping audio generation.")
        state.update({"audio_paths": []})
        return state

    print("[AudioNode] Splitting lesson text into 5 chunks for audio generation...")
    chunks = split_text_for_audio(lesson_text, num_chunks=5)
    print(f"[AudioNode] Generated {len(chunks)} text chunks for TTS.")

    # Generate audio for each chunk
    audio_results = generate_audio_for_text_chunks(chunks)
    print(f"[AudioNode] Successfully generated {len(audio_results)} audio files.")

    # Insert [AUDIO:filename.mp3] markers inline
    for path, text in audio_results:
        filename = os.path.basename(path)
        lesson_text = lesson_text.replace(text, f"{text}\n\n[AUDIO:{filename}]")

    # Update state
    state.update({
        "modified_lesson_text": lesson_text,
        "audio_paths": [path for path, _ in audio_results]
    })

    print(f"[AudioNode] Completed in {time.time() - start_time:.2f}s.")
    return state