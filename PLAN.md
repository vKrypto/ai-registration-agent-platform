# AI Registration Agent Platform - Project Plan

## 1. Project Objective

Build an AI-powered registration and approval platform for a business portal where users can register, upload required documents, and track approval status through a conversational assistant.

The system should reduce manual approval effort, shorten registration turnaround time, validate documents automatically, and route only risky or low-confidence cases to a human reviewer.

This project will use Azure AI Foundry, Azure OpenAI, Azure services, backend APIs, workflow orchestration, and a portal interface.

---

## 2. Core Business Problem

The current registration flow is manual and goes through many backend approval stages. Users upload identity and supporting documents such as Aadhaar, PAN, passport, bank letter, or business documents. Backend teams manually check document completeness, extract details, compare fields, validate against business rules, and approve or reject the application.

This creates four problems:

1. High manual effort for operations teams.
2. Slow registration turnaround time.
3. Inconsistent validation quality.
4. Poor user experience because users do not know what is missing or where the request is stuck.

The AI platform should automate predictable checks and keep humans only for exception cases.

---

## 3. Target Users

### 3.1 External Users

Users who come to the business portal to register and upload documents.

They need:

- Simple guidance on the registration process.
- Clear document checklist.
- Upload support.
- Missing document alerts.
- Registration status updates.

### 3.2 Internal Operations Users

Operations, compliance, and approval teams.

They need:

- Review queue for failed or risky cases.
- Extracted document fields.
- AI validation summary.
- Risk reasons.
- Manual approve, reject, or request-more-info actions.

### 3.3 Admin Users

System admins and business owners.

They need:

- Configure required documents.
- Configure validation rules.
- Monitor approval metrics.
- Audit user and agent actions.

---

## 4. High-Level Solution

The platform will have one user-facing conversational agent and multiple backend agents/services.

```text
User Portal
  -> Conversational Registration Agent
  -> Registration Backend API
  -> Workflow Orchestrator
  -> Document Intake Service
  -> OCR / Vision Extraction Service
  -> Document Validation Agent
  -> KYC / Verification Agent
  -> Compliance / Risk Agent
  -> Decision Engine
  -> Human Review Queue if needed
  -> Notification Service
```

The key design principle is simple: do not let the LLM own the final approval decision. The LLM should guide, summarize, reason over edge cases, and call tools. Final decisions should be controlled by deterministic services, rule engines, confidence thresholds, and human review where required.

---

## 5. Planned Features

### 5.1 User Portal Features

- User registration and login.
- Application creation.
- Document checklist display.
- Document upload.
- Chat-based registration guidance.
- Application status tracking.
- Missing document notifications.
- Request-more-info flow.
- Final approval or rejection status.

### 5.2 Conversational Agent Features

- Explain registration process.
- Answer only portal-specific questions.
- Ask user for missing details.
- Guide document upload step by step.
- Validate basic upload constraints such as file type and size.
- Call backend APIs for checklist, upload, and status.
- Refuse unrelated questions such as Gmail registration or external services.
- Escalate unclear user requests to human support or predefined fallback.

### 5.3 Document Processing Features

- Store uploaded files in Azure Blob Storage.
- Generate unique application ID.
- Classify uploaded document type.
- Extract text and structured fields.
- Validate document quality.
- Detect missing pages or unclear images.
- Match document fields with user-submitted profile.

### 5.4 Validation Features

- Name match across submitted form and documents.
- Date of birth match.
- Address match where applicable.
- PAN format validation.
- Aadhaar masked/unmasked policy validation.
- Passport expiry validation.
- Bank letter account holder validation.
- Duplicate application detection.
- Confidence score generation.

### 5.5 Approval Workflow Features

- Auto-approve low-risk applications.
- Auto-reject clearly invalid applications only if business permits.
- Route low-confidence or risky cases to manual review.
- Maintain audit trail for every decision.
- Allow reviewer to approve, reject, or request more information.

### 5.6 Admin Features

- Configure document checklist by registration type.
- Configure validation rules.
- Configure thresholds.
- View monitoring dashboard.
- View failed agent and tool calls.

---

## 6. Technology Stack

### 6.1 AI Platform

- Azure AI Foundry for model management, agent experiments, evaluation, tracing, and AI lifecycle management.
- Azure OpenAI for LLM calls.
- GPT-4o mini for cost-effective conversational interactions.
- GPT-4o or GPT-4.1 for complex reasoning and exception summaries.

### 6.2 Workflow Orchestration

Primary option:

- LangGraph for deterministic agent orchestration and state transitions.

Alternative option:

- Microsoft Agent Framework when Azure-native agent runtime is preferred.

Reasoning:

- Approval flow needs deterministic control, retries, audit, and state management.
- Pure prompt-flow style orchestration is not enough for production approval systems.
- Agent steps should be explicit and inspectable.

### 6.3 Backend

- Python.
- FastAPI.
- REST APIs.
- Async workers for long-running document processing.
- Pydantic for request and response validation.

### 6.4 Frontend

Recommended first implementation:

- React or Next.js portal.
- Login page.
- Registration dashboard.
- Document upload screen.
- Chat assistant panel.
- Reviewer dashboard.

### 6.5 Azure Services

- Azure AI Foundry.
- Azure OpenAI.
- Azure Blob Storage.
- Azure AI Vision OCR or Azure Document Intelligence depending on cost and accuracy needs.
- Azure Functions or Container Apps for worker tasks.
- Azure API Management for public API gateway.
- Azure Cosmos DB or Azure SQL for application metadata.
- Azure Key Vault for secrets.
- Azure Monitor and Application Insights for observability.
- Azure AI Search for registration-policy RAG if required.

### 6.6 Infrastructure and Deployment

- Terraform or Bicep for Azure infrastructure.
- GitHub Actions for CI/CD.
- Docker for backend packaging.
- Azure Container Apps for first production-friendly deployment.
- AKS only if enterprise scale, service mesh, or strict cluster-level control is required.

---

## 7. Agent Design

### 7.1 Conversational Registration Agent

Purpose:

- Talk to the user.
- Explain registration process.
- Collect required information.
- Guide document upload.
- Call backend APIs.
- Stay strictly within portal registration scope.

Allowed tools:

- Get document checklist.
- Create application.
- Upload document.
- Get application status.
- Request support.

Guardrails:

- Refuse unrelated topics.
- Never approve or reject application directly.
- Never expose internal validation rules fully.
- Never ask for unnecessary sensitive data.

### 7.2 Document Intake Agent / Service

Purpose:

- Receive uploaded files.
- Validate file type and size.
- Store files in Blob Storage.
- Link files to application ID.
- Trigger processing workflow.

### 7.3 Document Classification Agent / Service

Purpose:

- Identify uploaded document type.
- Detect if user uploaded the wrong document.
- Map document to checklist requirement.

Implementation options:

- Lightweight rules based on filename and user-selected type.
- GPT-4o mini vision for cheap classification.
- Azure AI Vision for OCR/classification.

### 7.4 OCR / Extraction Service

Purpose:

- Extract text and fields from uploaded documents.

Cost-optimized strategy:

- Use GPT-4o mini vision or Azure AI Vision for first-pass extraction.
- Use Azure Document Intelligence only for documents needing layout accuracy, confidence scores, or audit-grade structured output.
- Avoid sending every document to expensive extraction services by default.

### 7.5 Document Validation Agent / Service

Purpose:

- Validate extracted fields.
- Compare extracted values with user profile.
- Generate confidence score and validation result.

Checks:

- Document clarity.
- Required fields present.
- Expiry where applicable.
- Field-level mismatch.
- Duplicate or suspicious upload.

### 7.6 KYC / External Verification Agent

Purpose:

- Call internal or third-party KYC APIs.
- Validate PAN, Aadhaar, passport, bank details, or business identifiers where legally allowed.
- Return structured verification status.

### 7.7 Compliance / Risk Agent

Purpose:

- Evaluate business rules.
- Calculate risk score.
- Identify conditions requiring manual review.

This should be mostly rule-based. LLMs can summarize risk reasons, but should not silently invent compliance logic.

### 7.8 Decision Engine

Purpose:

- Decide next workflow state based on deterministic rules.

Possible outcomes:

- Approved.
- Rejected.
- Needs more information.
- Manual review required.

### 7.9 Notification Agent / Service

Purpose:

- Notify user via portal, email, SMS, or WhatsApp.
- Send missing document messages.
- Send final status updates.

---

## 8. Workflow States

```text
DRAFT
SUBMITTED
DOCUMENTS_UPLOADED
CLASSIFICATION_IN_PROGRESS
EXTRACTION_IN_PROGRESS
VALIDATION_IN_PROGRESS
EXTERNAL_VERIFICATION_IN_PROGRESS
RISK_REVIEW_IN_PROGRESS
MANUAL_REVIEW_REQUIRED
MORE_INFO_REQUIRED
APPROVED
REJECTED
CANCELLED
FAILED
```

Each state transition must be persisted with:

- Application ID.
- Previous state.
- New state.
- Actor type: user, agent, service, reviewer.
- Reason.
- Timestamp.
- Correlation ID.

---

## 9. Data Model - Initial Entities

### 9.1 User

- user_id
- full_name
- email
- phone
- auth_provider
- created_at
- updated_at

### 9.2 Application

- application_id
- user_id
- registration_type
- status
- risk_score
- confidence_score
- assigned_reviewer_id
- created_at
- updated_at

### 9.3 Document

- document_id
- application_id
- document_type
- blob_url
- file_name
- mime_type
- upload_status
- extraction_status
- validation_status
- created_at

### 9.4 ExtractedField

- field_id
- document_id
- field_name
- field_value
- confidence
- source_page
- created_at

### 9.5 ValidationResult

- validation_id
- application_id
- document_id
- rule_name
- result
- severity
- reason
- created_at

### 9.6 AuditEvent

- event_id
- application_id
- actor_type
- actor_id
- action
- payload
- created_at

---

## 10. API Design - Initial Endpoints

### 10.1 User and Application APIs

```http
POST /api/applications
GET /api/applications/{application_id}
GET /api/applications/{application_id}/status
```

### 10.2 Document APIs

```http
GET /api/applications/{application_id}/document-checklist
POST /api/applications/{application_id}/documents
GET /api/applications/{application_id}/documents
```

### 10.3 Agent APIs

```http
POST /api/agent/chat
POST /api/agent/tool/get-checklist
POST /api/agent/tool/create-application
POST /api/agent/tool/get-status
```

### 10.4 Reviewer APIs

```http
GET /api/reviewer/queue
GET /api/reviewer/applications/{application_id}
POST /api/reviewer/applications/{application_id}/approve
POST /api/reviewer/applications/{application_id}/reject
POST /api/reviewer/applications/{application_id}/request-info
```

### 10.5 Admin APIs

```http
GET /api/admin/rules
POST /api/admin/rules
GET /api/admin/metrics
```

---

## 11. Security Design

Security cannot be bolted on later. This project handles sensitive identity and financial documents, so the default design should assume regulated data.

### 11.1 Authentication

- Use portal login.
- JWT based session for frontend/backend.
- Azure Entra ID B2C or equivalent for production.

### 11.2 Authorization

- Role-based access control.
- Roles: user, reviewer, admin, service.
- Users can access only their own applications.
- Reviewers can access assigned or queued applications.
- Admins can configure rules but should not directly bypass audit.

### 11.3 Secrets

- Store all secrets in Azure Key Vault.
- No secrets in repository.
- No secrets in environment files committed to GitHub.

### 11.4 Storage Security

- Store documents in private Blob containers.
- Use short-lived SAS URLs only where needed.
- Encrypt at rest.
- Apply retention policies.

### 11.5 AI Safety

- Restrict agent scope through system prompt and tool permissions.
- Validate every tool call server-side.
- Log prompts, tool calls, and outputs with redaction for sensitive data.
- Add prompt injection checks for uploaded content.

---

## 12. Cost Optimization Strategy

Do not use the most expensive AI service for every step. That is how demo projects become budget bonfires.

### 12.1 Model Usage

- GPT-4o mini for normal chat guidance.
- GPT-4o mini or Azure AI Vision for basic document classification.
- Deterministic code for validation where possible.
- GPT-4o or GPT-4.1 only for complex exception summaries or ambiguous cases.

### 12.2 OCR Strategy

- Start with low-cost OCR or vision extraction.
- Escalate to Azure Document Intelligence only when layout accuracy, confidence scores, or audit-grade extraction is needed.
- Cache extraction results by document hash to avoid duplicate processing.

### 12.3 Backend Strategy

- Async processing for document workflows.
- Queue-based processing to avoid overloading services.
- Retry with backoff.
- Avoid repeated LLM calls for the same state.

---

## 13. Observability

### 13.1 Application Logs

- API request logs.
- Workflow state transition logs.
- Document processing logs.
- External API call logs.

### 13.2 AI Logs

- Prompt version.
- Model version.
- Token usage.
- Tool call name.
- Tool call latency.
- Agent output status.

### 13.3 Metrics

- Average registration completion time.
- Auto-approval rate.
- Manual review rate.
- Rejection rate.
- OCR failure rate.
- Validation mismatch rate.
- LLM cost per application.
- Average latency per workflow step.

---

## 14. Repository Structure

Planned structure:

```text
.
├── PLAN.md
├── README.md
├── docs
│   ├── ARCHITECTURE.md
│   ├── AGENT_DESIGN.md
│   ├── API_DESIGN.md
│   ├── DATA_MODEL.md
│   ├── DEPLOYMENT.md
│   ├── SECURITY.md
│   └── diagrams
├── backend
│   ├── app
│   ├── tests
│   ├── Dockerfile
│   └── requirements.txt
├── agents
│   ├── registration_agent
│   ├── workflow
│   └── prompts
├── frontend
│   └── portal
├── infra
│   ├── terraform
│   └── bicep
├── .github
│   └── workflows
└── scripts
```

---

## 15. Delivery Phases

### Phase 1 - Planning and Architecture

Deliverables:

- PLAN.md.
- README.md.
- Architecture document.
- Agent design document.
- API design document.
- Data model document.
- Security document.

### Phase 2 - Backend Skeleton

Deliverables:

- FastAPI project.
- Application APIs.
- Document APIs.
- Agent tool APIs.
- Mock persistence layer.
- Unit tests.

### Phase 3 - Agent Workflow

Deliverables:

- Conversational registration agent prompt.
- LangGraph workflow skeleton.
- Agent state schema.
- Tool calling layer.
- Mock tool implementations.

### Phase 4 - Document Processing

Deliverables:

- Document upload service.
- Blob abstraction.
- OCR abstraction.
- Validation pipeline.
- Mock extraction for local development.

### Phase 5 - Reviewer Workflow

Deliverables:

- Reviewer APIs.
- Review queue.
- Approval, rejection, request-more-info flow.
- Audit logging.

### Phase 6 - Infrastructure

Deliverables:

- Terraform skeleton.
- Azure resource modules.
- GitHub Actions pipeline.
- Docker build.
- Deployment documentation.

### Phase 7 - Frontend

Deliverables:

- Portal login placeholder.
- Registration dashboard.
- Document upload page.
- Chat assistant page.
- Reviewer dashboard.

### Phase 8 - Evaluation and Hardening

Deliverables:

- Prompt evaluation cases.
- Agent behavior test cases.
- Security checks.
- Cost monitoring plan.
- Production readiness checklist.

---

## 16. Acceptance Criteria

The project will be considered demo-ready when:

1. A user can create a registration application.
2. The assistant can explain required documents.
3. The user can upload documents.
4. The backend can classify and mock-extract document fields.
5. The workflow can validate documents using deterministic rules.
6. The decision engine can auto-route applications.
7. Manual review queue works for low-confidence cases.
8. Audit events are recorded.
9. README explains local setup.
10. Architecture documents explain production Azure deployment.

---

## 17. Immediate Next Steps

1. Create README.md.
2. Create docs/ARCHITECTURE.md.
3. Create docs/AGENT_DESIGN.md.
4. Create docs/API_DESIGN.md.
5. Create backend FastAPI skeleton.
6. Create LangGraph workflow skeleton.
7. Create mock portal UI structure.

---

## 18. Design Position

Azure AI Foundry should be used for AI lifecycle management, model operations, evaluations, tracing, and Azure OpenAI integration. It should not be treated as the entire application runtime.

Business workflow, approval state, retries, audit, authorization, and document lifecycle must live in backend services where they can be tested, versioned, and controlled.
