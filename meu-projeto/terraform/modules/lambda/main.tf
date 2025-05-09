resource "aws_lambda_function" "this" {
  function_name = var.function_name
  handler       = var.handler
  runtime       = var.runtime
  role          = var.role_arn
  filename      = "../lambda/funcao-um/target/funcao-um-1.0-SNAPSHOT.jar"
  source_code_hash = filebase64sha256("../lambda/funcao-um/target/funcao-um-1.0-SNAPSHOT.jar")
  memory_size   = var.memory_size
  timeout       = var.timeout
}
