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

  role = aws_iam_role.lambda_exec.arn

  environment {
    variables = {
      TABLE_NAME = var.TABLE_NAME
    }
  }
}

# Policy para acesso ao DynamoDB
resource "aws_iam_policy" "lambda_dynamodb_delete" {
  name        = "LambdaDynamoDBDelete"
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
        Resource = "arn:aws:dynamodb:sa-east-1:121316933785:table/ListaMercado"
      }
    ]
  })
}

# Anexar a policy à role usada pela Lambda
resource "aws_iam_role_policy_attachment" "lambda_dynamodb_attach" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = aws_iam_policy.lambda_dynamodb_delete.arn
}
