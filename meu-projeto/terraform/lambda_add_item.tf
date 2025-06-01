data "archive_file" "zip_add_item" {
  type        = "zip"
  source_file = "../lambda/lambda_add_item/add_item.py"
  output_path = "${path.module}/zip/lambda_add_item.zip"
}

resource "aws_lambda_function" "adicionar_item" {
  function_name = "adicionar_item"
  runtime       = "python3.12"
  handler       = "add_item.lambda_handler"
  memory_size   = 512
  timeout       = 10

  filename         = data.archive_file.zip_add_item.output_path
  source_code_hash = data.archive_file.zip_add_item.output_base64sha256
  
  # MUDANÇA: Referência para a role específica desta lambda
  role = aws_iam_role.lambda_exec_add.arn

  environment {
    variables = {
      TABLE_NAME = var.TABLE_NAME
    }
  }
}

# MUDANÇA: Nome único para esta role
resource "aws_iam_role" "lambda_exec_add" {
  name = "lambda-dynamodb-role-add-${var.environment}"

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
resource "aws_iam_role_policy_attachment" "lambda_dynamodb_add" {
  role       = aws_iam_role.lambda_exec_add.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess"
}

# Adicionar política básica de execução
resource "aws_iam_role_policy_attachment" "lambda_basic_execution_add" {
  role       = aws_iam_role.lambda_exec_add.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}