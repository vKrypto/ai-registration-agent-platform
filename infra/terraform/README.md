# Terraform Infrastructure

This folder contains the initial Azure infrastructure skeleton for the AI Registration Agent Platform.

## Current Resources

- Resource Group
- Storage Account
- Private Blob Container for documents
- Key Vault
- Cosmos DB Account
- Cosmos DB SQL Database

## Usage

```bash
cd infra/terraform
terraform init
terraform fmt
terraform validate
terraform plan -var-file=dev.tfvars
terraform apply -var-file=dev.tfvars
```

Copy the example variables file before use:

```bash
cp dev.tfvars.example dev.tfvars
```

Do not commit real `*.tfvars` files containing environment-specific or sensitive values.

## Design Notes

This is an MVP infrastructure baseline. Azure OpenAI, Azure AI Foundry, Container Apps, API Management, and monitoring modules will be added incrementally.
