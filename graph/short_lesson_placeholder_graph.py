# graph/lesson_graph_placeholders.py

from langgraph.graph import StateGraph
from graph.schema import State
from graph.nodes.rule_node import set_rules
from graph.nodes.download_lesson_node import download_lesson_node
from graph.nodes.modify_lesson_node import modify_lesson_node
from graph.nodes.final_output_node import final_output_node  # No audio/visual!

# Build the graph
workflow = StateGraph(State)

# Only essential nodes
workflow.add_node("set_rules", set_rules)
workflow.add_node("download_lesson_node", download_lesson_node)
workflow.add_node("modify_lesson_node", modify_lesson_node)
workflow.add_node("final_output_node", final_output_node)

# Define flow
workflow.set_entry_point("set_rules")
workflow.add_node("set_rules", "download_lesson_node")
workflow.add_edge("download_lesson_node", "modify_lesson_node")
workflow.add_edge("modify_lesson_node", "final_output_node")

# Final step
workflow.set_finish_point("final_output_node")

# Compile new app
short_lesson_placeholders_app = workflow.compile()