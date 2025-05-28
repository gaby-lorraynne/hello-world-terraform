resource "aws_api_gateway_rest_api" "rest_api" {
  name        = "rest-api"
  description = "API Gateway with Cognito Authentication"

  endpoint_configuration {
    types = ["REGIONAL"]
  }
}


resource "aws_api_gateway_authorizer" "cognito_authorizer" {
  name            = "cognito-authorizer"
  rest_api_id     = aws_api_gateway_rest_api.rest_api.id
  type            = "COGNITO_USER_POOLS"
  provider_arns   = [var.aws_cognito_user_pool_arn]
  identity_source = "method.request.header.Authorization"
}


resource "aws_api_gateway_resource" "lambdas_resource" {
  rest_api_id = aws_api_gateway_rest_api.rest_api.id
  parent_id   = aws_api_gateway_rest_api.rest_api.root_resource_id
  path_part   = var.value_path
}

resource "aws_api_gateway_method" "lambda_method" {
  resource_id   = aws_api_gateway_resource.lambdas_resource.id
  rest_api_id   = aws_api_gateway_rest_api.rest_api.id
  http_method   = var.http_method
  authorization = "COGNITO_USER_POOLS"
  authorizer_id = aws_api_gateway_authorizer.cognito_authorizer.id
}

resource "aws_api_gateway_integration" "lambda_integration" {
  rest_api_id             = aws_api_gateway_rest_api.rest_api.id
  resource_id             = aws_api_gateway_resource.lambdas_resource.id
  http_method             = aws_api_gateway_method.lambda_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = "arn:aws:apigateway:${var.region}:lambda:path/2015-03-31/functions/${var.lambda_function_arn}/invocations"
}

resource "aws_lambda_permission" "allow_api_gateway" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = var.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.rest_api.execution_arn}/*/${var.http_method}${aws_api_gateway_resource.lambdas_resource.path}"
}

resource "aws_api_gateway_deployment" "deployment" {
  depends_on  = [
    aws_api_gateway_integration.lambda_integration,
    aws_lambda_permission.allow_api_gateway  # Garantir que a permissão seja criada antes do deployment
  ]
  rest_api_id = aws_api_gateway_rest_api.rest_api.id
}

resource "aws_api_gateway_stage" "dev" {
  stage_name    = "dev"
  rest_api_id   = aws_api_gateway_rest_api.rest_api.id
  deployment_id = aws_api_gateway_deployment.deployment.id
}