from uuid import uuid4

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from app.schemas import (
    ApplicationResponse,
    ApplicationStatus,
    CreateApplicationRequest,
    DocumentType,
    ProcessApplicationResponse,
    StatusResponse,
    UploadDocumentResponse,
)
from app.services.processing import calculate_risk, decide_status, extract_fields, validate_documents

router = APIRouter()

# Temporary in-memory stores. Replace with Cosmos DB and Blob Storage repository layers.
APPLICATIONS: dict[str, dict] = {}
DOCUMENTS: dict[str, list[dict]] = {}

REQUIRED_DOCUMENTS = ["PAN", "AADHAAR", "BANK_LETTER"]
ALLOWED_CONTENT_TYPES = {"application/pdf", "image/jpeg", "image/png"}
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024


@router.post("", response_model=ApplicationResponse)
def create_application(payload: CreateApplicationRequest) -> ApplicationResponse:
    application_id = f"app_{uuid4().hex[:12]}"
    APPLICATIONS[application_id] = {
        "application_id": application_id,
        "registration_type": payload.registration_type,
        "full_name": payload.full_name,
        "email": str(payload.email),
        "phone": payload.phone,
        "status": ApplicationStatus.DRAFT,
        "required_documents": REQUIRED_DOCUMENTS,
        "risk_score": None,
        "decision": None,
        "validation_results": [],
    }
    DOCUMENTS[application_id] = []

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

    return {
        **application,
        "documents": DOCUMENTS.get(application_id, []),
    }


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

    uploaded_types = {document["document_type"] for document in DOCUMENTS.get(application_id, [])}

    return {
        "application_id": application_id,
        "documents": [
            {
                "type": document_type,
                "required": True,
                "uploaded": document_type in uploaded_types,
                "allowed_formats": ["pdf", "jpg", "jpeg", "png"],
                "max_size_mb": 10,
            }
            for document_type in REQUIRED_DOCUMENTS
        ],
    }


@router.post("/{application_id}/documents", response_model=UploadDocumentResponse)
async def upload_document(
    application_id: str,
    document_type: DocumentType = Form(...),
    file: UploadFile = File(...),
) -> UploadDocumentResponse:
    if application_id not in APPLICATIONS:
        raise HTTPException(status_code=404, detail="Application not found")

    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    content = await file.read()
    if len(content) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(status_code=400, detail="File size exceeds 10 MB limit")

    document_id = f"doc_{uuid4().hex[:12]}"
    document = {
        "document_id": document_id,
        "application_id": application_id,
        "document_type": document_type.value,
        "file_name": file.filename or "uploaded-file",
        "content_type": file.content_type,
        "file_size": len(content),
        "upload_status": "UPLOADED",
        "blob_url": f"mock://documents/{application_id}/{document_id}",
    }

    DOCUMENTS.setdefault(application_id, []).append(document)
    APPLICATIONS[application_id]["status"] = ApplicationStatus.DOCUMENTS_UPLOADED

    return UploadDocumentResponse(
        document_id=document_id,
        application_id=application_id,
        document_type=document_type,
        file_name=document["file_name"],
        upload_status="UPLOADED",
    )


@router.post("/{application_id}/process", response_model=ProcessApplicationResponse)
def process_application(application_id: str) -> ProcessApplicationResponse:
    application = APPLICATIONS.get(application_id)
    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")

    documents = DOCUMENTS.get(application_id, [])
    extracted = extract_fields(documents)
    validation_results = validate_documents(REQUIRED_DOCUMENTS, documents, extracted)
    risk_score = calculate_risk(validation_results)
    status, decision = decide_status(risk_score)

    application["status"] = status
    application["risk_score"] = risk_score
    application["decision"] = decision
    application["validation_results"] = validation_results
    application["extracted_fields"] = extracted

    return ProcessApplicationResponse(
        application_id=application_id,
        status=status,
        risk_score=risk_score,
        decision=decision,
        validation_results=validation_results,
    )
