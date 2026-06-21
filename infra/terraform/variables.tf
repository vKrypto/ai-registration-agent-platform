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

variable "tags" {
  description = "Common resource tags."
  type        = map(string)
  default = {
    project = "ai-registration-agent-platform"
  }
}
