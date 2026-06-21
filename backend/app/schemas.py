from enum import Enum
from pydantic import BaseModel, EmailStr


class ApplicationStatus(str, Enum):
    DRAFT = "DRAFT"
    SUBMITTED = "SUBMITTED"
    DOCUMENTS_UPLOADED = "DOCUMENTS_UPLOADED"
    VALIDATION_IN_PROGRESS = "VALIDATION_IN_PROGRESS"
    MANUAL_REVIEW_REQUIRED = "MANUAL_REVIEW_REQUIRED"
    MORE_INFO_REQUIRED = "MORE_INFO_REQUIRED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class DocumentType(str, Enum):
    PAN = "PAN"
    AADHAAR = "AADHAAR"
    BANK_LETTER = "BANK_LETTER"
    PASSPORT = "PASSPORT"
    OTHER = "OTHER"


class CreateApplicationRequest(BaseModel):
    registration_type: str
    full_name: str
    email: EmailStr
    phone: str


class ApplicationResponse(BaseModel):
    application_id: str
    status: ApplicationStatus
    required_documents: list[str]


class StatusResponse(BaseModel):
    application_id: str
    status: ApplicationStatus
    message: str
    next_action_required: bool


class UploadDocumentResponse(BaseModel):
    document_id: str
    application_id: str
    document_type: DocumentType
    file_name: str
    upload_status: str


class ProcessApplicationResponse(BaseModel):
    application_id: str
    status: ApplicationStatus
    risk_score: int
    decision: str
    validation_results: list[dict]


class ReviewDecisionRequest(BaseModel):
    comment: str | None = None
    reason: str | None = None


class AgentChatRequest(BaseModel):
    conversation_id: str | None = None
    application_id: str | None = None
    message: str


class AgentChatResponse(BaseModel):
    response: str
    tool_calls: list[str]
    application_status: str | None = None
