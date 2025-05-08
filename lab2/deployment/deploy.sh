#!/bin/bash

set -e  # Przerwij na błędzie
set -o pipefail

AWS_REGION="us-east-1"
ACCOUNT_ID="654654340788"
SERVICES=("booking-service" "cleaning-service" "dining-service" "accounting-service" "notification-service")

echo "🔐 Logowanie do ECR..."
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

for SERVICE in "${SERVICES[@]}"; do
  REPO_NAME=$SERVICE
  IMAGE_NAME="$ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$SERVICE:latest"

  echo "📦 Sprawdzanie istnienia repozytorium ECR: $REPO_NAME..."
  if ! aws ecr describe-repositories --repository-names "$REPO_NAME" --region $AWS_REGION &>/dev/null; then
    echo "🆕 Tworzenie repozytorium: $REPO_NAME"
    aws ecr create-repository --repository-name "$REPO_NAME" --region $AWS_REGION
  else
    echo "✅ Repozytorium $REPO_NAME już istnieje"
  fi

  echo "🔨 Budowanie obrazu Dockera dla $SERVICE..."
  docker build -t "$SERVICE" "../$SERVICE/$SERVICE"

  echo "🏷️ Tagowanie obrazu jako $IMAGE_NAME"
  docker tag "$SERVICE:latest" "$IMAGE_NAME"

  echo "🚀 Pushowanie obrazu do ECR..."
  docker push "$IMAGE_NAME"
done

echo "🌍 Wdrażanie infrastruktury z Terraform..."
terraform init
terraform apply -auto-approve

echo "✅ Wdrożenie zakończone pomyślnie!"
