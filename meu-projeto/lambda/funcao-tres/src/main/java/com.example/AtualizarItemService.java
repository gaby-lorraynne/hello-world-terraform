package com.example;

import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.RequestHandler;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.dynamodb.DynamoDbClient;
import software.amazon.awssdk.services.dynamodb.model.*;

import java.util.HashMap;
import java.util.Map;


public class AtualizarItemService implements RequestHandler<Map<String, String>, Map<String, String>> {

    private static final String TABLE_NAME = "ListaMercado";
    private final DynamoDbClient dynamoDbClient;

    public AtualizarItemService() {
        this.dynamoDbClient = DynamoDbClient.builder()
                .region(Region.SA_EAST_1)
                .build();
    }

    @Override
    public Map<String, String> handleRequest(Map<String, String> input, Context context) {
        String data = input.get("data");
        String itemId = input.get("itemId");

        String pk = "LIST#" + data.replace("-", "");
        String sk = "ITEM#" + itemId;

        // Verifica se o item existe
        GetItemRequest getRequest = GetItemRequest.builder()
                .tableName(TABLE_NAME)
                .key(Map.of(
                        "PK", AttributeValue.fromS(pk),
                        "SK", AttributeValue.fromS(sk)
                ))
                .build();

        GetItemResponse getResponse = dynamoDbClient.getItem(getRequest);
        if (!getResponse.hasItem()) {
            throw new RuntimeException("Item não encontrado.");
        }

        // Atualizar
        Map<String, AttributeValueUpdate> atualizar = new HashMap<>();
        if (input.containsKey("name")) {
            atualizar.put("name", AttributeValueUpdate.builder()
                    .value(AttributeValue.fromS(input.get("name")))
                    .action(AttributeAction.PUT)
                    .build());
        }

        if (input.containsKey("status")) {
            atualizar.put("status", AttributeValueUpdate.builder()
                    .value(AttributeValue.fromS(input.get("status")))
                    .action(AttributeAction.PUT)
                    .build());
        }

        UpdateItemRequest updateRequest = UpdateItemRequest.builder()
                .tableName(TABLE_NAME)
                .key(Map.of(
                        "PK", AttributeValue.fromS(pk),
                        "SK", AttributeValue.fromS(sk)
                ))
                .attributeUpdates(atualizar)
                .returnValues(ReturnValue.ALL_NEW)
                .build();

        UpdateItemResponse updateResponse = dynamoDbClient.updateItem(updateRequest);

        // Constrói retorno
        Map<String, String> resultado = new HashMap<>();
        updateResponse.attributes().forEach((k, v) -> resultado.put(k, v.s()));
        resultado.put("message", "Item atualizado com sucesso");

        return resultado;
    }
}
