# ZIP da lambda de listagem
data "archive_file" "zip_list_item" {
  type        = "zip"
  source_file = "../../lambda/lambda_list_item/list_item.py"
  output_path = "${path.module}/zip/lambda_list_item.zip"
}

# Função Lambda para listar itens
resource "aws_lambda_function" "listar_item" {
  function_name = "listar_item"
  runtime       = "python3.12"
  handler       = "list_item.lambda_handler"
  memory_size   = 512
  timeout       = 10

  filename         = data.archive_file.zip_list_item.output_path
  source_code_hash = data.archive_file.zip_list_item.output_base64sha256

  role = var.role_arn

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
