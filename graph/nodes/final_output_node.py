# graph/nodes/final_output_node.py

from tools.output.generate import generate_final_output

def final_output_node(state: dict) -> dict:
    """
    Creates the final output files (both .txt and .json) combining text, images, and audio.
    """
    lesson_text = state.get("modified_lesson_text", "")
    image_paths = state.get("image_paths", [])
    audio_paths = state.get("audio_paths", [])

    if not lesson_text:
        raise ValueError("Missing modified_lesson_text in state.")

    # generate_final_output now returns {"txt_path": ..., "json_path": ...}
    result = generate_final_output(lesson_text, image_paths, audio_paths)

    # update state with both outputs
    state.update({
        "final_output_path": result["txt_path"],       # path to the .txt file
        "final_output_json": result["json_path"]       # path to the .json file
    })
    return state