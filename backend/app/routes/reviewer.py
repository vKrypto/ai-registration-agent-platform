from fastapi import APIRouter, HTTPException

from app.routes.applications import APPLICATIONS
from app.schemas import ApplicationStatus, ReviewDecisionRequest
from app.services.audit import get_audit_events, record_audit_event

router = APIRouter()


@router.get("/queue")
def get_review_queue() -> dict:
    items = [
        {
            "application_id": application["application_id"],
            "status": application["status"],
            "risk_score": application.get("risk_score"),
            "reason": application.get("decision"),
        }
        for application in APPLICATIONS.values()
        if application["status"] == ApplicationStatus.MANUAL_REVIEW_REQUIRED
    ]

    return {"items": items}


@router.get("/applications/{application_id}")
def get_review_details(application_id: str) -> dict:
    application = APPLICATIONS.get(application_id)
    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")

    return {**application, "audit_events": get_audit_events(application_id)}


@router.post("/applications/{application_id}/approve")
def approve_application(application_id: str, payload: ReviewDecisionRequest) -> dict:
    application = APPLICATIONS.get(application_id)
    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")

    previous_state = application["status"].value
    application["status"] = ApplicationStatus.APPROVED
    application["decision"] = "APPROVED_BY_REVIEWER"
    application["review_comment"] = payload.comment
    record_audit_event(
        application_id=application_id,
        actor_type="REVIEWER",
        action="APPROVE_APPLICATION",
        previous_state=previous_state,
        new_state=ApplicationStatus.APPROVED.value,
        payload={"comment": payload.comment},
    )

    return {"application_id": application_id, "status": ApplicationStatus.APPROVED}


@router.post("/applications/{application_id}/reject")
def reject_application(application_id: str, payload: ReviewDecisionRequest) -> dict:
    application = APPLICATIONS.get(application_id)
    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")

    previous_state = application["status"].value
    application["status"] = ApplicationStatus.REJECTED
    application["decision"] = "REJECTED_BY_REVIEWER"
    application["review_reason"] = payload.reason
    record_audit_event(
        application_id=application_id,
        actor_type="REVIEWER",
        action="REJECT_APPLICATION",
        previous_state=previous_state,
        new_state=ApplicationStatus.REJECTED.value,
        payload={"reason": payload.reason},
    )

    return {"application_id": application_id, "status": ApplicationStatus.REJECTED}


@router.post("/applications/{application_id}/request-info")
def request_more_information(application_id: str, payload: ReviewDecisionRequest) -> dict:
    application = APPLICATIONS.get(application_id)
    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")

    previous_state = application["status"].value
    application["status"] = ApplicationStatus.MORE_INFO_REQUIRED
    application["decision"] = "MORE_INFO_REQUESTED_BY_REVIEWER"
    application["review_comment"] = payload.comment
    record_audit_event(
        application_id=application_id,
        actor_type="REVIEWER",
        action="REQUEST_MORE_INFORMATION",
        previous_state=previous_state,
        new_state=ApplicationStatus.MORE_INFO_REQUIRED.value,
        payload={"comment": payload.comment},
    )

    return {"application_id": application_id, "status": ApplicationStatus.MORE_INFO_REQUIRED}
