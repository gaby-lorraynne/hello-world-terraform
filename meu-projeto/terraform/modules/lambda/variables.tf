# variables.tf
variable "function_name" {
  description = "Nome da função Lambda"
  type        = string
}

variable "handler" {
  description = "Handler da função Lambda"
  type        = string
}

variable "runtime" {
  description = "Runtime da função Lambda"
  type        = string
}

variable "role_arn" {
  description = "ARN da role IAM para a Lambda"
  type        = string
}

variable "memory_size" {
  description = "Tamanho da memória em MB"
  type        = number
  default     = 512
}

variable "timeout" {
  description = "Timeout em segundos"
  type        = number
  default     = 10
}

variable "http_method" {
  description = "Método HTTP"
  type        = string
}

variable "value_path" {
  description = "Path do recurso"
  type        = string
}

variable "table_name" {
  description = "Nome da tabela DynamoDB"
  type        = string
}
