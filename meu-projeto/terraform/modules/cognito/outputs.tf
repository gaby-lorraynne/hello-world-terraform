output "user_pool_id" {
  description = "ID do User Pool do Cognito"
  value       = aws_cognito_user_pool.user_pool.id
}

output "user_pool_arn" {
  description = "ARN do User Pool do Cognito"
  value       = aws_cognito_user_pool.user_pool.arn
}

output "client_id" {
  description = "ID do Client do User Pool"
  value       = aws_cognito_user_pool_client.client.id
}

output "user_pool_endpoint" {
  description = "Endpoint do User Pool"
  value       = aws_cognito_user_pool.user_pool.endpoint
}