# 🐳 Kubernetes - FastFood API

Arquitetura Kubernetes para o sistema de autoatendimento FastFood - Tech Challenge FIAP.

## 📋 Arquitetura

### 🏗️ Componentes

| Arquivo | Função | Descrição |
|---------|--------|-----------|
| `namespace.yaml` | Namespace | Isolamento de recursos |
| `configmap.yaml` | ConfigMap | Variáveis de ambiente não sensíveis |
| `secret.yaml` | Secret | Dados sensíveis (senhas, chaves) |
| `app-deployment.yaml` | Deployment + Service | Aplicação FastAPI |
| `postgres-deployment.yaml` | Database | PostgreSQL com volume persistente |
| `hpa.yaml` | HPA | Escalabilidade automática |
| `ingress.yaml` | Ingress | Roteamento HTTP |
| `kustomization.yaml` | Kustomize | Orquestração de recursos |

### ⚡ Escalabilidade (HPA)

- **Mínimo**: 2 réplicas (disponibilidade)
- **Máximo**: 10 réplicas (picos de demanda)
- **CPU**: Escala em 70% de utilização
- **Memory**: Escala em 80% de utilização
- **Scale Up**: 60s (resposta rápida)
- **Scale Down**: 300s (estabilidade)

### 🔒 Segurança

- **Namespace isolado**: `postech-fase2`
- **ConfigMap**: Variáveis de ambiente
- **Secret**: Senhas e chaves JWT
- **Health Checks**: Liveness e Readiness probes

## 🚀 Como Deployar

### 1. Pré-requisitos
```bash
# Minikube
minikube start

# Ou cluster Kubernetes
kubectl cluster-info
```

### 2. Build da Imagem
```bash
# Build local
docker build -t postech-app:latest ./backend

# Carregar no Minikube
minikube image load postech-app:latest
```

### 3. Deploy
```bash
# Aplicar todos os recursos
kubectl apply -k backend/k8s/

# Verificar status
kubectl get all -n postech-fase2
```

### 4. Acesso
```bash
# Port forward para acesso local
kubectl port-forward -n postech-fase2 svc/postech-app-service 8000:80

# Acesse: http://localhost:8000
```

## 📊 Monitoramento

### Verificar HPA
```bash
kubectl get hpa -n postech-fase2
kubectl describe hpa postech-app-hpa -n postech-fase2
```

### Verificar Pods
```bash
kubectl get pods -n postech-fase2
kubectl logs -f deployment/postech-app-deployment -n postech-fase2
```

### Verificar Recursos
```bash
kubectl top pods -n postech-fase2
kubectl top nodes
```

## 🔧 Configurações

### Variáveis de Ambiente
- **ConfigMap**: `DATABASE_URL`, `POSTGRES_DB`, `POSTGRES_USER`
- **Secret**: `POSTGRES_PASSWORD`, `SECRET_KEY`

### Recursos
- **CPU**: 500m-1000m (0.5-1 core)
- **Memory**: 512Mi-1Gi
- **Storage**: 1Gi PostgreSQL

## 🎯 Requisitos Atendidos

✅ **Funcionalidades**: API completa com database  
✅ **Escalabilidade**: HPA com métricas CPU/Memory  
✅ **Segurança**: ConfigMap + Secret + Namespace  
✅ **Arquitetura**: Boas práticas Kubernetes  
✅ **Documentação**: Manifests no GitHub  

## 📈 Próximos Passos

1. **Produção**: Configurar registry de imagens
2. **Monitoramento**: Prometheus + Grafana
3. **Logs**: ELK Stack ou similar
4. **CI/CD**: GitHub Actions ou Jenkins
5. **SSL**: Certificados automáticos (Let's Encrypt) 