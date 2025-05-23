output "user_pool_id" {
  description = "ID do User Pool do Cognito"
  value       = data.aws_cognito_user_pool.pool.id
}

output "user_pool_arn" {
  description = "ARN do User Pool do Cognito"
  value       = data.aws_cognito_user_pool.pool.arn
}

output "api_gateway_id" {
  description = "ID do API Gateway"
  value       = aws_api_gateway_rest_api.rest_api
}

output "api_gateway_url" {
  value = "${aws_api_gateway_rest_api.rest_api.execution_arn}/${var.function_name}"
}