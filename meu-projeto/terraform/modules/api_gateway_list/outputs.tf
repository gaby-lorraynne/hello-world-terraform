output "api_invoke_url" {
  value = "https://${aws_api_gateway_rest_api.api_gateway_list.id}.execute-api.${var.region}.amazonaws.com/${aws_api_gateway_stage.dev.stage_name}"
}


output "lambda_invoke_arn" {
  value = var.lambda_invoke_arn_get
}

output "lambda_function_arn" {
  value = var.lambda_function_arn
}

output "function_name" {
  description = "Nome da função Lambda"
  value       = var.lambda_function_name_get
}
