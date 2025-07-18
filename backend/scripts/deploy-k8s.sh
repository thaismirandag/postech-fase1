#!/bin/bash

# Script para deploy da aplicação no Kubernetes
set -e

echo "Iniciando deploy no Kubernetes..."

# Build da imagem de produção
echo "Build da imagem de produção..."
docker build -f backend/Dockerfile.prod -t postech-app:latest ./backend

# Aplicar recursos Kubernetes
echo "Aplicando recursos Kubernetes..."
kubectl apply -k backend/k8s/

# Aguardar os pods ficarem prontos
echo "Aguardando pods ficarem prontos..."
kubectl wait --for=condition=ready pod -l app=postech-app -n ${K8S_NAMESPACE:-postech-fase2} --timeout=300s
kubectl wait --for=condition=ready pod -l app=postgres -n ${K8S_NAMESPACE:-postech-fase2} --timeout=300s

# Executar migrações
echo "Executando migrações..."
kubectl exec -n ${K8S_NAMESPACE:-postech-fase2} deployment/postech-app-deployment -- alembic upgrade head

echo "Deploy concluído com sucesso!"
echo "Para acessar a aplicação:"
echo "kubectl port-forward -n ${K8S_NAMESPACE:-postech-fase2} svc/postech-app-service 8080:80"
echo "Acesse: http://localhost:8080" 