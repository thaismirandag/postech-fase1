# Fase 3 - Tech Challenge

## 📋 **Visão Geral**

A Fase 3 representa a evolução do sistema de autoatendimento de fast food para uma arquitetura em nuvem com serviços serverless, implementando as melhores práticas de CI/CD e segurança.

## 🎯 **Objetivos da Fase 3**

### **1. API Gateway e Autenticação Serverless**
- Implementar API Gateway para receber solicitações externas
- Criar function serverless para autenticar/consultar cliente via CPF
- Integrar com sistema de autenticação (AD, Cognito)
- Utilizar JWT para autenticação sem senha

### **2. Arquitetura Multi-Repositório**
- **Repositório 1**: Lambda Functions
- **Repositório 2**: Infraestrutura Kubernetes (Terraform)
- **Repositório 3**: Infraestrutura Banco de Dados (Terraform)
- **Repositório 4**: Aplicação Kubernetes (atual `backend/`)

### **3. CI/CD e Segurança**
- Deploy automatizado via GitHub Actions
- Branches main/master protegidas
- Pull Requests obrigatórios
- Secrets para valores sensíveis
- Terraform para toda infraestrutura

### **4. Melhorias no Banco de Dados**
- Estrutura otimizada
- Documentação de modelagem
- Justificativa da escolha do banco

### **5. Serviços Cloud Serverless**
- **Functions**: AWS Lambda, Azure Functions, ou Google Functions
- **Banco de Dados**: AWS RDS, Azure SQL, ou Cloud SQL
- **Autenticação**: AWS Cognito, Microsoft AD, ou Google Identity

## 📁 **Estrutura Atual vs. Fase 3**

### **Estrutura Atual:**
```
📦 postech-fase1 (Repositório Principal)
├── 📁 backend/ (Aplicação FastAPI)
│   ├── 📁 src/clean_architecture/
│   │   ├── 📁 api/ (Rotas FastAPI)
│   │   ├── 📁 controllers/ (Lógica de negócio)
│   │   ├── 📁 entities/ (Entidades de domínio)
│   │   ├── 📁 gateways/ (Acesso a dados)
│   │   ├── 📁 use_cases/ (Casos de uso)
│   │   └── 📁 external/ (Serviços externos)
│   ├── 📁 k8s/ (Manifests Kubernetes)
│   ├── 📄 Dockerfile
│   ├── 📄 pyproject.toml (Poetry)
│   └── 📄 alembic/ (Migrations)
├── 📄 docker-compose.yml
├── 📄 render.yaml (Deploy atual)
└── 📁 docs/
    └── 📁 fase3/ (Esta documentação)
```

### **Estrutura Fase 3 (Proposta):**
```
📦 postech-fase1 (Repositório Principal - Mantido)
├── 📁 backend/ (Aplicação Kubernetes - Evoluída)
├── 📁 docs/fase3/ (Documentação)
└── 📄 README.md

📦 postech-lambda-functions (Novo Repositório)
├── 📁 src/auth/
├── 📄 serverless.yml
└── 📄 .github/workflows/

📦 postech-kubernetes-infra (Novo Repositório)
├── 📁 terraform/
├── 📁 kubernetes/
└── 📄 .github/workflows/

📦 postech-database-infra (Novo Repositório)
├── 📁 terraform/
├── 📁 migrations/
└── 📄 .github/workflows/
```

## 🚀 **Migração da Estrutura Atual**

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

## 🗂️ **Estrutura de Repositórios Detalhada**

### **1. Repositório: `postech-lambda-functions`**
```
📦 postech-lambda-functions
├── 📁 src/
│   ├── 📁 auth/
│   │   ├── 📄 authenticate.py (Autenticação por CPF)
│   │   └── 📄 validate_jwt.py (Validação JWT)
│   └── 📁 utils/
│       └── 📄 cognito_client.py (Cliente Cognito)
├── 📁 tests/
├── 📄 requirements.txt
├── 📄 serverless.yml
└── 📄 .github/workflows/deploy.yml
```

### **2. Repositório: `postech-kubernetes-infra`**
```
📦 postech-kubernetes-infra
├── 📁 terraform/
│   ├── 📁 eks/ (Cluster EKS)
│   ├── 📁 vpc/ (Rede)
│   ├── 📁 security-groups/ (Segurança)
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
│   ├── 📁 rds/ (PostgreSQL RDS)
│   ├── 📁 subnet-groups/
│   └── 📁 variables.tf
├── 📁 migrations/ (Evoluído do backend/alembic/)
└── 📄 .github/workflows/deploy.yml
```

### **4. Repositório: `postech-app` (backend atual)**
```
📦 postech-app
├── 📁 src/clean_architecture/ (Mantido)
├── 📄 Dockerfile (Otimizado)
├── 📄 pyproject.toml (Atualizado)
└── 📄 .github/workflows/deploy.yml (Novo)
```

## 🔄 **Plano de Migração**

### **Fase 1: Preparação**
1. ✅ Criar documentação da Fase 3
2. 🔄 Configurar AWS credentials
3. 🔄 Criar repositórios separados
4. 🔄 Configurar GitHub Actions

### **Fase 2: Infraestrutura**
1. 🔄 Deploy RDS PostgreSQL
2. 🔄 Deploy EKS Cluster
3. 🔄 Configurar ECR
4. 🔄 Configurar API Gateway

### **Fase 3: Aplicação**
1. 🔄 Deploy Lambda Functions
2. 🔄 Migrar aplicação para EKS
3. 🔄 Configurar autenticação
4. 🔄 Configurar monitoramento

### **Fase 4: Validação**
1. 🔄 Testes de integração
2. 🔄 Configurar alertas
3. 🔄 Documentar arquitetura
4. 🔄 Gravar vídeo demonstrativo

## 🚀 **Entregáveis**

### **Obrigatórios:**
1. ✅ 4 repositórios separados com CI/CD
2. ✅ API Gateway + Lambda para autenticação
3. ✅ Branches protegidas + Pull Requests
4. ✅ Documentação de arquitetura
5. ✅ Vídeo demonstrativo (YouTube/Vimeo/Drive)
6. ✅ Acesso ao usuário `soatarchitecture`

### **Artefatos:**
- 📄 PDF/TXT com links dos repositórios
- 🎥 URL do vídeo demonstrativo
- 📚 Documentação completa da arquitetura

## 🔧 **Próximos Passos**

1. **Criar repositórios separados**
2. **Implementar API Gateway**
3. **Desenvolver Lambda Functions**
4. **Configurar CI/CD pipelines**
5. **Documentar arquitetura**
6. **Gravar vídeo demonstrativo**

---

**Status**: 🟡 Em desenvolvimento  
**Prazo**: Conforme cronograma da disciplina
