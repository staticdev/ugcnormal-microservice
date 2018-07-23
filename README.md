ugcnormal-microservice
======================

Microsserviço REST para normalização pt\_BR usando o
[UGCNormal](https://github.com/avanco/UGCNormal). Ideal para aplicações
que precisam de normalização online como chatbots.

Webservice baseado no ugcnormal\_interface
[](https://github.com/thiagootuler/ugcnormal_interface).

Requisitos
----------

-   Instalar Docker-CE 18.03.1+
-   900 Mb de espaço em disco para imagem

Execução
--------

Rodar os comandos:

``` {.sourceCode .sh}
# gerar a imagem
sudo docker build -t staticdev/ugcnormal:0.1.1 .
# verificar se gerou
sudo docker images
# instanciar imagem
sudo docker run --name ugcnormal -d -p 5000:5000 --env "UGCNORMAL=./ugc_norm/speller" staticdev/ugcnormal:0.1.1
# conferir processo rodando
sudo docker ps -a

# para parar o container olhe o nome dele no docker ps -a e execute
sudo docker stop ugcnormal
# para remover um container (precisa parar primeiro)
sudo docker rm ugcnormal
```

Exemplos de uso
---------------

Basta fazer um POST da mensagem a ser normalizada na url /reply passando
a mensagem no campo "message" e o método no campo "method".

Métodos disponíveis:

-   token: tokenizer
-   spell: speller
-   acronym: acronyms searcher
-   textese: untextese
-   proper\_noun: proper noun normalizer

A mensagem normalizada é retornada no campo "reply". O status da
requisição no campo "status", tendo com valor padrão para sucesso "ok".

Exemplo curl:

``` {.sourceCode .sh}
curl -X POST \
  http://localhost:5000/reply \
  -H 'content-type: application/json; charset=utf-8' \
  -d '{
    "message": "oi td bm?",
    "method": "spell"
}'
```

Exemplo python3 nativo (http.client):

``` {.sourceCode .python}
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
```
