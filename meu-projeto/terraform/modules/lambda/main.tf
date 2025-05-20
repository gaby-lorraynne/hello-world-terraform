data "archive_file" "zip_hello_terraform" {
  type        = "zip"
  source_file = "../lambda/lambda_hello_terraform/hello_terraform.py"
  output_path = "${path.module}/zip/lambda_hello_terraform.zip"
}

resource "aws_lambda_function" "hello_terraform" {
  function_name = var.function_name
  handler       = var.handler
  runtime       = var.runtime
  role          = var.role_arn
  filename         = data.archive_file.zip_hello_terraform.output_path
  source_code_hash = data.archive_file.zip_hello_terraform.output_base64sha256
  memory_size   = var.memory_size
  timeout       = var.timeout
}
