output "user_pool_id" {
  description = "ID do User Pool do Cognito"
  value       = var.aws_cognito_user_pool_id
}

output "user_pool_arn" {
  description = "ARN do User Pool do Cognito"
  value       = var.aws_cognito_user_pool_arn
}

output "api_gateway_id" {
  description = "ID do API Gateway"
  value       = aws_api_gateway_rest_api.rest_api
}

output "api_gateway_url" {
  value = "${aws_api_gateway_rest_api.rest_api.execution_arn}/${var.function_name}"
}

output "lambda_invoke_arn" {
  value = var.lambda_invoke_arn
}

output "lambda_function_arn" {
  value = var.lambda_function_arn
}
