# Arquitetura da Fase 3

## 🏗️ **Visão Geral da Arquitetura**

A Fase 3 implementa uma arquitetura moderna baseada em microserviços e serverless, distribuída em múltiplos repositórios com CI/CD automatizado, evoluindo a estrutura atual do projeto.

## 🎯 **Escolha da Cloud: AWS**

**Justificativa**: AWS oferece a maior maturidade em serviços serverless e melhor integração entre os componentes necessários.

### **Serviços AWS Utilizados:**
- **API Gateway**: Roteamento e autenticação
- **Lambda**: Funções serverless para autenticação
- **Cognito**: Sistema de autenticação
- **RDS PostgreSQL**: Banco de dados gerenciado (evolui do PostgreSQL atual)
- **EKS**: Kubernetes gerenciado (evolui do k8s atual)
- **ECR**: Registry de containers
- **VPC**: Rede isolada
- **Secrets Manager**: Gerenciamento de secrets

## 📊 **Diagrama da Arquitetura**

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENTE                                 │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                    API GATEWAY                                 │
│  • Roteamento de requests                                      │
│  • Autenticação JWT                                            │
│  • Rate limiting                                               │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                    LAMBDA FUNCTIONS                            │
│  • Autenticação por CPF                                        │
│  • Validação de JWT                                            │
│  • Consulta Cognito                                            │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                    COGNITO                                     │
│  • Pool de usuários                                            │
│  • Autenticação sem senha                                      │
│  • Geração de JWT                                              │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                    EKS CLUSTER                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   FastAPI App   │  │   Monitoring    │  │   Load Balancer │ │
│  │   (Pods)        │  │   (Prometheus)  │  │   (Ingress)     │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────┬───────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                    RDS POSTGRESQL                              │
│  • Banco de dados principal                                    │
│  • Backup automático                                           │
│  • Multi-AZ deployment                                         │
└─────────────────────────────────────────────────────────────────┘
```

## 🗂️ **Estrutura de Repositórios**

### **1. Repositório: `postech-lambda-functions`**
```
📦 postech-lambda-functions
├── 📁 src/
│   ├── 📁 auth/
│   │   ├── 📄 authenticate.py
│   │   └── 📄 validate_jwt.py
│   └── 📁 utils/
│       └── 📄 cognito_client.py
├── 📁 tests/
├── 📄 requirements.txt
├── 📄 serverless.yml
└── 📄 .github/workflows/deploy.yml
```

### **2. Repositório: `postech-kubernetes-infra`**
```
📦 postech-kubernetes-infra
├── 📁 terraform/
│   ├── 📁 eks/
│   ├── 📁 vpc/
│   ├── 📁 security-groups/
│   └── 📁 variables.tf
├── 📁 kubernetes/
│   ├── 📁 deployments/ (Evoluído do backend/k8s/)
│   ├── 📁 services/
│   └── 📁 ingress/
└── 📄 .github/workflows/deploy.yml
```

### **3. Repositório: `postech-database-infra`**
```
📦 postech-database-infra
├── 📁 terraform/
│   ├── 📁 rds/
│   ├── 📁 subnet-groups/
│   ├── 📁 parameter-groups/
│   └── 📁 variables.tf
├── 📁 migrations/ (Evoluído do backend/alembic/)
└── 📄 .github/workflows/deploy.yml
```

### **4. Repositório: `postech-app` (atual backend)**
```
📦 postech-app
├── 📁 src/clean_architecture/ (Mantido)
├── 📁 docker/
├── 📄 Dockerfile (Otimizado)
├── 📄 pyproject.toml (Atualizado)
└── 📄 .github/workflows/deploy.yml (Novo)
```

## 🔄 **Migração da Estrutura Atual**

### **1. Aplicação FastAPI (backend/)**
**Atual:**
- ✅ Clean Architecture implementada
- ✅ FastAPI com SQLAlchemy
- ✅ Alembic para migrations
- ✅ Dockerfile funcional
- ✅ Manifests Kubernetes básicos

**Evolução para Fase 3:**
- 🔄 Adicionar autenticação JWT
- 🔄 Integrar com API Gateway
- 🔄 Otimizar Dockerfile para produção
- 🔄 Adicionar monitoramento (Prometheus/Grafana)
- 🔄 Configurar health checks avançados

### **2. Banco de Dados**
**Atual:**
- ✅ PostgreSQL local/Docker
- ✅ Alembic migrations
- ✅ SQLAlchemy ORM
- ✅ Modelos de dados definidos

**Evolução para Fase 3:**
- 🔄 Migrar para RDS PostgreSQL
- 🔄 Configurar backup automático
- 🔄 Implementar replicação
- 🔄 Configurar monitoramento

### **3. Kubernetes**
**Atual:**
- ✅ Manifests básicos em `backend/k8s/`
- ✅ Deployment, Service, Ingress
- ✅ ConfigMaps e Secrets
- ✅ HPA configurado

**Evolução para Fase 3:**
- 🔄 Migrar para EKS
- 🔄 Terraform para infraestrutura
- 🔄 Configurar ECR
- 🔄 Implementar CI/CD

## 🔐 **Fluxo de Autenticação**

### **1. Cliente faz login com CPF**
```
Cliente → API Gateway → Lambda → Cognito → JWT Token
```

### **2. Validação de requests**
```
Cliente → API Gateway → Lambda (valida JWT) → Aplicação
```

### **3. Integração com Aplicação Existente**
```python
# Evolução do backend/src/clean_architecture/api/
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    # Validação JWT via Lambda/Cognito
    user = await validate_jwt_token(credentials.credentials)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    return user
```

## 🚀 **CI/CD Pipeline**

### **Fluxo de Deploy:**
1. **Desenvolvimento**: Branch `feature/*`
2. **Pull Request**: `feature/*` → `develop`
3. **Staging**: `develop` → `staging` (deploy automático)
4. **Produção**: `staging` → `main` (deploy automático)

### **Proteção de Branches:**
- ✅ `main` e `staging` protegidas
- ✅ Pull Request obrigatório
- ✅ Code review obrigatório
- ✅ Tests obrigatórios
- ✅ Terraform plan obrigatório

## 📈 **Monitoramento e Observabilidade**

### **Stack de Monitoramento:**
- **Prometheus**: Métricas da aplicação
- **Grafana**: Dashboards
- **Jaeger**: Distributed tracing
- **ELK Stack**: Logs centralizados

### **Integração com Estrutura Atual:**
```python
# Adicionar ao backend/src/main.py
from prometheus_client import Counter, Histogram
import time

# Métricas
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP request latency')

@app.middleware("http")
async def add_metrics(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    
    REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path).inc()
    REQUEST_LATENCY.observe(duration)
    
    return response
```

## 🔒 **Segurança**

### **Medidas Implementadas:**
- ✅ VPC isolada
- ✅ Security Groups restritivos
- ✅ Secrets Manager para credenciais
- ✅ IAM roles com menor privilégio
- ✅ WAF no API Gateway
- ✅ Encryption em trânsito e repouso

### **Evolução da Segurança Atual:**
```yaml
# Evolução do backend/k8s/secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: postech-app-secret
  namespace: postech-fase2
type: Opaque
data:
  # Migrar para AWS Secrets Manager
  POSTGRES_PASSWORD: <base64-encoded>
  SECRET_KEY: <base64-encoded>
  JWT_SECRET: <base64-encoded>
  COGNITO_CLIENT_ID: <base64-encoded>
```

## 💰 **Estimativa de Custos**

### **Serviços AWS (estimativa mensal):**
- **API Gateway**: $1-5
- **Lambda**: $1-3
- **Cognito**: $1-2
- **EKS**: $73 (3 nodes t3.medium)
- **RDS**: $25-50 (db.t3.micro)
- **ECR**: $1-2
- **Total estimado**: $100-135/mês

## 🔧 **Plano de Implementação**

### **Fase 1: Preparação (1-2 semanas)**
1. ✅ Documentação da arquitetura
2. 🔄 Configurar AWS account
3. 🔄 Criar repositórios separados
4. 🔄 Configurar GitHub Actions

### **Fase 2: Infraestrutura (2-3 semanas)**
1. 🔄 Deploy RDS PostgreSQL
2. 🔄 Deploy EKS Cluster
3. 🔄 Configurar ECR
4. 🔄 Configurar API Gateway

### **Fase 3: Aplicação (2-3 semanas)**
1. 🔄 Deploy Lambda Functions
2. 🔄 Migrar aplicação para EKS
3. 🔄 Configurar autenticação
4. 🔄 Configurar monitoramento

### **Fase 4: Validação (1 semana)**
1. 🔄 Testes de integração
2. 🔄 Configurar alertas
3. 🔄 Documentar arquitetura
4. 🔄 Gravar vídeo demonstrativo

---

**Próximo**: Implementar Lambda Functions e configurar CI/CD
