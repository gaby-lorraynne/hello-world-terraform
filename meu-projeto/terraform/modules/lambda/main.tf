# Determinar o caminho correto do arquivo Python baseado no nome da função
locals {
  python_file_map = {
    "hello_terraform"     = "../lambda/lambda_hello_terraform/hello_terraform.py"
    "hello_terraform-dev" = "../lambda/lambda_hello_terraform/hello_terraform.py"
    "listar_item_dev"     = "../lambda/lambda_list_item/list_item.py"
    "listar_item"         = "../lambda/lambda_list_item/list_item.py"
  }
  
  # Usar o mapeamento ou um padrão default
  source_file = lookup(local.python_file_map, var.function_name, "../lambda/${var.function_name}/${var.function_name}.py")
}

# ZIP da função
data "archive_file" "lambda_zip" {
  type        = "zip"
  source_file = local.source_file
  output_path = "${path.module}/zip/${var.function_name}.zip"
}

# Função Lambda
resource "aws_lambda_function" "lambda" {
  function_name    = var.function_name
  handler          = var.handler
  runtime          = var.runtime
  role             = var.role_arn
  filename         = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  memory_size      = var.memory_size
  timeout          = var.timeout

  environment {
    variables = {
      HTTP_METHOD = var.http_method
      VALUE_PATH  = var.value_path
      TABLE_NAME  = var.table_name
    }
  }

  tags = {
    Name        = var.function_name
    Environment = "dev"
  }
}
