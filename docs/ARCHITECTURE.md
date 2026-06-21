# System Architecture

## Overview

The AI Registration Agent Platform is designed as a modular, enterprise-grade registration and approval system.

The architecture separates AI responsibilities from business workflow responsibilities.

AI components assist with guidance, extraction, classification, and reasoning.
Business services remain responsible for approvals, state management, auditing, and compliance.

---

# Architecture Principles

## Principle 1

LLMs never directly approve applications.

## Principle 2

All workflow state transitions are deterministic and auditable.

## Principle 3

Every AI action is observable and traceable.

## Principle 4

Business rules remain outside prompts.

## Principle 5

Human reviewers handle exceptions.

---

# High Level Architecture

```text
User Portal
    |
    v
Registration Agent
    |
    v
API Layer
    |
    v
Workflow Orchestrator
    |
    +-------------------+
    |                   |
    v                   v
Document Pipeline    Validation Pipeline
    |                   |
    +---------+---------+
              |
              v
       Decision Engine
              |
      +-------+-------+
      |               |
      v               v
 Auto Approval   Human Review
      |
      v
 Notification Service
```

---

# Azure Architecture

```text
Frontend Portal
        |
Azure API Management
        |
FastAPI Backend
        |
LangGraph Workflow Engine
        |
+------------------------------+
| Azure OpenAI                 |
| Azure AI Foundry            |
| Azure Blob Storage          |
| Azure Cosmos DB             |
| Azure Key Vault             |
| Azure Monitor               |
+------------------------------+
```

---

# Core Components

## Portal Layer

Responsibilities:

- Login
- Registration
- Upload documents
- Application tracking
- Chat assistant access

Recommended Stack:

- Next.js
- React
- Tailwind

---

## Registration Agent

Responsibilities:

- Explain registration process
- Provide document checklist
- Collect information
- Call backend tools
- Track status

Model:

- GPT-4o Mini

Tool Access:

- Create application
- Get checklist
- Upload document
- Check status

---

## Workflow Orchestrator

Responsibilities:

- State transitions
- Retry handling
- Agent coordination
- Routing
- Audit generation

Recommended:

- LangGraph

Reason:

Approval workflows require deterministic execution.

---

## Document Processing Pipeline

Responsibilities:

- Store uploads
- OCR
- Classification
- Metadata generation

Components:

- Blob Storage
- OCR Service
- Extraction Service

---

## Validation Pipeline

Responsibilities:

- Field validation
- Identity matching
- Duplicate detection
- Confidence calculation

Implementation:

- Mostly deterministic rules
- Minimal LLM usage

---

## Decision Engine

Possible Outcomes:

- Approved
- Rejected
- Manual Review
- More Information Required

Decision engine should be rule-based.

---

## Human Review Module

Responsibilities:

- Review exceptions
- Override outcomes
- Request information
- Record audit trail

---

# Data Flow

## Registration Flow

1. User creates application.
2. Application ID generated.
3. Document checklist returned.
4. User uploads documents.
5. Documents stored in Blob Storage.
6. Workflow triggered.
7. Classification executed.
8. OCR executed.
9. Validation executed.
10. Risk evaluation executed.
11. Decision engine executed.
12. Approval or review routing.
13. User notified.

---

# State Machine

```text
DRAFT
SUBMITTED
DOCUMENTS_UPLOADED
CLASSIFICATION_IN_PROGRESS
EXTRACTION_IN_PROGRESS
VALIDATION_IN_PROGRESS
RISK_REVIEW_IN_PROGRESS
MANUAL_REVIEW_REQUIRED
MORE_INFO_REQUIRED
APPROVED
REJECTED
```

Every transition must be persisted.

---

# Production Deployment

## Recommended

Frontend:

- Azure Static Web Apps

Backend:

- Azure Container Apps

Storage:

- Azure Blob Storage

Database:

- Azure Cosmos DB

Secrets:

- Azure Key Vault

Monitoring:

- Azure Monitor
- Application Insights

---

# Observability

Capture:

- Prompt versions
- Tool calls
- Latency
- Token consumption
- Workflow transitions
- Approval decisions
- Failures

---

# Scalability Strategy

MVP:

- Single backend deployment
- Container Apps
- Cosmos DB

Production:

- Horizontal scaling
- Queue-based processing
- Background workers
- Multi-region deployment

---

# Design Position

Azure AI Foundry is used for model lifecycle management, evaluation, tracing, and AI governance.

Business workflow ownership remains in backend services where deterministic execution, auditing, and compliance controls can be enforced.