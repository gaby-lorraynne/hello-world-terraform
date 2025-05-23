variable "user_pool_name" {
  description = "Nome do User Pool do Cognito existente"
  type        = string
}

variable "value_path" {
  description = "Valor do path para o recurso da API"
  type        = string
}

variable "http_method" {
  description = "Método HTTP para o recurso da API"
  type        = string
}

variable "function_name" {
  description = "Nome da função Lambda"
  type        = string
}

variable "lambda_invoke_arn" {
  description = "ARN da função Lambda"
  type        = string
}