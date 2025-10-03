# graph/lesson_graph.py

from langgraph.graph import StateGraph
from graph.schema import State
from graph.nodes.rule_node import rule_node
from graph.nodes.download_lesson_node import download_lesson_node
from graph.nodes.modify_lesson_node import modify_lesson_node
from graph.nodes.audio_node import audio_node
from graph.nodes.visual_node import visual_node
from graph.nodes.final_output_node import final_output_node

# Build the graph
workflow = StateGraph(State)

# Add all nodes
workflow.add_node("rule_node", rule_node)
workflow.add_node("download_lesson_node", download_lesson_node)
workflow.add_node("modify_lesson_node", modify_lesson_node)
workflow.add_node("audio_node", audio_node)
workflow.add_node("visual_node", visual_node)
workflow.add_node("final_output_node", final_output_node)

# Define edges (flow of data)
workflow.set_entry_point("rule_node")
workflow.add_edge("rule_node", "download_lesson_node")
workflow.add_edge("download_lesson_node", "modify_lesson_node")
workflow.add_edge("modify_lesson_node", "audio_node")
workflow.add_edge("audio_node", "visual_node")
workflow.add_edge("visual_node", "final_output_node")

# Define final step
workflow.set_finish_point("final_output_node")

# Compile runnable app
lesson_app = workflow.compile()