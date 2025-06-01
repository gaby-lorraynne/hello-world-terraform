import json
import os
import boto3
from boto3.dynamodb.conditions import Attr, Key

# Configurar o cliente DynamoDB para sa-east-1 
dynamodb = boto3.resource("dynamodb", region_name="sa-east-1")
TABLE_NAME = os.environ.get("TABLE_NAME", "ListaMercado")


def listar_tarefas(data=None, user_id=None):
    """
    Lista todas as tarefas ou tarefas de uma data específica

    Args:
        data (str, optional): Data no formato 'YYYY-MM-DD' ou 'YYYYMMDD'
        user_id (str, optional): ID do usuário (do Cognito)

    Returns:
        dict: Resposta com tarefas encontradas
    """
    try:
        table = dynamodb.Table(TABLE_NAME)

        if data:
            # Converter data para formato da PK se necessário
            if '-' in data:
                # Converter de 'YYYY-MM-DD' para 'YYYYMMDD'
                data_formatada = data.replace('-', '')
            else:
                # Já está no formato correto 'YYYYMMDD'
                data_formatada = data
            
            # Buscar tarefas de data específica
            pk = f"LIST#{data_formatada}"
            
            print(f"🔍 Buscando por PK: {pk}")
            print(f"📅 Data original: {data}")
            print(f"📅 Data formatada: {data_formatada}")

            # Query apenas pela PK específica da data
            response = table.query(
                KeyConditionExpression=Key("PK").eq(pk)
            )
            
            print(f"📦 Response do DynamoDB: {response}")
        else:
            # Buscar todas as tarefas
            print("🔍 Buscando todas as tarefas (scan)")
            response = table.scan(
                FilterExpression=Attr("PK").begins_with("LIST#")
                & Attr("SK").begins_with("ITEM#")
            )
            
        items = response.get("Items", [])
        print(f"📦 Items encontrados no DynamoDB: {len(items)}")
        
        # Log dos items para debug
        for item in items:
            print(f"🔸 Item: PK={item.get('PK')}, date={item.get('date')}, name={item.get('name')}")

        # Converter para formato amigável
        tarefas = []
        
        # Se foi especificada uma data, precisamos filtrar os resultados
        # para garantir que apenas itens da data correta sejam retornados
        if data:
            # Normalizar a data de busca para comparação
            if '-' in data:
                data_busca = data  # Já está no formato YYYY-MM-DD
            else:
                # Converter YYYYMMDD para YYYY-MM-DD
                data_busca = f"{data[:4]}-{data[4:6]}-{data[6:8]}"
        
        for item in items:
            # Validar se o item tem os campos necessários
            if all(field in item for field in ["itemId", "name", "date", "status"]):
                # Normalizar o formato da data para YYYY-MM-DD
                item_date = item.get("date", "")
                
                # Se a data está no formato YYYYMMDD, converter para YYYY-MM-DD
                if len(item_date) == 8 and '-' not in item_date:
                    normalized_date = f"{item_date[:4]}-{item_date[4:6]}-{item_date[6:8]}"
                else:
                    normalized_date = item_date
                
                # FILTRO ADICIONAL: Se foi especificada uma data, verificar se o item corresponde
                if data:
                    # Comparar com a data de busca normalizada
                    if normalized_date != data_busca:
                        print(f"⚠️ Item filtrado - data não corresponde: {normalized_date} != {data_busca}")
                        continue  # Pular este item
                
                tarefa = {
                    "itemId": item.get("itemId"),
                    "name": item.get("name"),
                    "date": normalized_date,  # Usar data normalizada
                    "status": item.get("status"),
                    "PK": item.get("PK"),
                    "SK": item.get("SK"),
                }
                tarefas.append(tarefa)
                
                print(f"✅ Item processado: {item.get('name')} - data original: {item_date} - data normalizada: {normalized_date}")
            else:
                print(f"⚠️ Item ignorado por campos faltantes: {item}")
          
        return {
            "message": "Tarefas listadas com sucesso!",
            "count": len(tarefas),
            "tarefas": tarefas,
        }

    except Exception as e:
        print(f"❌ Erro em listar_tarefas: {str(e)}")
        raise Exception(f"Erro ao listar tarefas: {str(e)}")


def lambda_handler(event, context):
    """
    Handler principal da Lambda

    Args:
        event (dict): Evento do API Gateway
        context (object): Contexto da Lambda

    Returns:
        dict: Resposta HTTP
    """
    try:
        # Extrair parâmetros
        data = None
        user_id = None

        print(f"📥 Event completo: {json.dumps(event, indent=2)}")

        # Query parameters - aceitar tanto 'data' quanto 'date'
        if event.get("queryStringParameters"):
            query_params = event["queryStringParameters"]
            data = query_params.get("data") or query_params.get("date")
            user_id = query_params.get("user_id")
            print(f"📥 Query parameters: {query_params}")

        # Body parameters (POST)
        if event.get("body"):
            body = json.loads(event["body"])
            data = body.get("data", data) or body.get("date", data)
            user_id = body.get("user_id", user_id)
            print(f"📥 Body parameters: {body}")

        # User ID do Cognito
        if event.get("requestContext", {}).get("authorizer", {}).get("claims"):
            user_id = event["requestContext"]["authorizer"]["claims"].get("sub")

        print(f"📥 Parâmetros finais - data: {data}, user_id: {user_id}")
      
        # Executar função principal
        resultado = listar_tarefas(data, user_id)

        print(f"✅ Resultado: {resultado['count']} tarefas encontradas")

        # Resposta de sucesso
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "GET,OPTIONS",
            },
            "body": json.dumps(resultado, ensure_ascii=False),
        }

    except Exception as e:
        print(f"❌ Erro no lambda_handler: {str(e)}")

        # Resposta de erro
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps(
                {"error": "Erro interno do servidor", "message": str(e)},
                ensure_ascii=False,
            ),
        }
    