terraform {
  backend "s3" {
    bucket = "bucket-terraform-gaby"
    key    = "dev/terraform.tfstate"
    region = "sa-east-1"
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

//Verificar se existe a Role ou nao
resource "aws_iam_role" "lambda_role" {
  count = var.create_role ? 1 : 0

  name = "${var.function_name}-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
    }]
  })
}

//Atachar Politica do lambda
resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  count      = var.create_role ? 1 : 0
  role       = aws_iam_role.lambda_role[0].name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

module "hello_terraform" {
  source = "./modules/lambda"

  function_name = var.function_name
  handler       = var.handler
  runtime       = var.runtime
  memory_size   = var.memory_size
  timeout       = var.timeout
  role_arn      = var.create_role ? aws_iam_role.lambda_role[0].arn : var.lambda_role_arn
  http_method   = var.http_method
  value_path    = var.value_path
}

// Módulo Cognito para autenticação de usuários
module "cognito" {
  source = "./modules/cognito"

  user_pool_name = var.cognito_user_pool_name
  client_name    = var.cognito_client_name

  // Configurações opcionais de senha 
  password_minimum_length    = var.cognito_password_minimum_length
  password_require_lowercase = var.cognito_password_require_lowercase
  password_require_numbers   = var.cognito_password_require_numbers
  password_require_symbols   = var.cognito_password_require_symbols
  password_require_uppercase = var.cognito_password_require_uppercase

  // Configuração MFA
  mfa_configuration = var.cognito_mfa_configuration

  // Configurações do Client
  generate_client_secret = var.cognito_generate_client_secret
  refresh_token_validity = var.cognito_refresh_token_validity
  access_token_validity  = var.cognito_access_token_validity
  id_token_validity      = var.cognito_id_token_validity
}

module "apigateway" {
  source            = "./modules/apigateway"
  function_name     = var.function_name
  http_method       = var.http_method
  user_pool_name    = var.cognito_user_pool_name
  value_path        = var.value_path
  lambda_invoke_arn = module.hello_terraform.lambda_invoke_arn
}