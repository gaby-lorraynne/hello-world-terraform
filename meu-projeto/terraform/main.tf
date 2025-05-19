terraform {
  backend "s3" {
    bucket = "bucket-terraform-gabrielly"
    key    = "dev/terraform.tfstate"
    region = "sa-east-1"
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

//Verificar se existe a Role ou nao
resource "aws_iam_role" "lambda_role" {
  count = var.create_role ? 1 : 0

  name = "${var.function_name}-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }]
  })
}

//Atachar Politica do lambda
resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  count      = var.create_role ? 1 : 0
  role       = aws_iam_role.lambda_role[0].name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}


module "hello_terraform" {
  source = "./modules/lambda"

  function_name = var.function_name
  handler       = var.handler
  runtime       = var.runtime
  memory_size   = var.memory_size
  timeout       = var.timeout
  role_arn      = var.create_role ? aws_iam_role.lambda_role[0].arn : var.lambda_role_arn
}

