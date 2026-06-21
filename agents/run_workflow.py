from workflow.graph import build_registration_workflow


if __name__ == "__main__":
    workflow = build_registration_workflow()

    initial_state = {
        "application_id": "app_demo_001",
        "user_id": "usr_demo_001",
        "status": "SUBMITTED",
        "required_documents": ["PAN", "AADHAAR", "BANK_LETTER"],
        "uploaded_documents": ["PAN", "AADHAAR", "BANK_LETTER"],
        "messages": [],
    }

    result = workflow.invoke(initial_state)
    print(result)
