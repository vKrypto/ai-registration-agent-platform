output "resource_group_name" {
  description = "Azure resource group name."
  value       = azurerm_resource_group.main.name
}

output "storage_account_name" {
  description = "Storage account used for uploaded documents."
  value       = azurerm_storage_account.documents.name
}

output "document_container_name" {
  description = "Private blob container for uploaded documents."
  value       = azurerm_storage_container.documents.name
}

output "key_vault_name" {
  description = "Key Vault name."
  value       = azurerm_key_vault.main.name
}

output "azure_openai_account_name" {
  description = "Azure OpenAI account name."
  value       = azurerm_cognitive_account.openai.name
}

output "azure_openai_endpoint" {
  description = "Azure OpenAI endpoint."
  value       = azurerm_cognitive_account.openai.endpoint
}

output "azure_openai_chat_deployment_name" {
  description = "Default Azure OpenAI chat deployment name."
  value       = azurerm_cognitive_deployment.chat.name
}

output "cosmosdb_account_name" {
  description = "Cosmos DB account name."
  value       = azurerm_cosmosdb_account.main.name
}
