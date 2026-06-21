variable "project_name" {
  description = "Project name used for Azure resource naming."
  type        = string
  default     = "ai-registration-agent"
}

variable "environment" {
  description = "Deployment environment."
  type        = string
  default     = "dev"
}

variable "location" {
  description = "Azure region."
  type        = string
  default     = "eastus"
}

variable "openai_model_name" {
  description = "Azure OpenAI model name for the default chat deployment."
  type        = string
  default     = "gpt-4o-mini"
}

variable "openai_model_version" {
  description = "Azure OpenAI model version. Confirm availability in the selected region before applying."
  type        = string
  default     = "2024-07-18"
}

variable "openai_deployment_capacity" {
  description = "Azure OpenAI deployment capacity. Keep small for dev."
  type        = number
  default     = 10
}

variable "tags" {
  description = "Common resource tags."
  type        = map(string)
  default = {
    project = "ai-registration-agent-platform"
  }
}
