output "lambda_function_name" {
  value = aws_lambda_function.hello_terraform.function_name
}

output "lambda_function_arn" {
  value = aws_lambda_function.hello_terraform.arn
}

output "lambda_invoke_arn" {
  value = aws_lambda_function.hello_terraform.invoke_arn
}

# Outputs da Lambda List Item
output "list_item_function_name" {
  description = "Nome da função Lambda de listar itens"
  value       = aws_lambda_function.listar_item.function_name
}

output "list_item_function_arn" {
  description = "ARN da função Lambda de listar itens"
  value       = aws_lambda_function.listar_item.arn
}

output "list_item_invoke_arn" {
  description = "Invoke ARN da Lambda de listar itens"
  value       = aws_lambda_function.listar_item.invoke_arn
}
