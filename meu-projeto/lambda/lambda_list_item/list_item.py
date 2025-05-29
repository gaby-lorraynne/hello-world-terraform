import json
import os

import boto3
from boto3.dynamodb.conditions import Attr, Key

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
            
            print(f"🔍 Buscando por PK: {pk}")  # Debug log
            print(f"📅 Data original: {data}")  # Debug log

            # Query apenas pela PK específica da data
            response = table.query(
                KeyConditionExpression=Key("PK").eq(pk)
            )
            
            print(f"📦 Response do DynamoDB: {response}")  # Debug log
        else:
            # Buscar todas as tarefas
            print("🔍 Buscando todas as tarefas (scan)")  # Debug log
            response = table.scan(
                FilterExpression=Attr("PK").begins_with("LIST#")
                & Attr("SK").begins_with("ITEM#")
            )
            
        items = response.get("Items", [])
        print(f"📦 Items encontrados no DynamoDB: {len(items)}")  # Debug log
        
        # Log dos items para debug
        for item in items:
            print(f"🔸 Item: PK={item.get('PK')}, date={item.get('date')}, name={item.get('name')}")

        # Converter para formato amigável
        tarefas = []
        for item in items:
            # Validar se o item tem os campos necessários
            if all(field in item for field in ["itemId", "name", "date", "status"]):
                tarefa = {
                    "itemId": item.get("itemId"),
                    "name": item.get("name"),
                    "date": item.get("date"),
                    "status": item.get("status"),
                    "PK": item.get("PK"),
                    "SK": item.get("SK"),
                }
                tarefas.append(tarefa)
            else:
                print(f"⚠️ Item ignorado por campos faltantes: {item}")  # Debug log

        # Se foi uma busca por data específica, validar se os itens realmente são da data correta
        if data:
            # Normalizar data original para comparação (formato YYYY-MM-DD)
            if '-' in data:
                data_original = data
            else:
                # Converter YYYYMMDD para YYYY-MM-DD
                data_original = f"{data[:4]}-{data[4:6]}-{data[6:8]}"
            
            print(f"🎯 Filtrando por data: {data_original}")  # Debug log
            tarefas_filtradas = []
            for tarefa in tarefas:
                print(f"🔸 Comparando: tarefa.date='{tarefa['date']}' vs data_original='{data_original}'")
                if tarefa["date"] == data_original:
                    tarefas_filtradas.append(tarefa)
            
            tarefas = tarefas_filtradas
            print(f"🎯 Tarefas após filtro de data '{data_original}': {len(tarefas)}")  # Debug log
          
        return {
            "message": "Tarefas listadas com sucesso!",
            "count": len(tarefas),
            "tarefas": tarefas,
        }

    except Exception as e:
        print(f"❌ Erro em listar_tarefas: {str(e)}")  # Debug log
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

        print(f"📥 Event completo: {json.dumps(event, indent=2)}")  # Debug log

        # Query parameters - aceitar tanto 'data' quanto 'date'
        if event.get("queryStringParameters"):
            query_params = event["queryStringParameters"]
            data = query_params.get("data") or query_params.get("date")  # Aceita ambos
            user_id = query_params.get("user_id")
            print(f"📥 Query parameters: {query_params}")  # Debug log

        # Body parameters (POST)
        if event.get("body"):
            body = json.loads(event["body"])
            data = body.get("data", data) or body.get("date", data)  # Aceita ambos
            user_id = body.get("user_id", user_id)
            print(f"📥 Body parameters: {body}")  # Debug log

        # User ID do Cognito
        if event.get("requestContext", {}).get("authorizer", {}).get("claims"):
            user_id = event["requestContext"]["authorizer"]["claims"].get("sub")

        print(f"📥 Parâmetros finais - data: {data}, user_id: {user_id}")  # Debug log
      
        # Executar função principal
        resultado = listar_tarefas(data, user_id)

        print(f"✅ Resultado: {resultado['count']} tarefas encontradas")  # Debug log

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
        print(f"❌ Erro no lambda_handler: {str(e)}")  # Debug log

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
    