#!/bin/bash

echo "Teste da rota sensor-data da API Node.js"
curl -X GET http://localhost:3000/sensor-data
echo -e "\n"
sleep 3

echo "Teste da rota alert da API Node.js e verificação na API Python (events)"
curl -X POST http://localhost:3000/alert \
  -H "Content-Type: application/json" \
  -d '{
        "type": "temperature",
        "value": 105.6,
        "message": "High temperature detected"
      }'
echo -e "\n"
sleep 1

curl -X GET http://localhost:5000/events
echo -e "\n"
sleep 3

echo "Teste da rota equipments da API PHP"
curl -X GET http://localhost:8000/equipments
echo -e "\n"
sleep 3

echo "Teste da rota dispatch da API PHP e verificação na API Python (via RabbitMQ)"
curl -X POST http://localhost:8000/dispatch \
  -H "Content-Type: application/json" \
  -d '{
        "equipment_id": 2,
        "priority": "high",
        "location": "Well A1",
        "message": "Crane needed for emergency operation"
      }'
echo -e "\n"
sleep 1

curl -X GET http://localhost:5000/events
echo -e "\n"

echo "Fim do teste"
read -p "Pressione Enter para continuar..."
