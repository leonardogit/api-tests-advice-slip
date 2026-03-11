package com.testadapter.steps;

import com.testadapter.utils.ApiUtils;
import io.cucumber.java.pt.Dado;
import io.cucumber.java.pt.Entao;
import io.cucumber.java.pt.Quando;
import io.restassured.response.Response;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class GetAdviceStep {

    private ApiUtils apiUtils;
    private Response response;

    private ApiUtils getApiUtils() {
        return this.apiUtils == null ? new ApiUtils() : this.apiUtils;
    }

    @Dado("que a API de advice esta disponivel")
    public void queAApiDeAdviceEstaDisponivel() {
        apiUtils = getApiUtils();
    }

    @Quando("envio uma request do tipo get para o path {string}")
    public void envioUmaRequestDoTipoGetParaOPath(String path) {
        apiUtils = getApiUtils();
        String url = "https://api.adviceslip.com" + path;
        response = apiUtils.get(url);
    }

    @Entao("o status code da resposta deve ser {int}")
    public void oStatusCodeDaRespostaDeveSer(int statusCode) {
        assertEquals(statusCode, response.getStatusCode(),
                "Status code esperado: " + statusCode + ", recebido: " + response.getStatusCode());
    }
}
