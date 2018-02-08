ugcnormal-microservice
======================

Microsserviço REST para normalização pt_BR usando o `UGCNormal <https://github.com/avanco/UGCNormal>`_. Ideal para aplicações que precisam de normalização online como chatbots.

Webservice baseado no ugcnormal_interface `<https://github.com/thiagootuler/ugcnormal_interface>`_.

Requisitos
----------

* Instalar Docker-CE 17.12.0+
* 900 Mb de espaço em disco para imagem

Execução
--------

Rodar os comandos:

.. code-block:: sh

  # gerar a imagem
  sudo docker build -t ugcnormal .
  # verificar se gerou
  sudo docker images
  # instanciar imagem
  sudo docker run --name ugcnormal -d -p 5000:5000 --env "UGCNORMAL=./ugc_norm/speller" ugcnormal
  # conferir processo rodando
  sudo docker ps -a
  
  # para parar o container olhe o nome dele no docker ps -a e execute
  sudo docker stop ugcnormal
  # para remover um container (precisa parar primeiro)
  sudo docker rm ugcnormal

Exemplos de uso
---------------

Basta fazer um POST da mensagem a ser normalizada na url /reply passando a mensagem no campo "message" e o método no campo "method".

Métodos disponíveis:

* token: tokenizer
* spell: speller
* acronym: acronyms searcher
* textese: untextese
* proper_noun: proper noun normalizer

A mensagem normalizada é retornada no campo "reply". O status da requisição no campo "status", tendo com valor padrão para sucesso "ok".

Exemplo curl:

.. code-block:: sh

  curl -X POST \
    http://localhost:5000/reply \
    -H 'content-type: application/json; charset=utf-8' \
    -d '{
      "message": "oi td bm?",
      "method": "spell"
  }'

Exemplo python3 nativo (http.client):

.. code-block:: python

  import http.client

  conn = http.client.HTTPConnection("localhost:5000")

  payload = "{\"message\": \"oi td bm?\", \"method\": \"spell\"}"

  headers = {
      'content-type': "application/json; charset=utf-8"
  }

  conn.request("POST", "/reply", payload, headers)
  res = conn.getresponse()
  data = res.read()

  print(data.decode("utf-8"))
