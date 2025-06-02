data "archive_file" "zip_update_item" {
  type        = "zip"
  source_file = "../lambda/lambda_update_item/update_item.py"
  output_path = "${path.module}/zip/lambda_update_item.zip"
}

resource "aws_lambda_function" "atualizar_item" {
  function_name = "atualizar_item"
  runtime       = "python3.12"
  handler       = "update_item.lambda_handler"
  memory_size   = 512
  timeout       = 10

  filename         = data.archive_file.zip_update_item.output_path
  source_code_hash = data.archive_file.zip_update_item.output_base64sha256

  # MUDANÇA: Referência para a role específica desta lambda
  role = aws_iam_role.lambda_exec_update.arn

  environment {
    variables = {
      TABLE_NAME = var.TABLE_NAME
    }
  }
}

# MUDANÇA: Nome único para esta role
resource "aws_iam_role" "lambda_exec_update" {
  name = "lambda-dynamodb-role-update-${var.environment}"

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

# MUDANÇA: Nome único para o attachment
resource "aws_iam_role_policy_attachment" "lambda_dynamodb_update" {
  role       = aws_iam_role.lambda_exec_update.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess"
}

# Adicionar política básica de execução
resource "aws_iam_role_policy_attachment" "lambda_basic_execution_update" {
  role       = aws_iam_role.lambda_exec_update.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}