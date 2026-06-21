from io import BytesIO

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def create_application() -> str:
    response = client.post(
        "/api/v1/applications",
        json={
            "registration_type": "individual",
            "full_name": "John Smith",
            "email": "john@example.com",
            "phone": "+911234567890",
        },
    )

    assert response.status_code == 200
    return response.json()["application_id"]


def upload_document(application_id: str, document_type: str) -> None:
    response = client.post(
        f"/api/v1/applications/{application_id}/documents",
        data={"document_type": document_type},
        files={"file": (f"{document_type.lower()}.pdf", BytesIO(b"fake-pdf-content"), "application/pdf")},
    )

    assert response.status_code == 200
    assert response.json()["document_type"] == document_type


def test_complete_registration_flow_auto_approves():
    application_id = create_application()

    upload_document(application_id, "PAN")
    upload_document(application_id, "AADHAAR")
    upload_document(application_id, "BANK_LETTER")

    process_response = client.post(f"/api/v1/applications/{application_id}/process")

    assert process_response.status_code == 200
    body = process_response.json()
    assert body["status"] == "APPROVED"
    assert body["decision"] == "APPROVED"
    assert body["risk_score"] == 20

    details_response = client.get(f"/api/v1/applications/{application_id}")
    actions = [event["action"] for event in details_response.json()["audit_events"]]
    assert "CREATE_APPLICATION" in actions
    assert "UPLOAD_DOCUMENT" in actions
    assert "PROCESS_APPLICATION" in actions


def test_incomplete_registration_goes_to_manual_review():
    application_id = create_application()

    upload_document(application_id, "PAN")

    process_response = client.post(f"/api/v1/applications/{application_id}/process")

    assert process_response.status_code == 200
    body = process_response.json()
    assert body["status"] == "MANUAL_REVIEW_REQUIRED"
    assert body["decision"] == "MANUAL_REVIEW_REQUIRED"

    queue_response = client.get("/api/v1/reviewer/queue")

    assert queue_response.status_code == 200
    assert any(item["application_id"] == application_id for item in queue_response.json()["items"])


def test_reviewer_can_request_more_information():
    application_id = create_application()
    upload_document(application_id, "PAN")
    client.post(f"/api/v1/applications/{application_id}/process")

    response = client.post(
        f"/api/v1/reviewer/applications/{application_id}/request-info",
        json={"comment": "Please upload Aadhaar and bank letter."},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "MORE_INFO_REQUIRED"

    details_response = client.get(f"/api/v1/reviewer/applications/{application_id}")
    actions = [event["action"] for event in details_response.json()["audit_events"]]
    assert "REQUEST_MORE_INFORMATION" in actions
