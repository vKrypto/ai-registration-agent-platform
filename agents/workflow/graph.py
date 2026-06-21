from langgraph.graph import END, StateGraph

from workflow.nodes import (
    calculate_risk,
    collect_documents,
    decide,
    extract_fields,
    validate_documents,
)
from workflow.state import RegistrationWorkflowState


def build_registration_workflow():
    graph = StateGraph(RegistrationWorkflowState)

    graph.add_node("collect_documents", collect_documents)
    graph.add_node("extract_fields", extract_fields)
    graph.add_node("validate_documents", validate_documents)
    graph.add_node("calculate_risk", calculate_risk)
    graph.add_node("decide", decide)

    graph.set_entry_point("collect_documents")
    graph.add_edge("collect_documents", "extract_fields")
    graph.add_edge("extract_fields", "validate_documents")
    graph.add_edge("validate_documents", "calculate_risk")
    graph.add_edge("calculate_risk", "decide")
    graph.add_edge("decide", END)

    return graph.compile()
