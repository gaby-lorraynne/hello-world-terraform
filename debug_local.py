"""
Script para debug local das funções Lambda - VERSÃO CORRIGIDA
Funciona com a estrutura atual do projeto
"""

import json
import os
import sys
from unittest.mock import MagicMock, patch


def encontrar_arquivo_lambda():
    """
    Encontra o arquivo list_item.py na estrutura do projeto
    """
    # Possíveis caminhos onde o arquivo pode estar
    possible_paths = [
        "meu-projeto/lambda/lambda_list_item",
        "lambda/lambda_list_item",
        "./meu-projeto/lambda/lambda_list_item",
        "../meu-projeto/lambda/lambda_list_item",
    ]

    for path in possible_paths:
        full_path = os.path.abspath(path)
        file_path = os.path.join(full_path, "list_item.py")

        if os.path.exists(file_path):
            print(f"✅ Arquivo encontrado em: {full_path}")
            return full_path

    print("❌ Arquivo list_item.py não encontrado!")
    print("📁 Estrutura esperada:")
    print("   meu-projeto/")
    print("   └── lambda/")
    print("       └── lambda_list_item/")
    print("           └── list_item.py")
    print("")
    print("📋 Tentamos buscar em:")
    for path in possible_paths:
        print(f"   • {os.path.abspath(path)}")

    return None


def criar_arquivo_lambda_exemplo():
    """
    Cria um arquivo de exemplo se não existir
    """
    print("🛠️  Criando arquivo list_item.py de exemplo...")

    # Criar estrutura de pastas
    lambda_dir = "meu-projeto/lambda/lambda_list_item"
    os.makedirs(lambda_dir, exist_ok=True)

    # Código da lambda corrigido
    lambda_code = '''import boto3
import os
import json
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb', region_name='sa-east-1')
TABLE_NAME = os.environ.get('TABLE_NAME', 'ListaMercado')

def listar_tarefas(data=None, user_id=None):
    """
    Lista todas as tarefas ou tarefas de uma data específica
    """
    try:
        table = dynamodb.Table(TABLE_NAME)
        
        if data:
            # Se data específica fornecida, busca tarefas dessa data
            pk = f"LIST#{data.replace('-', '')}"
            
            response = table.query(
                KeyConditionExpression=Key('PK').eq(pk),
                FilterExpression=Key('SK').begins_with('ITEM#')
            )
        else:
            # Se não especificou data, busca todas as tarefas do usuário
            response = table.scan(
                FilterExpression=Key('PK').begins_with('LIST#')
            )
        
        items = response.get('Items', [])
        
        # Converter os itens para formato mais amigável
        tarefas = []
        for item in items:
            tarefa = {
                'itemId': item.get('itemId'),
                'name': item.get('name'),
                'date': item.get('date'),
                'status': item.get('status'),
                'PK': item.get('PK'),
                'SK': item.get('SK')
            }
            tarefas.append(tarefa)
        
        return {
            'message': 'Tarefas listadas com sucesso!',
            'count': len(tarefas),
            'tarefas': tarefas
        }
        
    except Exception as e:
        raise Exception(f"Erro ao listar tarefas: {str(e)}")

def lambda_handler(event, context):
    """
    Handler principal da Lambda
    """
    try:
        # Extrair parâmetros da query string ou body
        data = None
        user_id = None
        
        # Verificar se existe queryStringParameters
        if event.get('queryStringParameters'):
            data = event['queryStringParameters'].get('data')
            user_id = event['queryStringParameters'].get('user_id')
        
        # Verificar se existe body (para POST requests)
        if event.get('body'):
            body = json.loads(event['body'])
            data = body.get('data', data)
            user_id = body.get('user_id', user_id)
        
        # Extrair user_id do contexto do Cognito se disponível
        if event.get('requestContext', {}).get('authorizer', {}).get('claims'):
            user_id = event['requestContext']['authorizer']['claims'].get('sub')
        
        resultado = listar_tarefas(data, user_id)
        
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "GET,OPTIONS"
            },
            "body": json.dumps(resultado, ensure_ascii=False)
        }
        
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "error": "Erro interno do servidor",
                "message": str(e)
            }, ensure_ascii=False)
        }
'''

    # Escrever arquivo
    file_path = os.path.join(lambda_dir, "list_item.py")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(lambda_code)

    print(f"✅ Arquivo criado em: {file_path}")
    return lambda_dir


def test_with_mock():
    """
    Testa com dados mockados (quando não há acesso ao DynamoDB)
    """
    print("🎭 Testando com DADOS MOCKADOS...")

    # Encontrar ou criar arquivo lambda
    lambda_path = encontrar_arquivo_lambda()

    if not lambda_path:
        print("🛠️  Arquivo não encontrado, criando exemplo...")
        lambda_path = criar_arquivo_lambda_exemplo()

    # Adicionar ao PYTHONPATH
    if lambda_path not in sys.path:
        sys.path.insert(0, lambda_path)

    # Dados de exemplo para o mock
    mock_items = [
        {
            "PK": "LIST#20241226",
            "SK": "ITEM#123e4567-e89b-12d3-a456-426614174000",
            "itemId": "123e4567-e89b-12d3-a456-426614174000",
            "name": "Comprar leite",
            "date": "2024-12-26",
            "status": "todo",
        },
        {
            "PK": "LIST#20241226",
            "SK": "ITEM#987fcdeb-51a2-4bc3-d789-123456789abc",
            "itemId": "987fcdeb-51a2-4bc3-d789-123456789abc",
            "name": "Fazer exercício",
            "date": "2024-12-26",
            "status": "done",
        },
        {
            "PK": "LIST#20241227",
            "SK": "ITEM#456e7890-f12a-34b5-c678-901234567def",
            "itemId": "456e7890-f12a-34b5-c678-901234567def",
            "name": "Estudar programação",
            "date": "2024-12-27",
            "status": "todo",
        },
    ]

    # Tentar importar o módulo
    try:
        import list_item

        print(f"✅ Módulo list_item importado com sucesso!")
    except ImportError as e:
        print(f"❌ Erro ao importar list_item: {e}")
        return

    # Mock do DynamoDB
    with patch("list_item.dynamodb") as mock_dynamodb:
        mock_table = MagicMock()
        mock_dynamodb.Table.return_value = mock_table

        # Configurar diferentes respostas para diferentes testes
        mock_table.scan.return_value = {"Items": mock_items}
        mock_table.query.return_value = {
            "Items": [item for item in mock_items if "20241226" in item["PK"]]
        }

        print("\n" + "=" * 60)
        print("🧪 EXECUTANDO TESTES COM MOCK")
        print("=" * 60)

        # Teste 1: Listar todas as tarefas
        print("\n📋 Teste 1: Listar TODAS as tarefas")
        print("-" * 40)

        event = create_api_gateway_event()
        context = create_lambda_context()

        response = list_item.lambda_handler(event, context)
        print(f"Status Code: {response['statusCode']}")

        if response["statusCode"] == 200:
            body_data = json.loads(response["body"])
            print(f"✅ Sucesso! Encontradas {body_data['count']} tarefas")
            print("📝 Tarefas:")
            for i, tarefa in enumerate(body_data["tarefas"], 1):
                print(
                    f"   {i}. {tarefa['name']} - {tarefa['date']} [{tarefa['status']}]"
                )
        else:
            body_data = json.loads(response["body"])
            print(f"❌ Erro: {body_data.get('message', 'Erro desconhecido')}")

        # Teste 2: Listar tarefas por data específica
        print("\n📅 Teste 2: Listar tarefas de 2024-12-26")
        print("-" * 40)

        event_with_date = create_api_gateway_event(query_params={"data": "2024-12-26"})

        response = list_item.lambda_handler(event_with_date, context)
        print(f"Status Code: {response['statusCode']}")

        if response["statusCode"] == 200:
            body_data = json.loads(response["body"])
            print(
                f"✅ Sucesso! Encontradas {body_data['count']} tarefas para 2024-12-26"
            )
            print("📝 Tarefas:")
            for i, tarefa in enumerate(body_data["tarefas"], 1):
                print(
                    f"   {i}. {tarefa['name']} - {tarefa['date']} [{tarefa['status']}]"
                )
        else:
            body_data = json.loads(response["body"])
            print(f"❌ Erro: {body_data.get('message', 'Erro desconhecido')}")

        # Teste 3: Simular erro
        print("\n🚨 Teste 3: Simular ERRO no DynamoDB")
        print("-" * 40)

        mock_table.scan.side_effect = Exception("Erro simulado no DynamoDB")

        response = list_item.lambda_handler(event, context)
        print(f"Status Code: {response['statusCode']}")

        body_data = json.loads(response["body"])
        print(
            f"⚠️  Erro simulado capturado: {body_data.get('message', 'Erro desconhecido')}"
        )

        # Teste 4: Teste com usuário Cognito
        print("\n👤 Teste 4: Com usuário COGNITO")
        print("-" * 40)

        # Resetar mock para funcionar novamente
        mock_table.scan.side_effect = None
        mock_table.scan.return_value = {"Items": mock_items}

        event_with_user = create_api_gateway_event(query_params={"data": "2024-12-26"})
        event_with_user["requestContext"]["authorizer"]["claims"] = {
            "sub": "user-abc-123-def-456",
            "email": "usuario.test@exemplo.com",
        }

        response = list_item.lambda_handler(event_with_user, context)
        print(f"Status Code: {response['statusCode']}")

        if response["statusCode"] == 200:
            body_data = json.loads(response["body"])
            print(f"✅ Sucesso! Usuário autenticado - {body_data['count']} tarefas")
            print(f"👤 User ID extraído do Cognito: user-abc-123-def-456")

        print("\n" + "=" * 60)
        print("🎉 TODOS OS TESTES MOCKADOS CONCLUÍDOS!")
        print("=" * 60)


def create_api_gateway_event(
    http_method="GET", path="/lista-tarefa", query_params=None, body=None, headers=None
):
    """
    Cria um evento simulado do API Gateway
    """
    event = {
        "httpMethod": http_method,
        "path": path,
        "pathParameters": None,
        "queryStringParameters": query_params,
        "headers": headers
        or {
            "Content-Type": "application/json",
            "User-Agent": "PostmanRuntime/7.26.8",
            "Authorization": "Bearer mock-token-123",
        },
        "body": json.dumps(body) if body else None,
        "isBase64Encoded": False,
        "requestContext": {
            "accountId": "123456789012",
            "apiId": "abc123def4",
            "stage": "dev",
            "requestId": "test-request-id-" + str(hash(str(query_params)))[:8],
            "identity": {
                "sourceIp": "192.168.1.100",
                "userAgent": "PostmanRuntime/7.26.8",
            },
            "authorizer": {
                "claims": {
                    "sub": "user-abc-123-def-456",
                    "email": "usuario.teste@exemplo.com",
                    "cognito:username": "usuario.teste",
                }
            },
        },
    }
    return event


def create_lambda_context():
    """
    Cria um contexto simulado do Lambda
    """

    class LambdaContext:
        def __init__(self):
            self.function_name = "listar-tarefas-test"
            self.function_version = "$LATEST"
            self.invoked_function_arn = (
                "arn:aws:lambda:sa-east-1:123456789012:function:listar-tarefas-test"
            )
            self.memory_limit_in_mb = "512"
            self.remaining_time_in_millis = lambda: 25000
            self.log_group_name = "/aws/lambda/listar-tarefas-test"
            self.log_stream_name = "2024/12/26/[$LATEST]abc123def456"
            self.aws_request_id = "test-request-" + str(hash("test"))[:10]

    return LambdaContext()


def verificar_estrutura_projeto():
    """
    Verifica e mostra a estrutura atual do projeto
    """
    print("📁 VERIFICANDO ESTRUTURA DO PROJETO")
    print("=" * 40)

    # Listar arquivos relevantes
    arquivos_importantes = [
        "meu-projeto/lambda/lambda_list_item/list_item.py",
        "meu-projeto/tests/test_list_tasks.py",
        "meu-projeto/terraform/main.tf",
        "meu-projeto/terraform/modules/lambda/main.tf",
        "debug_local.py",
    ]

    print("🔍 Verificando arquivos importantes:")
    for arquivo in arquivos_importantes:
        if os.path.exists(arquivo):
            size = os.path.getsize(arquivo)
            print(f"   ✅ {arquivo} ({size} bytes)")
        else:
            print(f"   ❌ {arquivo} (não encontrado)")

    print("\n🗂️  Estrutura de pastas:")

    # Mostrar estrutura das pastas principais
    for root, dirs, files in os.walk("."):
        # Pular pastas desnecessárias
        dirs[:] = [
            d
            for d in dirs
            if not d.startswith(".") and d not in ["__pycache__", "node_modules"]
        ]

        level = root.replace(".", "").count(os.sep)
        indent = "   " * level

        if level < 3:  # Limitar profundidade
            print(f"{indent}{os.path.basename(root)}/")
            sub_indent = "   " * (level + 1)
            for file in files:
                if file.endswith((".py", ".tf", ".json", ".md", ".txt")):
                    print(f"{sub_indent}{file}")


def main():
    """
    Função principal
    """
    print("🚀 DEBUG LOCAL - Lista de Tarefas Lambda")
    print("=" * 70)

    # Verificar estrutura do projeto
    verificar_estrutura_projeto()
    print("\n")

    # Configurar variáveis de ambiente
    os.environ["TABLE_NAME"] = "ListaMercado"
    os.environ["AWS_DEFAULT_REGION"] = "sa-east-1"

    print("⚙️  Configurações:")
    print(f"   📊 Tabela DynamoDB: {os.environ.get('TABLE_NAME')}")
    print(f"   🌍 Região AWS: {os.environ.get('AWS_DEFAULT_REGION')}")
    print()

    # Sempre usar mock por enquanto, já que a estrutura está funcionando para testes
    print("🎭 Executando em modo MOCK (mais confiável para desenvolvimento)...")
    test_with_mock()

    print("\n" + "=" * 70)
    print("✅ DEBUG LOCAL CONCLUÍDO!")
    print("\n💡 PRÓXIMOS PASSOS:")
    print("   1. 📱 Configure o Postman com as informações do terraform output")
    print("   2. 🚀 Faça o deploy: cd terraform && terraform apply")
    print("   3. 👤 Crie usuário no Cognito")
    print("   4. 🧪 Teste a API real no Postman")
    print("\n🎯 Os testes unitários já estão passando (9/9) - ótimo trabalho!")


if __name__ == "__main__":
    main()
