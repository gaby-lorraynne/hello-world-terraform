output "lambda_function_name" {
  value = aws_lambda_function.hello_terraform.function_name
}

output "lambda_function_arn" {
  value = aws_lambda_function.hello_terraform.arn
}

output "lambda_invoke_arn" {
  value = aws_lambda_function.hello_terraform.invoke_arn
}

# Outputs da função listar_item (condicional)
output "list_item_function_name" {
  value = var.function_name == "listar_item" ? aws_lambda_function.listar_item[0].function_name : null
}

output "list_item_function_arn" {
  value = var.function_name == "listar_item" ? aws_lambda_function.listar_item[0].arn : null
}

output "list_item_invoke_arn" {
  value = var.function_name == "listar_item" ? aws_lambda_function.listar_item[0].invoke_arn : null
}