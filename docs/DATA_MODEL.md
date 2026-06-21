# Data Model

## Overview

The platform manages registration applications, uploaded documents, validation results, workflow states, reviewer actions, and audit history.

The data model is designed around traceability and workflow lifecycle management.

Every important action must be reconstructable from stored data.

---

# Database Strategy

## Primary Database

Recommended:

- Azure Cosmos DB

Reason:

- Flexible schema
- Fast iteration during MVP
- Horizontal scalability
- Native JSON documents

Alternative:

- Azure SQL when strict relational constraints become more important.

---

# Core Entities

```text
User
  |
Application
  |
+----------------+
|                |
Document     AuditEvent
|
ExtractedField
|
ValidationResult
```

---

# User Entity

Represents a portal user.

## Fields

```text
user_id
full_name
email
phone
auth_provider
status
created_at
updated_at
```

## Example

```json
{
  "user_id": "usr_001",
  "full_name": "John Smith",
  "email": "john@example.com",
  "phone": "+911234567890"
}
```

---

# Application Entity

Represents a registration request.

One user may own multiple applications.

## Fields

```text
application_id
user_id
registration_type
status
risk_score
confidence_score
assigned_reviewer_id
submitted_at
approved_at
rejected_at
created_at
updated_at
```

---

# Application Status Lifecycle

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

Every status transition generates an audit event.

---

# Document Entity

Represents a file uploaded by a user.

## Fields

```text
document_id
application_id
document_type
file_name
blob_url
mime_type
file_size
upload_status
extraction_status
validation_status
created_at
updated_at
```

## Supported Types

```text
PAN
AADHAAR
PASSPORT
BANK_LETTER
BUSINESS_REGISTRATION
ADDRESS_PROOF
OTHER
```

---

# Extracted Field Entity

Stores OCR-extracted values.

## Fields

```text
field_id
document_id
field_name
field_value
confidence
source_page
created_at
```

## Example

```json
{
  "field_name": "pan_number",
  "field_value": "ABCDE1234F",
  "confidence": 0.98
}
```

---

# Validation Result Entity

Stores rule evaluation results.

## Fields

```text
validation_id
application_id
document_id
rule_name
result
severity
reason
created_at
```

---

# Example Validation Results

```json
{
  "rule_name": "PAN_FORMAT_VALIDATION",
  "result": "PASS"
}
```

```json
{
  "rule_name": "NAME_MATCH",
  "result": "FAIL",
  "reason": "Submitted name differs from passport"
}
```

---

# Verification Result Entity

Stores external verification outcomes.

## Fields

```text
verification_id
application_id
verification_type
status
provider
response_reference
verified_at
```

---

# Risk Assessment Entity

Stores risk evaluation results.

## Fields

```text
risk_id
application_id
risk_score
risk_level
reason
created_at
```

## Risk Levels

```text
LOW
MEDIUM
HIGH
```

---

# Review Entity

Represents reviewer actions.

## Fields

```text
review_id
application_id
reviewer_id
action
comment
created_at
```

## Actions

```text
APPROVE
REJECT
REQUEST_INFO
```

---

# Audit Event Entity

Most important entity in the system.

Every important action creates an audit event.

## Fields

```text
event_id
application_id
actor_type
actor_id
action
previous_state
new_state
payload
correlation_id
created_at
```

---

# Actor Types

```text
USER
AGENT
SERVICE
REVIEWER
ADMIN
```

---

# Example Audit Event

```json
{
  "event_id": "evt_001",
  "actor_type": "USER",
  "action": "UPLOAD_DOCUMENT",
  "application_id": "app_001"
}
```

---

# Conversation Entity

Stores registration assistant conversations.

## Fields

```text
conversation_id
user_id
application_id
started_at
ended_at
```

---

# Conversation Message Entity

Stores chat history.

## Fields

```text
message_id
conversation_id
role
content
token_count
created_at
```

## Roles

```text
USER
ASSISTANT
TOOL
SYSTEM
```

---

# Agent Execution Entity

Tracks AI activity.

## Fields

```text
execution_id
agent_name
application_id
model_name
prompt_version
latency_ms
token_usage
status
created_at
```

---

# Entity Relationships

```text
User
 |
 +---- Application
         |
         +---- Document
         |       |
         |       +---- ExtractedField
         |       |
         |       +---- ValidationResult
         |
         +---- VerificationResult
         |
         +---- RiskAssessment
         |
         +---- Review
         |
         +---- AuditEvent
         |
         +---- Conversation
                 |
                 +---- ConversationMessage
```

---

# Partitioning Strategy

For Cosmos DB:

Recommended partition key:

```text
application_id
```

Reason:

Most operations are application-centric.

This minimizes cross-partition queries.

---

# Retention Strategy

Documents:

- Business-configurable retention period

Audit Events:

- Long-term retention

Conversations:

- Retention based on compliance requirements

Logs:

- Centralized monitoring retention policy

---

# Design Position

The application entity is the aggregate root of the system.

Every document, validation result, workflow action, reviewer decision, and audit event should be traceable back to a single application identifier.

This keeps the platform explainable, auditable, and easier to operate in production.