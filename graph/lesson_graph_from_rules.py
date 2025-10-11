from langgraph.graph import StateGraph
from graph.schema import State
from graph.nodes.download_lesson_node import download_lesson_node
from graph.nodes.modify_lesson_node import modify_lesson_node
from graph.nodes.final_output_node import final_output_node

# Build a new graph that skips rule_node
workflow = StateGraph(State)

workflow.add_node("download_lesson_node", download_lesson_node)
workflow.add_node("modify_lesson_node", modify_lesson_node)
workflow.add_node("final_output_node", final_output_node)

workflow.set_entry_point("download_lesson_node")
workflow.add_edge("download_lesson_node", "modify_lesson_node")
workflow.add_edge("modify_lesson_node", "final_output_node")
workflow.set_finish_point("final_output_node")

lesson_from_rules_app = workflow.compile()