#!/bin/bash

SERVICES=("booking-service" "cleaning-service" "dining-service" "accounting-service" "notification-service")
ACCOUNT_ID="654654340788"  # Add this line with your actual account ID

for SERVICE in "${SERVICES[@]}"
do
  aws ecr create-repository --repository-name $SERVICE --region us-east-1
  docker build -t $SERVICE ../$SERVICE/$SERVICE
  docker tag $SERVICE:latest $ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/$SERVICE:latest
  aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com
  docker push $ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/$SERVICE:latest
done