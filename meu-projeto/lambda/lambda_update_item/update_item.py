import boto3
import os
import json

dynamodb = boto3.client('dynamodb', region_name='sa-east-1')
TABLE_NAME = os.environ.get('TABLE_NAME', 'ListaMercado')

def lambda_handler(event, context):
    data = event.get("data")
    item_id = event.get("itemId")

    if not data or not item_id:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Os parâmetros 'data' e 'itemId' são obrigatórios!"}, ensure_ascii=False)
        }
    
    pk = f"LIST#{data.replace('-', '')}"
    sk = f"ITEM#{item_id}"


    # Verificar a presença do item
    response = dynamodb.get_item(
        TableName=TABLE_NAME,
        Key={
            'PK': {'S': pk},
            'SK': {'S': sk}
        }
    )

    if 'Item' not in response:
        return {
                "statusCode": 404,
                "body": json.dumps({"message": "Item não encontrado."}, ensure_ascii=False)
            }

    # Atributos a atualizar
    expression_attributes_values = {}
    expression_attributes_names = {}
    update_expression = []

    if "name" in event:
        update_expression.append("#n = :name")
        expression_attributes_values[":name"] = {'S': event["name"]}
        expression_attributes_names["#n"] = "name"

    if "status" in event:
        update_expression.append("#s = :status")
        expression_attributes_values[":status"] = {'S': event["status"]}
        expression_attributes_names["#s"] = "status"

    if not update_expression:
        return {
                "statusCode": 400,
                "body": json.dumps({"message": "Nenhum atributo para atualizar."}, ensure_ascii=False)
            }

    # Atualizar o item
    if update_expression:
        update_response = dynamodb.update_item(
            TableName=TABLE_NAME,
            Key={
                'PK': {'S': pk},
                'SK': {'S': sk}
            },
            UpdateExpression="SET " + ", ".join(update_expression),
            ExpressionAttributeValues=expression_attributes_values,
            ExpressionAttributeNames=expression_attributes_names,
            ReturnValues="ALL_NEW"
        )

    # Retorno
    updated_attributes = update_response.get("Attributes", {})
    result = {key: value.get("S", "") for key, value in updated_attributes.items()}
    result["message"] = "Item atualizado com sucesso!"

    return {
        "statusCode": 200,
        "body": json.dumps(result, ensure_ascii=False)
    }
