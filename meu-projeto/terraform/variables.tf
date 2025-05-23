//Definindo regiao
variable "region" {
  type = string
  //Regiao de SP
  default = "sa-east-1"
}

//Definando o perfil
variable "profile" {
  type        = string
  description = "AWS CLI perfil"
  default     = "default"
}


//Definindo nome function lambda
variable "function_name" {
  type        = string
  description = "Funcao lambda"
  default     = "hello_terraform"
}

//Chamar a funcao
variable "handler" {
  type        = string
  description = "Handler da funcao"
  default     = "hello_terraform.lambda_handler"
}

//Tempo de execucao da minha funcao
variable "runtime" {
  type        = string
  description = "Tempo execucao da funcao Lambda"
  default     = "python3.12"
}

//Tamanho da memoria
variable "memory_size" {
  type        = number
  description = "Quantidade de armazenamento"
  default     = 512
}

//Limite de tempo
variable "timeout" {
  type        = number
  description = "Tempo de esgotamento"
  default     = 10
}

variable "lambda_role_arn" {
  type        = string
  description = "IAM Role ARN to attach to the Lambda"
  default     = ""
}

//Criar funcao para a lambda
variable "create_role" {
  type        = bool
  description = "Criar uma nova funcao"
  default     = true
}

//Nome da tabela
variable "TABLE_NAME" {
  description = "Nome da tabela"
  type        = string
  default     = "ListaMercado"
}

variable "http_method" {
  description = "Método HTTP"
  type        = string
  default     = "GET"
}

variable "value_path" {
  description = "Caminho do recurso"
  type        = string
  default     = "hello"
}


// variaveis do Cognito

variable "cognito_user_pool_name" {
  description = "Nome do User Pool do Cognito"
  type        = string
  default     = "Auth-UserPool"
}

variable "cognito_client_name" {
  description = "Nome do Client do User Pool"
  type        = string
  default     = "auth-client"
}

// Configurações de senha
variable "cognito_password_minimum_length" {
  description = "Comprimento mínimo da senha"
  type        = number
  default     = 8
}

variable "cognito_password_require_lowercase" {
  description = "Exigir caracteres minúsculos na senha"
  type        = bool
  default     = true
}

variable "cognito_password_require_numbers" {
  description = "Exigir números na senha"
  type        = bool
  default     = true
}

variable "cognito_password_require_symbols" {
  description = "Exigir símbolos na senha"
  type        = bool
  default     = true
}

variable "cognito_password_require_uppercase" {
  description = "Exigir caracteres maiúsculos na senha"
  type        = bool
  default     = true
}

// Configuração MFA
variable "cognito_mfa_configuration" {
  description = "Configuração MFA: OFF, OPTIONAL ou REQUIRED"
  type        = string
  default     = "OFF"
}

// Configurações do Client
variable "cognito_generate_client_secret" {
  description = "Gerar segredo para o client"
  type        = bool
  default     = false
}

variable "cognito_refresh_token_validity" {
  description = "Validade do refresh token em dias"
  type        = number
  default     = 30
}

variable "cognito_access_token_validity" {
  description = "Validade do access token em minutos"
  type        = number
  default     = 60
}

variable "cognito_id_token_validity" {
  description = "Validade do ID token em minutos"
  type        = number
  default     = 60
}