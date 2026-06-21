# Agent Design

## Overview

This platform uses a hybrid architecture.

AI agents are responsible for understanding, reasoning, summarization, classification, and user interaction.

Business services are responsible for approvals, validation rules, state management, auditing, and compliance.

The design intentionally avoids allowing LLMs to make final business decisions.

---

# Agent Architecture

```text
User
  |
Registration Agent
  |
Workflow Orchestrator
  |
+-----------------------------+
| Document Agent             |
| OCR Agent                  |
| Validation Agent           |
| Risk Agent                 |
| Notification Agent         |
+-----------------------------+
  |
Decision Engine
```

---

# Why Multiple Agents

A single large agent becomes difficult to control, audit, and scale.

Separating responsibilities provides:

- Better maintainability
- Lower cost
- Better observability
- Easier testing
- Reduced hallucination risk
- Clear ownership boundaries

---

# Agent 1 - Registration Agent

## Business Purpose

Acts as the front desk representative of the platform.

The user should never directly interact with backend workflows.

The registration agent becomes the primary interface.

## Responsibilities

- Explain registration process
- Explain required documents
- Create application
- Guide uploads
- Answer portal-specific questions
- Show application status

## Not Allowed

- Approval decisions
- Compliance decisions
- Direct database updates
- Access to internal reviewer notes

## Model

GPT-4o Mini

## Tools

- create_application
- get_checklist
- upload_document
- get_status
- request_support

---

# Agent 2 - Document Agent

## Business Purpose

Ensure uploaded files satisfy document requirements.

## Responsibilities

- Accept uploads
- Validate file type
- Validate file size
- Validate upload completeness
- Link files to application

## Inputs

- Application ID
- Uploaded file

## Outputs

- Document metadata
- Storage location

---

# Agent 3 - OCR Agent

## Business Purpose

Convert uploaded documents into structured information.

## Responsibilities

- OCR processing
- Field extraction
- Layout analysis
- Confidence generation

## Inputs

- Document

## Outputs

- Name
- Date of Birth
- Address
- PAN Number
- Passport Number
- Other extracted fields

## Implementation Strategy

Level 1:

- GPT-4o Mini Vision
- Azure AI Vision

Level 2:

- Azure Document Intelligence

Only escalate expensive processing when required.

---

# Agent 4 - Validation Agent

## Business Purpose

Verify extracted information.

## Responsibilities

- Field validation
- Identity matching
- Format validation
- Completeness validation

## Example Checks

Name Match

Submitted Form:

John Smith

Passport:

John A Smith

Result:

Partial Match

Confidence:

92%

---

# Agent 5 - Risk Agent

## Business Purpose

Identify risky applications.

## Responsibilities

- Risk scoring
- Suspicious activity detection
- Escalation recommendations

## Example Signals

- Multiple applications
- Document mismatch
- Expired documents
- Missing mandatory documents
- Failed verification

## Output

Risk Score

Example:

0-30
Low Risk

31-70
Medium Risk

71-100
High Risk

---

# Agent 6 - Notification Agent

## Business Purpose

Keep users informed.

## Responsibilities

- Missing document alerts
- Status updates
- Approval notifications
- Rejection notifications

## Channels

- Portal
- Email
- SMS
- WhatsApp

---

# Decision Engine

## Business Purpose

Convert agent outputs into workflow decisions.

This is intentionally not an LLM.

## Inputs

- Validation results
- Risk score
- Verification status

## Outcomes

- Approved
- Rejected
- More Information Required
- Manual Review Required

---

# Workflow Orchestration

## Recommended Technology

LangGraph

## Reason

Registration workflows require:

- Deterministic execution
- State management
- Retry handling
- Human-in-the-loop support

---

# LangGraph Flow

```text
START
  |
Create Application
  |
Document Upload
  |
Classification
  |
OCR
  |
Validation
  |
Risk Analysis
  |
Decision
  |
END
```

---

# State Schema

## Application State

```python
application_id
user_id
status
risk_score
confidence_score
required_documents
uploaded_documents
validation_results
verification_results
review_status
```

---

# Agent Communication Pattern

Agents should not directly call each other.

Recommended pattern:

```text
Agent
  |
Workflow Orchestrator
  |
Next Agent
```

Benefits:

- Traceability
- Retry support
- Easier debugging
- Better governance

---

# Tool Calling Strategy

Every tool call must be:

- Authenticated
- Authorized
- Audited
- Logged

Agent output should never directly trigger sensitive actions.

Backend validation is mandatory.

---

# Human Review Flow

Cases routed for review:

- Low confidence extraction
- Failed validation
- High risk score
- Missing documents
- Compliance exceptions

Reviewer Actions:

- Approve
- Reject
- Request Information

---

# Observability

For every agent execution capture:

- Prompt version
- Model version
- Input
- Output
- Tool calls
- Token usage
- Latency
- Errors

---

# Design Position

The registration agent is intentionally simple.

Complex business logic should remain in backend services and workflow orchestration layers.

This keeps the system predictable, auditable, scalable, and easier to maintain in production.