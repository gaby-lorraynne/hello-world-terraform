resource "aws_lambda_function" "atualizar_item" {
  function_name = "atualizar_item"
  runtime       = "python3.12"
  handler       = "update_item.lambda_handler"
  memory_size   = 512
  timeout       = 10

  filename         = "../lambda/lambda_update_item/lambda_update_item.zip"
  source_code_hash = filebase64sha256("../lambda/lambda_update_item/lambda_update_item.zip")

  role = aws_iam_role.lambda_exec.arn
}
