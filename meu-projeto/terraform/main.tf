terraform {
  backend "s3" {
    bucket = "bucket-terraform-gabrielly"
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


# Tabela DynamoDB
resource "aws_dynamodb_table" "lista_mercado" {
  name           = var.TABLE_NAME
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "PK"
  range_key      = "SK"

  attribute {
    name = "PK"
    type = "S"
  }

  attribute {
    name = "SK"
    type = "S"
  }

  tags = {
    Name        = var.TABLE_NAME
    Environment = var.environment
  }
}

# Role IAM para a função principal Hello Terraform
resource "aws_iam_role" "lambda_role" {
  count = var.create_role ? 1 : 0
  name  = "${var.function_name}-role-${var.environment}"

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

# Políticas para a role principal
resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  count      = var.create_role ? 1 : 0
  role       = aws_iam_role.lambda_role[0].name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy_attachment" "lambda_main_dynamodb" {
  count      = var.create_role ? 1 : 0
  role       = aws_iam_role.lambda_role[0].name
  policy_arn = "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess"
}

# Módulo para a função Hello Terraform
module "hello_terraform" {
  source = "./modules/lambda"

  function_name = "${var.function_name}-${var.environment}"
  handler       = var.handler
  runtime       = var.runtime
  memory_size   = var.memory_size
  timeout       = var.timeout
  role_arn      = var.create_role ? aws_iam_role.lambda_role[0].arn : var.lambda_role_arn
  http_method   = var.http_method
  value_path    = var.value_path
  table_name    = var.TABLE_NAME
  
  depends_on = [aws_dynamodb_table.lista_mercado]
}

# Módulo Cognito para autenticação de usuários
module "cognito" {
  source = "./modules/cognito"

  user_pool_name = "${var.cognito_user_pool_name}-${var.environment}"
  client_name    = "${var.cognito_client_name}-${var.environment}"

  # Configurações opcionais de senha 
  password_minimum_length    = var.cognito_password_minimum_length
  password_require_lowercase = var.cognito_password_require_lowercase
  password_require_numbers   = var.cognito_password_require_numbers
  password_require_symbols   = var.cognito_password_require_symbols
  password_require_uppercase = var.cognito_password_require_uppercase

  # Configuração MFA
  mfa_configuration = var.cognito_mfa_configuration

  # Configurações do Client
  generate_client_secret = var.cognito_generate_client_secret
  refresh_token_validity = var.cognito_refresh_token_validity
  access_token_validity  = var.cognito_access_token_validity
  id_token_validity      = var.cognito_id_token_validity
}

# Módulo do API Gateway principal
module "apigateway" {
  source                    = "./modules/apigateway"
  function_name             = "${var.function_name}-${var.environment}"
  http_method               = var.http_method
  user_pool_name            = "${var.cognito_user_pool_name}-${var.environment}"
  aws_cognito_user_pool_arn = module.cognito.user_pool_arn
  aws_cognito_user_pool_id  = module.cognito.user_pool_id
  value_path                = var.value_path
  lambda_invoke_arn         = module.hello_terraform.lambda_invoke_arn
  lambda_function_arn       = module.hello_terraform.lambda_function_arn
  region                    = var.region

    # IMPORTANTE: Garantir que a Lambda seja criada primeiro
  depends_on = [
    module.hello_terraform,
    aws_iam_role.lambda_role,
    aws_iam_role_policy_attachment.lambda_basic_execution,
    aws_iam_role_policy_attachment.lambda_main_dynamodb
  ]
}

# Role IAM para a Lambda List Item
resource "aws_iam_role" "lambda_exec_listar_item" {
  name = "lambda-role-listar-item-${var.environment}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

# Políticas para a role de listar item
resource "aws_iam_role_policy_attachment" "lambda_basic_execution_list" {
  role       = aws_iam_role.lambda_exec_listar_item.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy_attachment" "lambda_dynamodb_list_item" {
  role       = aws_iam_role.lambda_exec_listar_item.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess"
}

# Módulo Lambda para List Item
module "lambda_list_item" {
  source = "./modules/lambda"

  function_name = "listar_item_${var.environment}"
  handler       = "list_item.lambda_handler"
  runtime       = var.runtime
  memory_size   = var.memory_size
  timeout       = var.timeout
  role_arn      = aws_iam_role.lambda_exec_listar_item.arn
  http_method   = "GET"
  value_path    = "lista-tarefa"
  table_name    = var.TABLE_NAME
  
  depends_on = [aws_dynamodb_table.lista_mercado]
}

# Módulo API Gateway para List Item
module "apigateway_list" {
  source                   = "./modules/api_gateway_list"
  api_name                 = "lista-item"
  environment              = var.environment
  function_name_list       = module.lambda_list_item.lambda_function_name
  http_method              = "GET"
  region                   = var.region
  lambda_invoke_arn_get    = module.lambda_list_item.lambda_invoke_arn
  lambda_function_arn      = module.lambda_list_item.lambda_function_arn
  lambda_function_name_get = module.lambda_list_item.lambda_function_name
  cognito_user_pool_arn    = module.cognito.user_pool_arn
}