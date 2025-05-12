package com.example;

import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.RequestHandler;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.dynamodb.DynamoDbClient;
import software.amazon.awssdk.services.dynamodb.model.AttributeValue;
import software.amazon.awssdk.services.dynamodb.model.ConditionalCheckFailedException;
import software.amazon.awssdk.services.dynamodb.model.DynamoDbException;
import software.amazon.awssdk.services.dynamodb.model.PutItemRequest;

import java.util.HashMap;
import java.util.Map;
import java.util.UUID;

public class ListaMercadoService implements RequestHandler<Map<String, String>, Map<String, String>> {

    private static final String TABLE_NAME = "ListaMercado";
    private final DynamoDbClient dynamoDbClient;

    public ListaMercadoService() {
        this.dynamoDbClient = DynamoDbClient.builder()
                .region(Region.SA_EAST_1)
                .build();
    }

    public Map<String, String> adicionarItem(String nome, String data) {
        String itemId = UUID.randomUUID().toString();
        String pk = "LIST#" + data.replace("-", "");
        String sk = "ITEM#" + itemId;

        Map<String, AttributeValue> item = new HashMap<>();
        item.put("PK", AttributeValue.fromS(pk));
        item.put("SK", AttributeValue.fromS(sk));
        item.put("name", AttributeValue.fromS(nome));
        item.put("date", AttributeValue.fromS(data));
        item.put("status", AttributeValue.fromS("todo"));
        item.put("itemId", AttributeValue.fromS(itemId));

        PutItemRequest request = PutItemRequest.builder()
                .tableName(TABLE_NAME)
                .item(item)
                .conditionExpression("attribute_not_exists(PK) AND attribute_not_exists(SK)")
                .build();

        try {
            dynamoDbClient.putItem(request);
            System.out.println("Item adicionado com sucesso.");

            Map<String, String> resultado = new HashMap<>();
            resultado.put("message", "Item criado com sucesso");
            resultado.put("PK", pk);
            resultado.put("SK", sk);
            resultado.put("name", nome);
            resultado.put("date", data);
            resultado.put("status", "todo");
            resultado.put("itemId", itemId);
            return resultado;

        } catch (ConditionalCheckFailedException e) {
            throw new RuntimeException("Item já existe.", e);
        } catch (DynamoDbException e) {
            throw new RuntimeException("Erro ao adicionar item: " + e.getMessage(), e);
        }
    }

    @Override
    public Map<String, String> handleRequest(Map<String, String> input, Context context) {
        String nome = input.get("nome");
        String data = input.get("data");

        return adicionarItem(nome, data);
    }
}
