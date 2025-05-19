resource "aws_lambda_function" "hello_terraform" {
  function_name = var.function_name
  handler       = var.handler
  runtime       = var.runtime
  role          = var.role_arn
  filename         = "../lambda/lambda_hello_terraform/lambda_hello_terraform.zip"
  source_code_hash = filebase64sha256("../lambda/lambda_hello_terraform/lambda_hello_terraform.zip")
  memory_size   = var.memory_size
  timeout       = var.timeout
}
