output "lambda_function_name" {
  description = "Nome da função Lambda"
  value       = module.hello_terraform.lambda_function_name
}

output "lambda_function_arn" {
  description = "ARN da função Lambda"
  value       = module.hello_terraform.lambda_function_arn
}

output "lambda_invoke_arn" {
  description = "Invoke ARN da Lambda"
  value       = module.hello_terraform.lambda_invoke_arn
}

// Outputs do módulo Cognito
output "cognito_user_pool_id" {
  description = "ID do User Pool do Cognito"
  value       = module.cognito.user_pool_id
}

output "cognito_user_pool_arn" {
  description = "ARN do User Pool do Cognito"
  value       = module.cognito.user_pool_arn
}

output "cognito_client_id" {
  description = "ID do Client do User Pool do Cognito"
  value       = module.cognito.client_id
}

output "cognito_user_pool_endpoint" {
  description = "Endpoint do User Pool do Cognito"
  value       = module.cognito.user_pool_endpoint
}