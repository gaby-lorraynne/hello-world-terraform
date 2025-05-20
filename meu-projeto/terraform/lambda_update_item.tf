data "archive_file" "zip_update_item" {
  type        = "zip"
  source_file = "../lambda/lambda_update_item/update_item.py"
  output_path = "${path.module}/zip/lambda_update_item.zip"
}

resource "aws_lambda_function" "atualizar_item" {
  function_name = "atualizar_item"
  runtime       = "python3.12"
  handler       = "update_item.lambda_handler"
  memory_size   = 512
  timeout       = 10

  filename         = data.archive_file.zip_update_item.output_path
  source_code_hash = data.archive_file.zip_update_item.output_base64sha256

  role = aws_iam_role.lambda_exec.arn
}
