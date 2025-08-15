# Guia de Deployment - Fase 3

## 🚀 **Visão Geral do Deployment**

Este guia descreve o processo de deployment da arquitetura completa da Fase 3, incluindo todos os repositórios e suas integrações, evoluindo a estrutura atual do projeto.

## 📋 **Pré-requisitos**

### **1. Conta AWS**
- ✅ Conta AWS ativa
- ✅ IAM User com permissões adequadas
- ✅ AWS CLI configurado
- ✅ Terraform instalado (v1.0+)

### **2. GitHub**
- ✅ Conta GitHub
- ✅ 4 repositórios criados
- ✅ GitHub Actions habilitado
- ✅ Secrets configurados

### **3. Ferramentas Locais**
```bash
# Instalar ferramentas necessárias
brew install terraform kubectl awscli
# ou
sudo apt install terraform kubectl awscli
```

## 🗂️ **Estrutura de Repositórios**

### **Repositórios Necessários:**
1. `postech-lambda-functions` - Funções serverless
2. `postech-kubernetes-infra` - Infraestrutura EKS
3. `postech-database-infra` - Infraestrutura RDS
4. `postech-app` - Aplicação principal (evolução do atual `backend/`)

## 🔧 **Configuração Inicial**

### **1. Configurar AWS Credentials**
```bash
aws configure
# AWS Access Key ID: [sua-access-key]
# AWS Secret Access Key: [sua-secret-key]
# Default region name: us-east-1
# Default output format: json
```

### **2. Configurar GitHub Secrets**
Para cada repositório, adicionar os seguintes secrets:

```yaml
# Secrets necessários
AWS_ACCESS_KEY_ID: [sua-access-key]
AWS_SECRET_ACCESS_KEY: [sua-secret-key]
AWS_REGION: us-east-1
DOCKER_USERNAME: [seu-docker-username]
DOCKER_PASSWORD: [seu-docker-password]
```

## 📦 **Deployment por Repositório**

### **1. Repositório: `postech-database-infra`**

#### **Estrutura do Terraform:**
```hcl
# main.tf
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  backend "s3" {
    bucket = "postech-terraform-state"
    key    = "database/terraform.tfstate"
    region = "us-east-1"
  }
}

provider "aws" {
  region = var.aws_region
}

# VPC e Subnets
module "vpc" {
  source = "./modules/vpc"
  # ... configurações
}

# RDS PostgreSQL
module "rds" {
  source = "./modules/rds"
  # ... configurações
}
```

#### **GitHub Actions Workflow:**
```yaml
# .github/workflows/deploy.yml
name: Deploy Database Infrastructure

on:
  push:
    branches: [main, staging]
  pull_request:
    branches: [main]

jobs:
  terraform:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v2
        
      - name: Terraform Init
        run: terraform init
        
      - name: Terraform Plan
        run: terraform plan
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          
      - name: Terraform Apply
        if: github.ref == 'refs/heads/main'
        run: terraform apply -auto-approve
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
```

### **2. Repositório: `postech-kubernetes-infra`**

#### **Estrutura do Terraform:**
```hcl
# main.tf
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  backend "s3" {
    bucket = "postech-terraform-state"
    key    = "kubernetes/terraform.tfstate"
    region = "us-east-1"
  }
}

# EKS Cluster
module "eks" {
  source = "./modules/eks"
  # ... configurações
}

# ECR Repository
module "ecr" {
  source = "./modules/ecr"
  # ... configurações
}
```

#### **Kubernetes Manifests (Evoluído do backend/k8s/):**
```yaml
# kubernetes/deployments/app.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastfood-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: fastfood-app
  template:
    metadata:
      labels:
        app: fastfood-app
    spec:
      containers:
      - name: app
        image: ${ECR_REPO}:${IMAGE_TAG}
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
        - name: AWS_REGION
          value: us-east-1
        resources:
          limits:
            memory: "1Gi"
            cpu: "1000m"
          requests:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 60
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
```

### **3. Repositório: `postech-lambda-functions`**

#### **Estrutura do Serverless:**
```yaml
# serverless.yml
service: postech-auth-functions

provider:
  name: aws
  runtime: python3.9
  region: us-east-1
  environment:
    COGNITO_USER_POOL_ID: ${ssm:/postech/cognito/user-pool-id}
    COGNITO_CLIENT_ID: ${ssm:/postech/cognito/client-id}

functions:
  authenticate:
    handler: src/auth/authenticate.handler
    events:
      - http:
          path: /auth
          method: post
          cors: true
          
  validateJwt:
    handler: src/auth/validate_jwt.handler
    events:
      - http:
          path: /validate
          method: post
          cors: true
```

#### **GitHub Actions Workflow:**
```yaml
# .github/workflows/deploy.yml
name: Deploy Lambda Functions

on:
  push:
    branches: [main, staging]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          
      - name: Install Serverless Framework
        run: npm install -g serverless
        
      - name: Deploy to AWS
        run: serverless deploy --stage ${{ github.ref_name }}
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
```

### **4. Repositório: `postech-app` (evolução do backend atual)**

#### **Dockerfile Otimizado (evolução do atual):**
```dockerfile
# Dockerfile
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

# Expor porta
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Comando de inicialização
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### **pyproject.toml Atualizado (evolução do atual):**
```toml
[project]
name = "backend"
version = "0.1.0"
description = ""
authors = [
    {name = "Thais Gomes",email = "thaismrgs@gmail.com"}
]
readme = "README.md"
requires-python = ">=3.11"
package-mode = false

dependencies = [
    "fastapi (==0.104.1)",
    "uvicorn (==0.24.0)",
    "sqlalchemy (==2.0.23)",
    "alembic (==1.12.1)",
    "psycopg2-binary (==2.9.9)",
    "python-dotenv (==1.0.0)",
    "pydantic[email] (>=2.11.5,<3.0.0)",
    "pydantic-settings (==2.1.0)",
    "python-jose[cryptography] (>=3.5.0,<4.0.0)",
    "passlib[bcrypt] (==1.7.4)",
    "python-multipart (==0.0.6)",
    "mercadopago (==2.2.0)",
    "requests (==2.31.0)",
    "email-validator (>=2.2.0,<3.0.0)",
    # Novas dependências para Fase 3
    "boto3 (>=1.34.0)",
    "prometheus-client (>=0.19.0)",
    "structlog (>=23.2.0)"
]
```

#### **GitHub Actions Workflow:**
```yaml
# .github/workflows/deploy.yml
name: Deploy Application

on:
  push:
    branches: [main, staging]

jobs:
  build-and-deploy:
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

## 🔐 **Configuração de Segurança**

### **1. Proteção de Branches**
Para cada repositório, configurar:

```yaml
# Settings > Branches > Add rule
Branch name pattern: main
- ✅ Require a pull request before merging
- ✅ Require approvals: 1
- ✅ Require status checks to pass before merging
- ✅ Require branches to be up to date before merging
```

### **2. Secrets Management**
```bash
# Criar secrets no AWS Secrets Manager
aws secretsmanager create-secret \
    --name "/postech/database/credentials" \
    --description "Database credentials for Postech app" \
    --secret-string '{"username":"postech","password":"secure-password","host":"postech-db.cluster-xyz.us-east-1.rds.amazonaws.com","port":"5432","database":"postech"}'

aws secretsmanager create-secret \
    --name "/postech/cognito/credentials" \
    --description "Cognito credentials for Postech app" \
    --secret-string '{"user_pool_id":"us-east-1_xyz","client_id":"abc123"}'
```

## 📊 **Monitoramento e Observabilidade**

### **1. CloudWatch Dashboards**
```yaml
# Criar dashboard para monitoramento
- API Gateway metrics
- Lambda function metrics
- EKS cluster metrics
- RDS database metrics
```

### **2. Alertas**
```yaml
# Configurar alertas
- CPU > 80% por 5 minutos
- Memory > 85% por 5 minutos
- Error rate > 5% por 1 minuto
- Response time > 2s por 1 minuto
```

## 🧪 **Testes de Deployment**

### **1. Testes de Sanidade**
```bash
# Testar API Gateway
curl -X POST https://api.postech.com/auth \
  -H "Content-Type: application/json" \
  -d '{"cpf":"12345678901"}'

# Testar aplicação
curl https://app.postech.com/health

# Testar banco de dados
kubectl exec -it deployment/fastfood-app -- python -c "
import psycopg2
conn = psycopg2.connect('postgresql://...')
print('Database connection successful')
"
```

### **2. Testes de Carga**
```bash
# Usar k6 para testes de carga
k6 run load-test.js
```

## 🔄 **Rollback Strategy**

### **1. Rollback Automático**
```yaml
# Configurar rollback automático em caso de falha
- Monitorar health checks
- Rollback automático se health check falhar por 3 minutos
- Notificação via Slack/Email
```

### **2. Rollback Manual**
```bash
# Rollback para versão anterior
kubectl rollout undo deployment/fastfood-app

# Rollback Terraform
terraform apply -var="app_version=previous"
```

## 📝 **Checklist de Deployment**

### **Pré-deployment:**
- [ ] Todos os repositórios criados
- [ ] GitHub Secrets configurados
- [ ] AWS credentials configurados
- [ ] Terraform state bucket criado
- [ ] ECR repositories criados

### **Deployment:**
- [ ] Database infrastructure deployed
- [ ] Kubernetes infrastructure deployed
- [ ] Lambda functions deployed
- [ ] Application deployed
- [ ] API Gateway configured

### **Pós-deployment:**
- [ ] Health checks passando
- [ ] Monitoramento configurado
- [ ] Alertas configurados
- [ ] Documentação atualizada
- [ ] Vídeo demonstrativo gravado

## 🔄 **Migração da Estrutura Atual**

### **1. Manter no Repositório Principal:**
- ✅ `backend/` - Aplicação FastAPI (evoluir para EKS)
- ✅ `docs/` - Documentação
- ✅ `README.md` - Documentação principal

### **2. Extrair para Repositórios Separados:**
- 🔄 `backend/k8s/` → `postech-kubernetes-infra/`
- 🔄 `backend/alembic/` → `postech-database-infra/`
- ➕ Criar `postech-lambda-functions/` (novo)

### **3. Evoluir a Aplicação:**
- 🔄 `backend/Dockerfile` - Otimizar para produção
- 🔄 `backend/pyproject.toml` - Adicionar dependências de monitoramento
- 🔄 `backend/src/` - Adicionar autenticação JWT
- 🔄 `render.yaml` - Migrar para AWS EKS

---

**Próximo**: Executar deployment e configurar monitoramento
