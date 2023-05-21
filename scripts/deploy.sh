#! /usr/bin/env sh

# Exit in case of error
set -e

DOMAIN=${DOMAIN?Variable not set} \
TRAEFIK_TAG=${TRAEFIK_TAG?Variable not set} \
STACK_NAME=${STACK_NAME?Variable not set} \
TAG=${TAG?Variable not set} \
docker-compose \
-f docker-compose.yml \
config > docker-stack.yml

docker-auto-labels docker-stack.yml

docker stack deploy -c docker-stack.yml --with-registry-auth "${STACK_NAME?Variable not set}"


eksctl create cluster --name asap-api --region us-east-1 --fargate
kubectl create namespace eks-asap-api-app
kubectl apply -f eks-asap-deployment.yaml
kubectl apply -f eks-asap-api-service.yaml


kubectl get all -n eks-asap-api-app

aws ecr create-repository --region us-east-1 --repository-name eks-asap-api
