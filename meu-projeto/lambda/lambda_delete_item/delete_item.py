import boto3
import os
import json

dynamodb = boto3.client('dynamodb', region_name='sa-east-1')
TABLE_NAME = os.environ.get('TABELA_LISTA', 'ListaMercado')

def lambda_handler(event, context):
    pk = event.get("pk")
    sk = event.get("sk")


    if not pk or not sk:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "status": "error",
                "message": "Parâmetros 'pk' e 'sk' são obrigatórios."
            }, ensure_ascii=False)
        }

    full_pk = f"LIST#{pk}"
    full_sk = f"ITEM#{sk}"

    try:
        result = dynamodb.delete_item(
            TableName=TABLE_NAME,
            Key={
                'PK': {'S': full_pk},
                'SK': {'S': full_sk}
            },
            ReturnValues="ALL_OLD"
        )

        if 'Attributes' not in result:
            return {
                "statusCode": 404,
                "body": json.dumps({
                    "status": "not_found",
                    "message": "Item não existia na tabela."
                }, ensure_ascii=False)
            }
        else:
            return {
                "statusCode": 200,
                "body": json.dumps({
                    "status": "success",
                    "message": "Item excluído com sucesso."
                }, ensure_ascii=False)
            }

    except dynamodb.exceptions.ResourceNotFoundException as e:
        return {
                "statusCode": 500,
                "body": json.dumps({
                    "status": "error",
                    "message": f"Tabela não encontrada: {str(e)}"
                }, ensure_ascii=False)
            }
    except Exception as e:
        return {
                "statusCode": 500,
                "body": json.dumps({
                    "status": "error",
                    "message": f"Erro ao excluir item: {str(e)}"
                }, ensure_ascii=False)
            }
