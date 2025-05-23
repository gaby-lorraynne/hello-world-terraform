variable "user_pool_name" {
  description = "Nome do User Pool do Cognito"
  type        = string
}

variable "client_name" {
  description = "Nome do Client do User Pool"
  type        = string
}

# Configurações de senha
variable "password_minimum_length" {
  description = "Comprimento mínimo da senha"
  type        = number
  default     = 8
}

variable "password_require_lowercase" {
  description = "Exigir caracteres minúsculos na senha"
  type        = bool
  default     = true
}

variable "password_require_numbers" {
  description = "Exigir números na senha"
  type        = bool
  default     = true
}

variable "password_require_symbols" {
  description = "Exigir símbolos na senha"
  type        = bool
  default     = true
}

variable "password_require_uppercase" {
  description = "Exigir caracteres maiúsculos na senha"
  type        = bool
  default     = true
}

# Configurações MFA
variable "mfa_configuration" {
  description = "Configuração MFA: OFF, OPTIONAL ou REQUIRED"
  type        = string
  default     = "OPTIONAL"

  validation {
    condition     = contains(["OFF", "OPTIONAL", "REQUIRED"], var.mfa_configuration)
    error_message = "O valor de mfa_configuration deve ser um dos seguintes: OFF, OPTIONAL ou REQUIRED."
  }
}

# Configurações do Client
variable "generate_client_secret" {
  description = "Gerar segredo para o client"
  type        = bool
  default     = false
}

variable "refresh_token_validity" {
  description = "Validade do refresh token em dias"
  type        = number
  default     = 30
}

variable "access_token_validity" {
  description = "Validade do access token em minutos"
  type        = number
  default     = 60
}

variable "id_token_validity" {
  description = "Validade do ID token em minutos"
  type        = number
  default     = 60
}

# Tags
variable "tags" {
  description = "Tags para os recursos criados"
  type        = map(string)
  default     = {}
}