resource "aws_cognito_user_pool" "user_pool" {
  name = var.user_pool_name

  # Políticas de senha
  password_policy {
    minimum_length    = var.password_minimum_length
    require_lowercase = var.password_require_lowercase
    require_numbers   = var.password_require_numbers
    require_symbols   = var.password_require_symbols
    require_uppercase = var.password_require_uppercase
  }

  # Configurações de verificação
  auto_verified_attributes = ["email"]

  # Configurações de esquema de atributos
  schema {
    name                = "email"
    attribute_data_type = "String"
    mutable             = true
    required            = true
  }

  # Configuração de mensagens
  email_configuration {
    email_sending_account = "COGNITO_DEFAULT"
  }

  # Configurações de MFA
  mfa_configuration = var.mfa_configuration


  tags = var.tags
}

# Cliente do User Pool
resource "aws_cognito_user_pool_client" "client" {
  name         = var.client_name
  user_pool_id = aws_cognito_user_pool.user_pool.id

  # Configurações de autenticação
  explicit_auth_flows = [
    "ALLOW_USER_PASSWORD_AUTH",
    "ALLOW_REFRESH_TOKEN_AUTH",
    "ALLOW_USER_SRP_AUTH"
  ]

  # Não gerar segredo do cliente
  generate_secret = var.generate_client_secret

  # Configurações de token
  refresh_token_validity = var.refresh_token_validity
  access_token_validity  = var.access_token_validity
  id_token_validity      = var.id_token_validity

  token_validity_units {
    access_token  = "minutes"
    id_token      = "minutes"
    refresh_token = "days"
  }

  # Configurações de leitura/escrita de atributos
  read_attributes  = ["email", "email_verified", "name", "phone_number", "phone_number_verified"]
  write_attributes = ["email", "name", "phone_number"]

  # Impedir revogação do token de usuário
  prevent_user_existence_errors = "ENABLED"
}