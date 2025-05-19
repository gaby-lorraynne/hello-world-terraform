import boto3
import uuid
import os
import json

dynamodb = boto3.client('dynamodb', region_name='sa-east-1')
TABLE_NAME = os.environ.get('TABLE_NAME', 'ListaMercado')

def adicionar_item(nome, data):
    item_id = str(uuid.uuid4())
    pk = f"LIST#{data.replace('-', '')}"
    sk = f"ITEM#{item_id}" 

    item = {
        'PK': {'S': pk},
        'SK': {'S': sk},
        'name': {'S': nome},
        'date': {'S': data},
        'status': {'S': 'todo'},
        'itemId': {'S': item_id}
    }

    try:
        dynamodb.put_item(
            TableName=TABLE_NAME,
            Item=item,
            ConditionExpression='attribute_not_exists(PK) AND attribute_not_exists(SK)'
        )

        return {
            'message': 'Item criado com sucesso!',
            'PK': {'S': pk},
            'SK': {'S': sk},
            'name': {'S': nome},
            'date': {'S': data},
            'status': {'S': 'todo'},
            'itemId': {'S': item_id}
        }

    except dynamodb.exceptions.ConditionalCheckFailedException:
        raise Exception('Item já existe!')
    except Exception as e:
        raise Exception(f"Erro ao adicionar item: {str(e)}")
    
def lambda_handler(event, context):
    nome = event.get('nome')
    data = event.get('data')
    resultado = adicionar_item(nome, data)

    return {
        "statusCode": 200,
        "body": json.dumps(resultado, ensure_ascii=False)
    }