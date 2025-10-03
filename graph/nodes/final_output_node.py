# graph/nodes/final_output_node.py

from tools.output.generate import generate_final_output

def final_output_node(state: dict) -> dict:
    """
    Creates the final output file combining text, images, and audio.
    """
    lesson_text = state.get("modified_lesson_text", "")
    image_paths = state.get("image_paths", [])
    audio_paths = state.get("audio_paths", [])

    if not lesson_text:
        raise ValueError("Missing modified_lesson_text in state.")

    final_path = generate_final_output(lesson_text, image_paths, audio_paths)
    state.update({"final_output_path" : final_path})
    return state