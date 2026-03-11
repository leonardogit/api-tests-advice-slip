# language: pt

Funcionalidade: Consultar Advice Slip API

  @get_advice
  Cenario: Validar GET advice retorna status code 200
    Dado que a API de advice esta disponivel
    Quando envio uma request do tipo get para o path "/advice"
    Entao o status code da resposta deve ser 200
