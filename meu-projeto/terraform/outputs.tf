output "lambda_function_name" {
  description = "Nome da função Lambda"
  value       = module.lambda_funcao_um.lambda_function_name
}

output "lambda_function_arn" {
  description = "ARN da função Lambda"
  value       = module.lambda_funcao_um.lambda_function_arn
}

output "lambda_invoke_arn" {
  description = "Invoke ARN da Lambda"
  value       = module.lambda_funcao_um.lambda_invoke_arn
}
