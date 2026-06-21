from app.schemas import ApplicationStatus


def extract_fields(documents: list[dict]) -> dict[str, dict]:
    """Mock OCR extraction. Replace with Azure AI Vision or Document Intelligence."""
    extracted: dict[str, dict] = {}

    for document in documents:
        document_type = document["document_type"]
        if document_type == "PAN":
            extracted["PAN"] = {
                "name": "John Smith",
                "pan_number": "ABCDE1234F",
                "confidence": 0.98,
            }
        elif document_type == "AADHAAR":
            extracted["AADHAAR"] = {
                "name": "John Smith",
                "last_4_digits": "1234",
                "confidence": 0.95,
            }
        elif document_type == "BANK_LETTER":
            extracted["BANK_LETTER"] = {
                "account_holder": "John Smith",
                "confidence": 0.94,
            }

    return extracted


def validate_documents(required_documents: list[str], uploaded_documents: list[dict], extracted_fields: dict[str, dict]) -> list[dict]:
    uploaded_types = {document["document_type"] for document in uploaded_documents}
    results: list[dict] = []

    for required_document in required_documents:
        results.append(
            {
                "rule": f"{required_document}_UPLOADED",
                "result": "PASS" if required_document in uploaded_types else "FAIL",
                "severity": "HIGH",
            }
        )

    if "PAN" in extracted_fields and extracted_fields["PAN"].get("pan_number"):
        results.append({"rule": "PAN_NUMBER_PRESENT", "result": "PASS", "severity": "HIGH"})
    else:
        results.append({"rule": "PAN_NUMBER_PRESENT", "result": "FAIL", "severity": "HIGH"})

    return results


def calculate_risk(validation_results: list[dict]) -> int:
    high_failures = [
        result
        for result in validation_results
        if result.get("result") == "FAIL" and result.get("severity") == "HIGH"
    ]
    return 20 if not high_failures else 85


def decide_status(risk_score: int) -> tuple[ApplicationStatus, str]:
    if risk_score <= 30:
        return ApplicationStatus.APPROVED, "APPROVED"
    return ApplicationStatus.MANUAL_REVIEW_REQUIRED, "MANUAL_REVIEW_REQUIRED"
