# intsistemas-a2
Prova A2 de Integração de Sistemas

## API eventos
### Como rodar
No dir api_eventos, rode o container docker pelo shell-script:
```
./docker_api_python.sh
```

### Objetivo
Feito em Python, 
Recebe os eventos via API na rota POST /events.
E também recebe eventos via mensageria RabbitMQ na queue php_events.
Salva-os em cache no redis (TTL 5 min) e em uma lista interna.
Ao chamar a rota GET /events os eventos são enviados, recuperando-os do cache ou da lista interna.


## API Logistica
### Como rodar
No dir api_logistica, rode o container docker via shell-script:
```
./docker_api_php.sh
```

### Objetivo
Feito em PHP,
Ao chamar a rota GET /equipments, retorna um json contendo um array de equipamentos hard coded.
Ao chamar a rota POST /dispatch, manda um evento para a API de Eventos via mensageria Rabbit MQ na queue php_events.

## API Sensores
### Como rodar
No dir api_sensores, rode o comando:
```
node app.js
```

### Objetivo
Feito em Node.js,
Ao chamar a rota GET /sensor-data, retorna um JSON com informações de um sensor, a informação é recuperada do cache Redis (TTL 60s), ou caso a chave não exista no redis, o conteúdo do Array hard coded é retornado.
Ao chamar a rota POST /alert, envia um alerta para a API Python, via HTTP, o conteúdo enviado para a API Python é o mesmo do que você enviou na POST /alert.

## EXTRA: Shell-Script para testar as rotas das APIs
Criei um .sh para testar todas as rotas da API.
No root do repositório, rode:
```
./test.sh
```

E também, há um .sh para rodar um container RabbitMQ.
```
./docker_rabbitmq.sh
```

### Resultado esperado do test.sh
```
Teste da rota sensor-data da API Node.js
{"temperature":"23.92","pressure":"1000.24","timestamp":"2025-05-28T23:58:41.226Z"}

Teste da rota alert da API Node.js e verificação na API Python (events)
{"status":"Alert sent","response":{"event":{"data":{"message":"High temperature detected","type":"temperature","value":105.6},"id":1,"timestamp":"2025-05-28 23:59:47"},"status":"Event received"}}

[{"data":{"message":"High temperature detected","type":"temperature","value":105.6},"id":1,"timestamp":"2025-05-28 23:59:47"}]


Teste da rota equipments da API PHP
[{"id":1,"name":"Forklift"},{"id":2,"name":"Crane"},{"id":3,"name":"Conveyor Belt"}]

Teste da rota dispatch da API PHP e verificação na API Python (via RabbitMQ)
{"status":"Message dispatched"}

[{"data":{"message":"High temperature detected","type":"temperature","value":105.6},"id":1,"timestamp":"2025-05-28 23:59:47"},{"data":{"equipment_id":2,"location":"Well A1","message":"Crane needed for emergency operation","priority":"high"},"id":2,"source":"PHP","timestamp":"2025-05-28 23:59:54"}]


Fim do teste
Pressione Enter para continuar...
```