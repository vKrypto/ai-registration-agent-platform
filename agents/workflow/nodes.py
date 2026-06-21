from workflow.state import RegistrationWorkflowState


def collect_documents(state: RegistrationWorkflowState) -> RegistrationWorkflowState:
    required = state.get("required_documents", ["PAN", "AADHAAR", "BANK_LETTER"])
    uploaded = state.get("uploaded_documents", [])
    missing = [doc for doc in required if doc not in uploaded]

    state["required_documents"] = required
    state["status"] = "DOCUMENTS_UPLOADED" if not missing else "MORE_INFO_REQUIRED"
    state.setdefault("messages", []).append(f"Missing documents: {missing}" if missing else "All required documents uploaded.")
    return state


def extract_fields(state: RegistrationWorkflowState) -> RegistrationWorkflowState:
    # Mock extraction. Replace with OCR / Azure AI Vision / Document Intelligence integration.
    state["status"] = "EXTRACTION_IN_PROGRESS"
    state["extracted_fields"] = {
        "PAN": {"name": "John Smith", "pan_number": "ABCDE1234F", "confidence": 0.98},
        "AADHAAR": {"name": "John Smith", "last_4_digits": "1234", "confidence": 0.95},
        "BANK_LETTER": {"account_holder": "John Smith", "confidence": 0.94},
    }
    return state


def validate_documents(state: RegistrationWorkflowState) -> RegistrationWorkflowState:
    extracted = state.get("extracted_fields", {})
    validation_results = []

    pan = extracted.get("PAN", {})
    if pan.get("pan_number"):
        validation_results.append({"rule": "PAN_PRESENT", "result": "PASS"})
    else:
        validation_results.append({"rule": "PAN_PRESENT", "result": "FAIL"})

    state["validation_results"] = validation_results
    state["status"] = "VALIDATION_IN_PROGRESS"
    return state


def calculate_risk(state: RegistrationWorkflowState) -> RegistrationWorkflowState:
    failures = [item for item in state.get("validation_results", []) if item.get("result") == "FAIL"]
    risk_score = 20 if not failures else 80

    state["risk_score"] = risk_score
    state["risk_level"] = "LOW" if risk_score <= 30 else "HIGH"
    state["status"] = "RISK_REVIEW_IN_PROGRESS"
    return state


def decide(state: RegistrationWorkflowState) -> RegistrationWorkflowState:
    risk_score = state.get("risk_score", 100)

    if risk_score <= 30:
        state["decision"] = "APPROVED"
        state["status"] = "APPROVED"
    else:
        state["decision"] = "MANUAL_REVIEW_REQUIRED"
        state["status"] = "MANUAL_REVIEW_REQUIRED"

    return state
