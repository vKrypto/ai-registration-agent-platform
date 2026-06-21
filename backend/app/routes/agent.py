from fastapi import APIRouter

from app.schemas import AgentChatRequest, AgentChatResponse

router = APIRouter()


@router.post("/chat", response_model=AgentChatResponse)
def chat(payload: AgentChatRequest) -> AgentChatResponse:
    # MVP stub. Replace with Azure OpenAI + LangGraph orchestration.
    normalized = payload.message.lower()

    if "gmail" in normalized or "instagram" in normalized or "facebook" in normalized:
        return AgentChatResponse(
            response="I can only help with registration on this business portal.",
            tool_calls=[],
            application_status=None,
        )

    if "document" in normalized or "required" in normalized:
        return AgentChatResponse(
            response="For individual registration, the required documents are PAN, Aadhaar, and bank letter.",
            tool_calls=["get_checklist"],
            application_status=None,
        )

    return AgentChatResponse(
        response="I can help you create an application, understand required documents, upload documents, and check registration status.",
        tool_calls=[],
        application_status=None,
    )
