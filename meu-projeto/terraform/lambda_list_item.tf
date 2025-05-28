# ZIP da função de listagem de itens
data "archive_file" "zip_list_item" {
  type        = "zip"
  source_file = "../lambda/lambda_list_item/list_item.py"  # Caminho do arquivo Python
  output_path = "${path.module}/zip/lambda_list_item.zip"
}

# Função Lambda para listar itens
resource "aws_lambda_function" "listar_item" {
  function_name = "listar_item_v1"
  runtime       = "python3.12"
  handler       = "list_item.lambda_handler"
  memory_size   = 512
  timeout       = 10

  filename         = data.archive_file.zip_list_item.output_path
  source_code_hash = data.archive_file.zip_list_item.output_base64sha256

  role = aws_iam_role.lambda_exec_listar_item.arn  # Usando a role única para listar_item

  environment {
    variables = {
      TABLE_NAME = var.TABLE_NAME
    }
  }

  tags = {
    Name        = "listar_item"
    Environment = "dev"
  }
}

# Criando a role IAM para a Lambda `listar_item`
resource "aws_iam_role" "lambda_exec_listar_item" {
  name = "lambda-dynamodb-role-listar-item"

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

# Anexando a política de DynamoDB à role
resource "aws_iam_role_policy_attachment" "lambda_dynamodb_listar_item" {
  role       = aws_iam_role.lambda_exec_listar_item.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess"
}
