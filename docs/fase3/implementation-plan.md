# Plano de Implementação - Fase 3

## 🎯 **Visão Geral**

Este documento apresenta um plano prático e detalhado para implementar a Fase 3, considerando a estrutura atual do projeto e os requisitos específicos.

## 📋 **Análise da Estrutura Atual**

### **✅ Pontos Fortes Identificados:**
- Clean Architecture bem implementada
- FastAPI com SQLAlchemy funcionando
- Alembic para migrations
- Dockerfile funcional
- Manifests Kubernetes básicos
- Poetry para gerenciamento de dependências
- Estrutura modular e organizada

### **🔄 Pontos de Evolução:**
- Migração de PostgreSQL local para RDS
- Adição de autenticação JWT
- Implementação de CI/CD
- Separação em múltiplos repositórios
- Monitoramento e observabilidade

## 🚀 **Plano de Implementação Detalhado**

### **Fase 1: Preparação (Semana 1-2)**

#### **1.1 Configuração AWS**
```bash
# 1. Criar conta AWS
# 2. Configurar IAM User com permissões
aws configure
# 3. Criar S3 bucket para Terraform state
aws s3 mb s3://postech-terraform-state
# 4. Habilitar versionamento
aws s3api put-bucket-versioning --bucket postech-terraform-state --versioning-configuration Status=Enabled
```

#### **1.2 Criar Repositórios Separados**
```bash
# 1. postech-lambda-functions
git clone https://github.com/seu-usuario/postech-lambda-functions.git
cd postech-lambda-functions
# Estrutura inicial

# 2. postech-kubernetes-infra
git clone https://github.com/seu-usuario/postech-kubernetes-infra.git
cd postech-kubernetes-infra
# Copiar backend/k8s/ para kubernetes/

# 3. postech-database-infra
git clone https://github.com/seu-usuario/postech-database-infra.git
cd postech-database-infra
# Copiar backend/alembic/ para migrations/

# 4. postech-app (renomear backend atual)
git clone https://github.com/seu-usuario/postech-app.git
cd postech-app
# Copiar conteúdo do backend/ atual
```

#### **1.3 Configurar GitHub Actions**
Para cada repositório, criar `.github/workflows/deploy.yml` com:
- Proteção de branches
- Pull Request obrigatório
- Code review obrigatório
- Tests automatizados

### **Fase 2: Infraestrutura (Semana 3-4)**

#### **2.1 Database Infrastructure**
```bash
# postech-database-infra/
cd postech-database-infra

# Criar estrutura Terraform
mkdir -p terraform/{rds,vpc,subnet-groups}
touch terraform/main.tf
touch terraform/variables.tf
touch terraform/outputs.tf

# Implementar módulos
# 1. VPC com subnets públicas e privadas
# 2. RDS PostgreSQL em subnet privada
# 3. Security Groups restritivos
# 4. Parameter Groups otimizados
```

#### **2.2 Kubernetes Infrastructure**
```bash
# postech-kubernetes-infra/
cd postech-kubernetes-infra

# Criar estrutura Terraform
mkdir -p terraform/{eks,vpc,ecr}
touch terraform/main.tf
touch terraform/variables.tf

# Implementar módulos
# 1. EKS Cluster
# 2. ECR Repository
# 3. IAM Roles e Policies
# 4. Node Groups
```

#### **2.3 Deploy Infraestrutura**
```bash
# Deploy database primeiro
cd postech-database-infra
terraform init
terraform plan
terraform apply

# Deploy Kubernetes
cd ../postech-kubernetes-infra
terraform init
terraform plan
terraform apply
```

### **Fase 3: Lambda Functions (Semana 5)**

#### **3.1 Implementar Funções de Autenticação**
```python
# postech-lambda-functions/src/auth/authenticate.py
import json
import boto3
import jwt
from datetime import datetime, timedelta

def handler(event, context):
    try:
        body = json.loads(event['body'])
        cpf = body.get('cpf')
        
        # Validar CPF
        if not validate_cpf(cpf):
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'CPF inválido'})
            }
        
        # Buscar usuário no Cognito
        user = get_user_from_cognito(cpf)
        
        if user:
            # Gerar JWT
            token = generate_jwt(user)
            return {
                'statusCode': 200,
                'body': json.dumps({'token': token})
            }
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Usuário não encontrado'})
            }
            
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
```

#### **3.2 Configurar Cognito**
```bash
# Criar User Pool
aws cognito-idp create-user-pool \
    --pool-name postech-users \
    --policies PasswordPolicy={MinimumLength=8,RequireUppercase=false,RequireLowercase=false,RequireNumbers=false,RequireSymbols=false} \
    --auto-verified-attributes email

# Criar App Client
aws cognito-idp create-user-pool-client \
    --user-pool-id <user-pool-id> \
    --client-name postech-client \
    --no-generate-secret \
    --explicit-auth-flows ALLOW_USER_PASSWORD_AUTH ALLOW_REFRESH_TOKEN_AUTH
```

#### **3.3 Deploy Lambda Functions**
```bash
# postech-lambda-functions/
cd postech-lambda-functions

# Instalar Serverless Framework
npm install -g serverless

# Deploy
serverless deploy --stage production
```

### **Fase 4: Aplicação (Semana 6-7)**

#### **4.1 Evoluir Aplicação FastAPI**
```python
# postech-app/src/main.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from prometheus_client import Counter, Histogram
import time

# Métricas
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP request latency')

app = FastAPI(title="FastFood API", version="2.0.0")

# Middleware para métricas
@app.middleware("http")
async def add_metrics(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    
    REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path).inc()
    REQUEST_LATENCY.observe(duration)
    
    return response

# Endpoint de autenticação
@app.post("/auth")
async def authenticate(cpf: str):
    # Integração com Lambda/Cognito
    pass

# Middleware de autenticação
security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    # Validação JWT
    pass
```

#### **4.2 Atualizar Dependências**
```toml
# postech-app/pyproject.toml
[project]
dependencies = [
    # ... dependências existentes ...
    "boto3 (>=1.34.0)",
    "prometheus-client (>=0.19.0)",
    "structlog (>=23.2.0)",
    "python-jose[cryptography] (>=3.5.0,<4.0.0)"
]
```

#### **4.3 Otimizar Dockerfile**
```dockerfile
# postech-app/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instalar Poetry
RUN pip install --no-cache-dir poetry

# Copiar arquivos de dependências
COPY pyproject.toml poetry.lock* ./

# Instalar dependências
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Copiar código da aplicação
COPY . .

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### **4.4 Configurar CI/CD**
```yaml
# postech-app/.github/workflows/deploy.yml
name: Deploy Application

on:
  push:
    branches: [main, staging]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install Poetry
        run: pip install poetry
      - name: Install dependencies
        run: poetry install
      - name: Run tests
        run: poetry run pytest

  build-and-deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
          
      - name: Login to Amazon ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v1
        
      - name: Build and push Docker image
        env:
          ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
          ECR_REPOSITORY: postech-app
          IMAGE_TAG: ${{ github.sha }}
        run: |
          docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG .
          docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
          
      - name: Update Kubernetes deployment
        run: |
          aws eks update-kubeconfig --name postech-cluster --region us-east-1
          kubectl set image deployment/fastfood-app app=$ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
```

### **Fase 5: API Gateway (Semana 8)**

#### **5.1 Configurar API Gateway**
```bash
# Criar API Gateway
aws apigateway create-rest-api \
    --name postech-api \
    --description "API Gateway para FastFood"

# Configurar recursos e métodos
# 1. /auth (POST) -> Lambda authenticate
# 2. /validate (POST) -> Lambda validateJwt
# 3. /{proxy+} -> EKS Load Balancer
```

#### **5.2 Configurar Integração**
```yaml
# Configuração do API Gateway
Resources:
  ApiGatewayRestApi:
    Type: AWS::ApiGateway::RestApi
    Properties:
      Name: postech-api
      Description: API Gateway para FastFood

  ApiGatewayResource:
    Type: AWS::ApiGateway::Resource
    Properties:
      RestApiId: !Ref ApiGatewayRestApi
      ParentId: !GetAtt ApiGatewayRestApi.RootResourceId
      PathPart: '{proxy+}'

  ApiGatewayMethod:
    Type: AWS::ApiGateway::Method
    Properties:
      RestApiId: !Ref ApiGatewayRestApi
      ResourceId: !Ref ApiGatewayResource
      HttpMethod: ANY
      AuthorizationType: NONE
      Integration:
        Type: HTTP_PROXY
        IntegrationHttpMethod: ANY
        Uri: http://eks-load-balancer-url/{proxy}
```

### **Fase 6: Monitoramento (Semana 9)**

#### **6.1 Configurar Prometheus/Grafana**
```yaml
# postech-app/k8s/monitoring.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-config
data:
  prometheus.yml: |
    global:
      scrape_interval: 15s
    scrape_configs:
      - job_name: 'fastfood-app'
        static_configs:
          - targets: ['fastfood-app:8000']
        metrics_path: '/metrics'

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: prometheus
spec:
  replicas: 1
  selector:
    matchLabels:
      app: prometheus
  template:
    metadata:
      labels:
        app: prometheus
    spec:
      containers:
      - name: prometheus
        image: prom/prometheus
        ports:
        - containerPort: 9090
        volumeMounts:
        - name: config
          mountPath: /etc/prometheus
      volumes:
      - name: config
        configMap:
          name: prometheus-config
```

#### **6.2 Configurar Alertas**
```yaml
# CloudWatch Alarms
- CPU > 80% por 5 minutos
- Memory > 85% por 5 minutos
- Error rate > 5% por 1 minuto
- Response time > 2s por 1 minuto
- Database connections > 80%
```

### **Fase 7: Validação e Documentação (Semana 10)**

#### **7.1 Testes de Integração**
```bash
# Testar fluxo completo
# 1. Autenticação via CPF
curl -X POST https://api.postech.com/auth \
  -H "Content-Type: application/json" \
  -d '{"cpf":"12345678901"}'

# 2. Usar token para acessar API
curl -X GET https://api.postech.com/produtos \
  -H "Authorization: Bearer <token>"

# 3. Verificar métricas
curl https://app.postech.com/metrics
```

#### **7.2 Gravar Vídeo Demonstrativo**
- Mostrar arquitetura na AWS Console
- Demonstrar CI/CD pipelines
- Mostrar monitoramento e alertas
- Explicar escolhas de arquitetura

## 📊 **Cronograma Detalhado**

| Semana | Fase | Atividades | Entregáveis |
|--------|------|------------|-------------|
| 1-2 | Preparação | AWS, Repositórios, GitHub Actions | Estrutura base |
| 3-4 | Infraestrutura | RDS, EKS, ECR | Infraestrutura pronta |
| 5 | Lambda | Funções de autenticação | Autenticação funcionando |
| 6-7 | Aplicação | Evolução FastAPI, CI/CD | App em produção |
| 8 | API Gateway | Integração completa | API Gateway ativo |
| 9 | Monitoramento | Prometheus, Grafana, Alertas | Monitoramento ativo |
| 10 | Validação | Testes, Documentação, Vídeo | Projeto completo |

## 🔧 **Comandos Úteis**

### **AWS CLI**
```bash
# Configurar AWS
aws configure

# Verificar recursos
aws ec2 describe-instances
aws eks list-clusters
aws rds describe-db-instances

# Gerenciar secrets
aws secretsmanager create-secret --name "/postech/database/credentials" --secret-string '{"username":"postech","password":"secure"}'
```

### **Kubernetes**
```bash
# Configurar kubectl
aws eks update-kubeconfig --name postech-cluster --region us-east-1

# Verificar pods
kubectl get pods -n postech-fase2
kubectl logs deployment/fastfood-app

# Aplicar manifests
kubectl apply -f k8s/
```

### **Terraform**
```bash
# Inicializar
terraform init

# Planejar mudanças
terraform plan

# Aplicar mudanças
terraform apply

# Destruir recursos
terraform destroy
```

## 🎯 **Critérios de Sucesso**

### **Funcionais:**
- ✅ Autenticação por CPF funcionando
- ✅ API Gateway roteando requests
- ✅ Aplicação rodando no EKS
- ✅ Banco de dados no RDS
- ✅ CI/CD automatizado

### **Não Funcionais:**
- ✅ Response time < 2s
- ✅ Uptime > 99.9%
- ✅ Backup automático configurado
- ✅ Monitoramento ativo
- ✅ Segurança implementada

---

**Próximo**: Iniciar implementação da Fase 1
