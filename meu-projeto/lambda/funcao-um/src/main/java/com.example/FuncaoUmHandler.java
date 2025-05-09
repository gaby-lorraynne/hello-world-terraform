package com.example;

import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.RequestHandler;

import java.util.Map;
import java.util.HashMap;

public class FuncaoUmHandler implements RequestHandler<Object, Map<String, Object>> {
    @Override
   public Map<String, Object> handleRequest(Object input, Context context) {
        context.getLogger().log("Recebido: " + input);

        Map<String, Object> response = new HashMap<>();
        response.put("statusCode", 200);
        response.put("body", "Hello Terraform");

        return response;
    }
}
