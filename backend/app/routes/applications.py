from uuid import uuid4

from fastapi import APIRouter, HTTPException

from app.schemas import (
    ApplicationResponse,
    ApplicationStatus,
    CreateApplicationRequest,
    StatusResponse,
)

router = APIRouter()

# Temporary in-memory store. Replace with Cosmos DB repository layer.
APPLICATIONS: dict[str, dict] = {}

REQUIRED_DOCUMENTS = ["PAN", "AADHAAR", "BANK_LETTER"]


@router.post("", response_model=ApplicationResponse)
def create_application(payload: CreateApplicationRequest) -> ApplicationResponse:
    application_id = f"app_{uuid4().hex[:12]}"
    APPLICATIONS[application_id] = {
        "application_id": application_id,
        "registration_type": payload.registration_type,
        "full_name": payload.full_name,
        "email": payload.email,
        "phone": payload.phone,
        "status": ApplicationStatus.DRAFT,
        "required_documents": REQUIRED_DOCUMENTS,
    }

    return ApplicationResponse(
        application_id=application_id,
        status=ApplicationStatus.DRAFT,
        required_documents=REQUIRED_DOCUMENTS,
    )


@router.get("/{application_id}")
def get_application(application_id: str) -> dict:
    application = APPLICATIONS.get(application_id)
    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return application


@router.get("/{application_id}/status", response_model=StatusResponse)
def get_application_status(application_id: str) -> StatusResponse:
    application = APPLICATIONS.get(application_id)
    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")

    status = application["status"]
    return StatusResponse(
        application_id=application_id,
        status=status,
        message=f"Application is currently in {status} state.",
        next_action_required=status in {ApplicationStatus.DRAFT, ApplicationStatus.MORE_INFO_REQUIRED},
    )


@router.get("/{application_id}/document-checklist")
def get_document_checklist(application_id: str) -> dict:
    if application_id not in APPLICATIONS:
        raise HTTPException(status_code=404, detail="Application not found")

    return {
        "application_id": application_id,
        "documents": [
            {
                "type": document_type,
                "required": True,
                "uploaded": False,
                "allowed_formats": ["pdf", "jpg", "jpeg", "png"],
                "max_size_mb": 10,
            }
            for document_type in REQUIRED_DOCUMENTS
        ],
    }
