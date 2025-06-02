#!/bin/bash

set -e

STACK_NAME="hotel"

echo "▶️ Usuwanie istniejącego stacka: $STACK_NAME..."
docker stack rm "$STACK_NAME"

# Czekaj aż stack zostanie całkowicie usunięty
echo "⏳ Czekam na usunięcie stacka..."
while docker stack ls | grep -q "$STACK_NAME"; do
  sleep 1
done
echo "✅ Stack usunięty."

echo "🔨 Budowanie obrazów..."
docker build -t booking-service:latest booking-service/booking-service
docker build -t cleaning-service:latest cleaning-service/cleaning-service
docker build -t dining-service:latest dining-service/dining-service
docker build -t accounting-service:latest accounting-service/accounting-service
docker build -t notification-service:latest notification-service/notification-service

echo "🚀 Wdrażanie stacka $STACK_NAME..."
docker stack deploy -c docker-compose.yml "$STACK_NAME"

echo "📋 Lista usług:"
docker service ls
