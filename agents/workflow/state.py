from typing import TypedDict


class RegistrationWorkflowState(TypedDict, total=False):
    application_id: str
    user_id: str
    status: str
    required_documents: list[str]
    uploaded_documents: list[str]
    extracted_fields: dict[str, dict]
    validation_results: list[dict]
    risk_score: int
    risk_level: str
    decision: str
    messages: list[str]
