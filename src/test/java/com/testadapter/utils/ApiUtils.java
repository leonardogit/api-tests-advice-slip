package com.testadapter.utils;

import io.restassured.RestAssured;
import io.restassured.response.Response;
import io.restassured.specification.RequestSpecification;

public class ApiUtils {

    public ApiUtils() {
        RestAssured.useRelaxedHTTPSValidation();
    }

    public Response get(String url) {
        return buildRequest()
                .when()
                .get(url)
                .then()
                .extract()
                .response();
    }

    public Response post(String url, String body) {
        return buildRequest()
                .body(body)
                .when()
                .post(url)
                .then()
                .extract()
                .response();
    }

    private RequestSpecification buildRequest() {
        return RestAssured.given()
                .relaxedHTTPSValidation()
                .header("Content-Type", "application/json");
    }
}
