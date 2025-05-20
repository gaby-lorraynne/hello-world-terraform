data "archive_file" "zip_add_item" {
  type        = "zip"
  source_file = "../lambda/lambda_add_item/add_item.py"
  output_path = "${path.module}/zip/lambda_add_item.zip"
}

resource "aws_lambda_function" "adicionar_item" {
  function_name = "adicionar_item"
  runtime       = "python3.12"
  handler = "add_item.lambda_handler"
  memory_size   = 512
  timeout       = 10

  filename         = data.archive_file.zip_add_item.output_path
  source_code_hash = data.archive_file.zip_add_item.output_base64sha256


  role = aws_iam_role.lambda_exec.arn

  environment {
    variables = {
      TABLE_NAME = var.TABLE_NAME
    }
  }
}

resource "aws_iam_role" "lambda_exec" {
  name = "lambda-dynamodb-role"

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

resource "aws_iam_role_policy_attachment" "lambda_dynamodb" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess"
}

