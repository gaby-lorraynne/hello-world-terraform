resource "aws_lambda_function" "atualizarItem" {
  function_name = "atualizar-item"
  runtime       = "java17"
  handler       = "com.example.AtualizarItemService::handleRequest"
  memory_size   = 512
  timeout       = 10

  filename         = "../lambda/funcao-tres/target/funcao-tres-1.0-SNAPSHOT.jar"
  source_code_hash = filebase64sha256("../lambda/funcao-tres/target/funcao-tres-1.0-SNAPSHOT.jar")

  role = aws_iam_role.lambda_exec.arn
}
