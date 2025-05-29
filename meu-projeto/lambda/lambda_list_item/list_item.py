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

            # Query apenas pela PK específica da data
            response = table.query(
                KeyConditionExpression=Key("PK").eq(pk)
            )
        else:
            # Buscar todas as tarefas
            response = table.scan(
                FilterExpression=Attr("PK").begins_with("LIST#")
                & Attr("SK").begins_with("ITEM#")
            )
            
        items = response.get("Items", [])
        print(f"📦 Items encontrados no DynamoDB: {len(items)}")  # Debug log

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

        # Filtro adicional por data se necessário (double check)
        if data:
            # Normalizar data original para comparação
            data_original = data if '-' in data else f"{data[:4]}-{data[4:6]}-{data[6:8]}"
            tarefas = [tarefa for tarefa in tarefas if tarefa["date"] == data_original]
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

        # Query parameters (?data=2024-12-26 ou ?data=20241226)
        if event.get("queryStringParameters"):
            data = event["queryStringParameters"].get("data")
            user_id = event["queryStringParameters"].get("user_id")

        # Body parameters (POST)
        if event.get("body"):
            body = json.loads(event["body"])
            data = body.get("data", data)
            user_id = body.get("user_id", user_id)

        # User ID do Cognito
        if event.get("requestContext", {}).get("authorizer", {}).get("claims"):
            user_id = event["requestContext"]["authorizer"]["claims"].get("sub")

      
        # Executar função principal
        resultado = listar_tarefas(data, user_id)


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
    