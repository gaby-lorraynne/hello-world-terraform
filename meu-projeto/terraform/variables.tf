//Definindo regiao
variable "region" {
  type        = string
  //Regiao de SP
  default = "sa-east-1"
}

//Definando o perfil
variable "profile" {
  type        = string
  description = "AWS CLI perfil"
  default = "default"
}


//Definindo nome function lambda
variable "function_name" {
  type        = string
  description = "Funcao lambda"
  default = "funcao-um"
}

//Chamar a funcao
variable "handler" {
  type = string
  description = "Handler da funcao"
  default = "com.example.FuncaoUmHandler::handleRequest"
}

//Tempo de execucao da minha funcao
variable "runtime" {
  type        = string
  description = "Tempo execucao da funcao Lambda"
  default = "java21"
}

//Tamanho da memoria
variable "memory_size" {
  type = number
  description = "Quantidade de armazenamento"
  default = 512
}

//Limite de tempo
variable "timeout" {
  type = number
  description = "Tempo de esgotamento"
  default = 10
}

variable "lambda_role_arn" {
  type        = string
  description = "IAM Role ARN to attach to the Lambda"
  default = ""
}

//Criar funcao para a lambda
variable "create_role" {
  type = bool
  description = "Criar uma nova funcao"
  default = true
}