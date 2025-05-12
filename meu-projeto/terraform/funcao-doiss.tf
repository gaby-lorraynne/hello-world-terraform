resource "aws_lambda_function" "adicionarItem" {
  function_name = "adicionar-item"
  runtime       = "java17"
  handler = "com.example.ListaMercadoService::handleRequest"
  memory_size   = 512
  timeout       = 10

  filename = "../lambda/funcao-doiss/target/funcao-doiss-1.0-SNAPSHOT.jar"
  source_code_hash = filebase64sha256("../lambda/funcao-doiss/target/funcao-doiss-1.0-SNAPSHOT.jar")


  role = aws_iam_role.lambda_exec.arn
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
