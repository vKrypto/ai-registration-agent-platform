# Deployment Design

## Overview

This document defines how the AI Registration Agent Platform should be deployed across local, MVP, and production environments.

The deployment approach should support incremental delivery. Start simple, keep it observable, and avoid over-engineering before the workflow is proven.

---

# Deployment Goals

1. Provide a simple local development setup.
2. Support a cost-effective MVP deployment.
3. Keep production architecture secure and scalable.
4. Use infrastructure as code.
5. Automate build and deployment with CI/CD.
6. Keep secrets outside the repository.

---

# Environments

## Local

Used by developers.

Components:

- FastAPI backend
- Mock database
- Mock storage
- Mock OCR
- Local LangGraph workflow

## Development

Used for early Azure integration.

Components:

- Azure OpenAI
- Azure Blob Storage
- Cosmos DB dev account
- Container Apps or App Service

## Staging

Used for release validation.

Components:

- Production-like Azure resources
- Real AI services
- Test KYC providers
- Restricted test data

## Production

Used by real users and reviewers.

Components:

- Private storage
- Production database
- Monitoring
- RBAC
- Key Vault
- API Management

---

# MVP Deployment Architecture

```text
GitHub
  |
GitHub Actions
  |
Azure Container Apps
  |
FastAPI Backend
  |
+----------------------+
| Azure OpenAI         |
| Azure Blob Storage   |
| Azure Cosmos DB      |
| Azure Key Vault      |
| Azure Monitor        |
+----------------------+
```

This is enough for the first working demo.

Do not start with AKS unless there is a real need. Kubernetes is not a personality trait.

---

# Production Deployment Architecture

```text
User
  |
Azure Front Door / App Gateway
  |
Frontend Portal
  |
Azure API Management
  |
Backend API
  |
Workflow Workers
  |
+-------------------------+
| Azure OpenAI            |
| Azure AI Foundry        |
| Azure Blob Storage      |
| Azure Cosmos DB         |
| Azure Key Vault         |
| Azure Monitor           |
| Azure AI Search         |
+-------------------------+
```

---

# Azure Services

## Azure AI Foundry

Used for:

- Model lifecycle management
- Evaluation
- Prompt testing
- Tracing
- Responsible AI workflows

## Azure OpenAI

Used for:

- Registration assistant
- Document reasoning
- Exception summarization

Recommended models:

- GPT-4o Mini for regular conversations
- GPT-4o or GPT-4.1 for complex reasoning

## Azure Blob Storage

Used for:

- Uploaded documents
- Temporary processing files

Security:

- Private containers
- No public blob access
- Short-lived SAS only if required

## Azure Cosmos DB

Used for:

- Applications
- Documents
- Audit events
- Conversations
- Workflow state

## Azure Key Vault

Used for:

- API keys
- Database secrets
- External provider credentials
- Signing secrets

## Azure Monitor and Application Insights

Used for:

- Logs
- Metrics
- Traces
- Alerts

## Azure API Management

Used for:

- API gateway
- Throttling
- Authentication policies
- Public API protection

---

# Infrastructure as Code

Recommended:

- Terraform

Alternative:

- Bicep

Terraform modules planned:

```text
infra/terraform
├── main.tf
├── variables.tf
├── outputs.tf
├── providers.tf
├── modules
│   ├── resource-group
│   ├── openai
│   ├── storage
│   ├── cosmosdb
│   ├── keyvault
│   ├── container-apps
│   └── monitoring
```

---

# CI/CD Strategy

Use GitHub Actions.

## Pipeline Stages

```text
Checkout
  |
Lint
  |
Test
  |
Build Docker Image
  |
Push Image
  |
Terraform Plan
  |
Terraform Apply
  |
Deploy App
```

---

# Deployment Flow

## Backend Deployment

1. Build Docker image.
2. Push image to registry.
3. Deploy to Azure Container Apps.
4. Inject secrets from Key Vault.
5. Run health check.

## Infrastructure Deployment

1. Run terraform fmt.
2. Run terraform validate.
3. Run terraform plan.
4. Manual approval for production.
5. Run terraform apply.

---

# Environment Variables

Expected variables:

```text
AZURE_OPENAI_ENDPOINT
AZURE_OPENAI_API_VERSION
AZURE_OPENAI_DEPLOYMENT_NAME
COSMOS_DB_ENDPOINT
BLOB_STORAGE_ACCOUNT
KEY_VAULT_URL
APP_ENV
LOG_LEVEL
```

Do not commit real values.

Use `.env.example` only.

---

# Secrets Strategy

Local:

- `.env` file ignored by Git

Azure:

- Key Vault
- Managed Identity

GitHub Actions:

- GitHub environment secrets
- OIDC federation preferred over long-lived Azure credentials

---

# Container Strategy

Backend should run as a Docker container.

Planned file:

```text
backend/Dockerfile
```

Runtime:

```text
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

# Health Checks

Required endpoints:

```http
GET /health
GET /ready
```

Health should validate:

- API is running

Readiness should validate:

- Database reachable
- Storage reachable
- Key Vault reachable

---

# Rollback Strategy

MVP:

- Redeploy previous container image

Production:

- Blue-green deployment or revision rollback
- Database migrations must be backward compatible

---

# Observability

Capture:

- API latency
- Workflow failures
- OCR failures
- Agent token usage
- LLM cost per application
- Approval turnaround time
- Manual review rate

---

# Cost Control

Cost controls:

- Use GPT-4o Mini for normal chat
- Use expensive extraction only when required
- Cache OCR outputs
- Rate-limit chat endpoint
- Avoid repeated processing for the same document hash

---

# Production Readiness Checklist

- Terraform state configured
- Key Vault enabled
- Managed Identity configured
- Blob public access disabled
- API Management configured
- Monitoring enabled
- Alerts configured
- CI/CD pipeline tested
- Health checks configured
- Secrets removed from repo
- Load test completed
- Prompt injection tests completed

---

# Design Position

Start with Azure Container Apps, not AKS.

AKS should only be introduced when the platform needs advanced networking, service mesh, heavy workload isolation, or enterprise cluster governance.

For this project, the correct early move is simple, secure, observable deployment.