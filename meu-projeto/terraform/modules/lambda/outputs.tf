output "lambda_function_name" {
  value = aws_lambda_function.hello_terraform.function_name
}

output "lambda_function_arn" {
  value = aws_lambda_function.hello_terraform.arn
}

output "lambda_invoke_arn" {
  value = aws_lambda_function.hello_terraform.invoke_arn
}
