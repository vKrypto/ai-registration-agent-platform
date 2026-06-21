from workflow.graph import build_registration_workflow


def test_workflow_approves_low_risk_complete_application():
    workflow = build_registration_workflow()

    result = workflow.invoke(
        {
            "application_id": "app_test_001",
            "user_id": "usr_test_001",
            "status": "SUBMITTED",
            "required_documents": ["PAN", "AADHAAR", "BANK_LETTER"],
            "uploaded_documents": ["PAN", "AADHAAR", "BANK_LETTER"],
            "messages": [],
        }
    )

    assert result["status"] == "APPROVED"
    assert result["decision"] == "APPROVED"
    assert result["risk_level"] == "LOW"


def test_workflow_stops_when_documents_are_missing():
    workflow = build_registration_workflow()

    result = workflow.invoke(
        {
            "application_id": "app_test_002",
            "user_id": "usr_test_002",
            "status": "SUBMITTED",
            "required_documents": ["PAN", "AADHAAR", "BANK_LETTER"],
            "uploaded_documents": ["PAN"],
            "messages": [],
        }
    )

    assert result["status"] == "MORE_INFO_REQUIRED"
    assert "decision" not in result
    assert "extracted_fields" not in result
