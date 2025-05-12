package com.example;

import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.RequestHandler;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.dynamodb.DynamoDbClient;
import software.amazon.awssdk.services.dynamodb.model.AttributeValue;
import software.amazon.awssdk.services.dynamodb.model.DeleteItemRequest;
import software.amazon.awssdk.services.dynamodb.model.DeleteItemResponse;
import software.amazon.awssdk.services.dynamodb.model.ResourceNotFoundException;

import java.util.HashMap;
import java.util.Map;

public class RemoverItemService implements RequestHandler<Map<String, Object>, Map<String, Object>> {

    private final DynamoDbClient dynamoDbClient = DynamoDbClient.builder()
            .region(Region.SA_EAST_1)
            .build();

    private final String tableName = System.getenv("TABELA_LISTA");

    @Override
    public Map<String, Object> handleRequest(Map<String, Object> input, Context context) {
        String pk = "LIST#" + input.get("pk");
        String sk = "ITEM#" + input.get("sk");

        Map<String, Object> response = new HashMap<>();

        try {
            Map<String, AttributeValue> key = new HashMap<>();
            key.put("PK", AttributeValue.builder().s(pk).build());
            key.put("SK", AttributeValue.builder().s(sk).build());

            DeleteItemRequest request = DeleteItemRequest.builder()
                    .tableName(tableName)
                    .key(key)
                    .returnValues("ALL_OLD")
                    .build();

            DeleteItemResponse result = dynamoDbClient.deleteItem(request);

            if (result.attributes().isEmpty()) {
                response.put("status", "not_found");
                response.put("message", "Item não existia na tabela.");
            } else {
                response.put("status", "success");
                response.put("message", "Item excluído com sucesso.");
            }

            return response;

        } catch (ResourceNotFoundException e) {
            response.put("status", "error");
            response.put("message", "Tabela não encontrada: " + e.getMessage());
            return response;
        } catch (Exception e) {
            response.put("status", "error");
            response.put("message", "Erro ao excluir item: " + e.getMessage());
            return response;
        }
    }
}
