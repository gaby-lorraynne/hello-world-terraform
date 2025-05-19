resource "aws_lambda_function" "adicionar_item" {
  function_name = "adicionar_item"
  runtime       = "python3.12"
  handler = "add_item.lambda_handler"
  memory_size   = 512
  timeout       = 10

  filename         = "../lambda/lambda_add_item/lambda_add_item.zip"
  source_code_hash = filebase64sha256("../lambda/lambda_add_item/lambda_add_item.zip")


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

