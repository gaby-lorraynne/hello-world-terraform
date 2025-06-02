data "archive_file" "zip_delete_item" {
  type        = "zip"
  source_file = "../lambda/lambda_delete_item/delete_item.py"
  output_path = "${path.module}/zip/lambda_delete_item.zip"
}

resource "aws_lambda_function" "remover_item" {
  function_name = "remover_item"
  runtime       = "python3.12"
  handler       = "delete_item.lambda_handler"
  memory_size   = 512
  timeout       = 10

  filename         = data.archive_file.zip_delete_item.output_path
  source_code_hash = data.archive_file.zip_delete_item.output_base64sha256

  # MUDANÇA: Referência para a role específica desta lambda
  role = aws_iam_role.lambda_exec_delete.arn

  environment {
    variables = {
      TABLE_NAME = var.TABLE_NAME
    }
  }
}

# MUDANÇA: Nome único para esta role
resource "aws_iam_role" "lambda_exec_delete" {
  name = "lambda-dynamodb-role-delete-${var.environment}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action = "sts:AssumeRole",
      Effect = "Allow",
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

# Policy para acesso ao DynamoDB
resource "aws_iam_policy" "lambda_dynamodb_delete" {
  name        = "LambdaDynamoDBDelete-${var.environment}"
  description = "Permite deletar e buscar itens da tabela DynamoDB"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "dynamodb:DeleteItem",
          "dynamodb:GetItem"
        ],
        # MUDANÇA: Usar região correta
        Resource = "arn:aws:dynamodb:${var.region}:${data.aws_caller_identity.current.account_id}:table/${var.TABLE_NAME}"
      }
    ]
  })
}

# Data source para obter account ID
data "aws_caller_identity" "current" {}

# MUDANÇA: Nome único para o attachment
resource "aws_iam_role_policy_attachment" "lambda_dynamodb_delete_attach" {
  role       = aws_iam_role.lambda_exec_delete.name
  policy_arn = aws_iam_policy.lambda_dynamodb_delete.arn
}

# Adicionar política básica de execução
resource "aws_iam_role_policy_attachment" "lambda_basic_execution_delete" {
  role       = aws_iam_role.lambda_exec_delete.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}