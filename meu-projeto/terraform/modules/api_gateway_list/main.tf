resource "aws_api_gateway_rest_api" "api_gateway_list" {
  name = "${var.api_name}-${var.environment}"

  endpoint_configuration {
    types = ["REGIONAL"]
  }
}

resource "aws_api_gateway_authorizer" "cognito" {
  name            = "cognito-authorizer"
  rest_api_id     = aws_api_gateway_rest_api.api_gateway_list.id
  identity_source = "method.request.header.Authorization"
  type            = "COGNITO_USER_POOLS"
  provider_arns   = [var.cognito_user_pool_arn]
}

resource "aws_api_gateway_resource" "lista_tarefa" {
  rest_api_id = aws_api_gateway_rest_api.api_gateway_list.id
  parent_id   = aws_api_gateway_rest_api.api_gateway_list.root_resource_id
  path_part   = "lista-tarefa"
}

resource "aws_api_gateway_method" "get_lista" {
  rest_api_id   = aws_api_gateway_rest_api.api_gateway_list.id
  resource_id   = aws_api_gateway_resource.lista_tarefa.id
  http_method   = "GET"
  authorization = "COGNITO_USER_POOLS"
  authorizer_id = aws_api_gateway_authorizer.cognito.id
}

resource "aws_api_gateway_integration" "get_lista" {
  rest_api_id             = aws_api_gateway_rest_api.api_gateway_list.id
  resource_id             = aws_api_gateway_resource.lista_tarefa.id
  http_method             = aws_api_gateway_method.get_lista.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = "arn:aws:apigateway:${var.region}:lambda:path/2015-03-31/functions/${var.lambda_function_arn}/invocations"
}

resource "aws_lambda_permission" "allow_api_gateway" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = var.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.api_gateway_list.execution_arn}/*/*/*"
}

resource "aws_api_gateway_deployment" "deployment" {
  depends_on  = [aws_api_gateway_integration.get_lista]
  rest_api_id = aws_api_gateway_rest_api.api_gateway_list.id
}

resource "aws_api_gateway_stage" "dev" {
  stage_name    = "dev"
  rest_api_id   = aws_api_gateway_rest_api.api_gateway_list.id
  deployment_id = aws_api_gateway_deployment.deployment.id
}
