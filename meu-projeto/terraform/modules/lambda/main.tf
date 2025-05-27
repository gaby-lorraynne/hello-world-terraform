# ZIP da função hello_terraform
data "archive_file" "zip_hello_terraform" {
  type        = "zip"
  source_file = "../lambda/lambda_hello_terraform/hello_terraform.py"
  output_path = "${path.module}/zip/lambda_hello_terraform.zip"
}

resource "aws_lambda_function" "hello_terraform" {
  function_name    = var.function_name
  handler          = var.handler
  runtime          = var.runtime
  role             = var.role_arn
  filename         = data.archive_file.zip_hello_terraform.output_path
  source_code_hash = data.archive_file.zip_hello_terraform.output_base64sha256
  memory_size      = var.memory_size
  timeout          = var.timeout
  environment {
    variables = {
      HTTP_METHOD = var.http_method
      VALUE_PATH  = var.value_path
    }
  }
}

# ZIP da lambda de listagem
data "archive_file" "zip_list_item" {
  type        = "zip"
  source_file = "../lambda/lambda_list_item/list_item.py"
  output_path = "${path.module}/zip/lambda_list_item.zip"
}

# Função Lambda para listar itens - só cria se for o módulo correto
resource "aws_lambda_function" "listar_item" {
  count = var.function_name == "listar_item" ? 1 : 0
     
  function_name    = "listar_item"
  handler          = "list_item.lambda_handler"
  runtime          = "python3.12"
  role             = var.role_arn
  filename         = data.archive_file.zip_list_item.output_path
  source_code_hash = data.archive_file.zip_list_item.output_base64sha256
  memory_size      = 512
  timeout          = 10
        
  environment {
    variables = {
      TABLE_NAME = var.table_name
    }
  }
      
  tags = {
    Name        = "listar_item"
    Environment = "dev"
  }
}