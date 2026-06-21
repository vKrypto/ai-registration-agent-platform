# API Design

## Overview

This document defines the API contract for the AI Registration Agent Platform.

The APIs support four main consumers:

1. Portal frontend
2. Conversational registration agent
3. Reviewer dashboard
4. Admin and operations tooling

The API layer must remain deterministic, secure, and auditable. Agents may call APIs as tools, but APIs must validate every request independently.

---

# API Design Principles

## 1. Agent Tools Are Just APIs

Agent tools should map to backend APIs.

The LLM should not bypass backend validation.

## 2. Never Trust Agent Output

Every request from an agent must be treated like any other external request.

Validate:

- User identity
- Application ownership
- Request payload
- Authorization
- Business rule constraints

## 3. Use Explicit State Transitions

Avoid generic update endpoints for workflow state.

Prefer explicit operations:

- submit application
- request more information
- approve application
- reject application

## 4. Audit Every Sensitive Operation

Every mutation must produce an audit event.

---

# Base URL

```http
/api/v1
```

---

# Authentication

## User Authentication

Recommended:

- JWT bearer token
- Azure Entra ID B2C for production

```http
Authorization: Bearer <token>
```

## Service Authentication

Recommended:

- Managed identity
- Client credentials for internal services
- API Management subscription policies where needed

---

# Common Response Format

## Success

```json
{
  "success": true,
  "data": {},
  "correlation_id": "req_123"
}
```

## Error

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Document type is required",
    "details": []
  },
  "correlation_id": "req_123"
}
```

---

# Error Codes

| Code | Meaning |
|---|---|
| VALIDATION_ERROR | Invalid request payload |
| UNAUTHORIZED | User is not authenticated |
| FORBIDDEN | User does not have permission |
| NOT_FOUND | Resource not found |
| CONFLICT | Invalid state transition |
| RATE_LIMITED | Too many requests |
| PROCESSING_FAILED | Backend processing failed |
| AGENT_TOOL_DENIED | Agent attempted unsupported operation |

---

# Application APIs

## Create Application

```http
POST /api/v1/applications
```

### Request

```json
{
  "registration_type": "individual",
  "full_name": "John Smith",
  "email": "john@example.com",
  "phone": "+911234567890"
}
```

### Response

```json
{
  "application_id": "app_123",
  "status": "DRAFT",
  "required_documents": ["PAN", "AADHAAR", "BANK_LETTER"]
}
```

---

## Get Application

```http
GET /api/v1/applications/{application_id}
```

Returns application metadata, current status, required documents, uploaded documents, and high-level validation status.

---

## Submit Application

```http
POST /api/v1/applications/{application_id}/submit
```

This moves the application from DRAFT to SUBMITTED if mandatory fields and required uploads exist.

---

## Get Application Status

```http
GET /api/v1/applications/{application_id}/status
```

### Response

```json
{
  "application_id": "app_123",
  "status": "VALIDATION_IN_PROGRESS",
  "message": "Your documents are being validated.",
  "next_action_required": false
}
```

---

# Document APIs

## Get Document Checklist

```http
GET /api/v1/applications/{application_id}/document-checklist
```

### Response

```json
{
  "application_id": "app_123",
  "documents": [
    {
      "type": "PAN",
      "required": true,
      "uploaded": false,
      "allowed_formats": ["pdf", "jpg", "png"],
      "max_size_mb": 10
    }
  ]
}
```

---

## Upload Document

```http
POST /api/v1/applications/{application_id}/documents
```

Content type:

```http
multipart/form-data
```

Fields:

- document_type
- file

### Response

```json
{
  "document_id": "doc_123",
  "application_id": "app_123",
  "document_type": "PAN",
  "upload_status": "UPLOADED"
}
```

---

## List Documents

```http
GET /api/v1/applications/{application_id}/documents
```

---

## Get Document Validation Result

```http
GET /api/v1/applications/{application_id}/documents/{document_id}/validation
```

---

# Agent Tool APIs

These APIs are exposed as tools to the conversational registration agent.

## Agent Chat

```http
POST /api/v1/agent/chat
```

### Request

```json
{
  "conversation_id": "conv_123",
  "application_id": "app_123",
  "message": "What documents do I need?"
}
```

### Response

```json
{
  "response": "You need PAN, Aadhaar, and bank letter for this registration.",
  "tool_calls": [],
  "application_status": "DRAFT"
}
```

---

## Tool: Create Application

```http
POST /api/v1/agent/tools/create-application
```

Used by the registration agent after collecting required user details.

---

## Tool: Get Checklist

```http
POST /api/v1/agent/tools/get-checklist
```

Used by the registration agent to answer checklist questions.

---

## Tool: Get Status

```http
POST /api/v1/agent/tools/get-status
```

Used by the registration agent to answer application status questions.

---

# Workflow APIs

Workflow APIs are mostly internal.

## Trigger Workflow

```http
POST /api/v1/internal/workflows/applications/{application_id}/start
```

## Get Workflow State

```http
GET /api/v1/internal/workflows/applications/{application_id}
```

## Retry Workflow Step

```http
POST /api/v1/internal/workflows/applications/{application_id}/steps/{step_id}/retry
```

---

# Reviewer APIs

## Get Review Queue

```http
GET /api/v1/reviewer/queue
```

### Response

```json
{
  "items": [
    {
      "application_id": "app_123",
      "status": "MANUAL_REVIEW_REQUIRED",
      "risk_score": 72,
      "reason": "Name mismatch between PAN and submitted profile"
    }
  ]
}
```

---

## Get Review Details

```http
GET /api/v1/reviewer/applications/{application_id}
```

Returns:

- Application details
- Uploaded documents
- Extracted fields
- Validation results
- Risk summary
- Audit history

---

## Approve Application

```http
POST /api/v1/reviewer/applications/{application_id}/approve
```

### Request

```json
{
  "comment": "Documents verified manually."
}
```

---

## Reject Application

```http
POST /api/v1/reviewer/applications/{application_id}/reject
```

### Request

```json
{
  "reason": "Invalid PAN document"
}
```

---

## Request More Information

```http
POST /api/v1/reviewer/applications/{application_id}/request-info
```

### Request

```json
{
  "message": "Please upload a clearer bank letter."
}
```

---

# Admin APIs

## Get Rules

```http
GET /api/v1/admin/rules
```

## Create Rule

```http
POST /api/v1/admin/rules
```

## Get Metrics

```http
GET /api/v1/admin/metrics
```

---

# Eventing Strategy

For async processing use events.

Recommended events:

- application.created
- document.uploaded
- document.extraction.started
- document.extraction.completed
- validation.completed
- risk.completed
- review.required
- application.approved
- application.rejected

---

# Idempotency

Mutation endpoints should support idempotency keys.

```http
Idempotency-Key: <uuid>
```

Required for:

- Create application
- Upload document
- Submit application
- Reviewer decisions

---

# Rate Limits

Suggested limits:

- Agent chat: 30 requests per minute per user
- Upload document: 10 uploads per application per hour
- Status check: 60 requests per minute per user

---

# Security Rules

- Users can only access their own applications.
- Agents can only call allowlisted tool APIs.
- Reviewers can only access review queue data.
- Admin APIs require elevated role.
- Internal workflow APIs must not be publicly exposed.

---

# Design Position

The API layer is the control boundary.

The conversational agent can guide users, but the backend decides what is allowed, what state transition is valid, and what must be audited.