# 📟 Tech Challenge - Sistema de Autoatendimento de Fast Food

Este projeto é um sistema de autoatendimento desenvolvido para uma lanchonete, implementado em duas fases do Tech Challenge da pós de arquitetura de software da FIAP. O sistema visa facilitar o gerenciamento de pedidos, produtos e a simulação de pagamento via QR Code do Mercado Pago.

## 📃 Sumário

- [📟 Sobre o Projeto](#-tech-challenge---sistema-de-autoatendimento-de-fast-food)
- [🎯 Fases do Projeto](#-fases-do-projeto)
- [🏗️ Arquitetura do Sistema](#️-arquitetura-do-sistema)
- [⚙️ Tecnologias Utilizadas](#⚙️-tecnologias-utilizadas)
- [🚀 Como Executar o Projeto](#-como-executar-o-projeto)
- [🔗 Endpoints da API](#-endpoints-da-api)
- [📋 Collection de APIs](#-collection-de-apis)
- [📄 Estrutura do Projeto](#-estrutura-do-projeto)
- [👥 Desenvolvedores](#-desenvolvedores)
- [📽️ Demo](#-demo)

---

## 🎯 Fases do Projeto

### 📋 Fase 1 - Sistema Básico
Sistema inicial com funcionalidades básicas de autoatendimento:
- ✅ Cadastro e consulta de clientes
- ✅ Gerenciamento de produtos
- ✅ Criação e acompanhamento de pedidos
- ✅ Simulação de pagamento via QR Code
- ✅ Painel administrativo

### 🚀 Fase 2 - Sistema Avançado
Evolução do sistema com funcionalidades avançadas:
- ✅ **Checkout de Pedido**: Recebe produtos e retorna identificação do pedido
- ✅ **Consulta Status de Pagamento**: Verifica se pagamento foi aprovado
- ✅ **Webhook Pagamento**: Recebe confirmações do Mercado Pago
- ✅ **Listagem Ordenada**: Pedidos ordenados por status e data
- ✅ **Atualização de Status**: Com validações de transição
- ✅ **Kubernetes**: Deploy completo com HPA, ConfigMaps, Secrets

---

## 🏗️ Arquitetura do Sistema

### ☸️ Infraestrutura Kubernetes
**Namespace: fastfood**

#### **Ingress Controller**
- **Nginx Ingress**: SSL/TLS Termination, Load Balancing, Path-based routing, Rate limiting
- **SSL/TLS**: Certificados automáticos para segurança
- **Rate Limiting**: Proteção contra ataques e sobrecarga

#### **Service Layer**
- **fastfood-service**: ClusterIP com health checks
- **Load Balancer interno**: Distribuição de carga
- **Health Checks**: Monitoramento de disponibilidade

#### **Deployment**
- **fastfood-deployment**: 2-10 réplicas com HPA automático
- **Image**: fastfood-api:latest
- **Resources**: CPU 500m-1000m, Memory 512Mi-1Gi
- **Health Checks**: Liveness Probe, Readiness Probe

#### **HPA - Solução para Performance** ⚡
**Problema Resolvido**: Picos de demanda causando lentidão no atendimento
- **Min Replicas**: 2 (disponibilidade mínima)
- **Max Replicas**: 10 (escala automática)
- **Target CPU**: 70% (escala baseada em CPU)
- **Target Memory**: 80% (escala baseada em memória)
- **Scale Up**: 30s (resposta rápida)
- **Scale Down**: 300s (estabilidade)

#### **Configuração**
- **app-config**: ConfigMap com variáveis de ambiente
- **db-secret**: Secret com credenciais sensíveis
- **PostgreSQL**: Database com backup e replicação

### 🌐 Serviços Externos
- **Mercado Pago**: Integração real para QR Code e webhooks
- **Render**: Alternativa gratuita para deploy

### 🔄 Fluxo de Dados
- **API FastAPI**: Endpoints públicos e administrativos
- **Clean Architecture**: Use Cases, entidades, controllers e gateways

![Arquitetura Completa](docs/fase2/Arquitetura%20Completa%20-%20Sistema%20de%20Autoatendimento%20Fast%20Food%20-%20Fase%202.png)
![Arquitetura Completa](docs/fase2/Arquitetura%20Completa%20-%20Sistema%20de%20Autoatendimento%20Fast%20Food%20-%20Fase%202.png)

---

## ⚙️ Tecnologias Utilizadas

- **Backend**: Python 3.11, FastAPI, SQLAlchemy, Alembic
- **Banco de Dados**: PostgreSQL
- **Containerização**: Docker & Docker Compose
- **Orquestração**: Kubernetes
- **Pagamentos**: Mercado Pago SDK
- **Validação**: Pydantic
- **Autenticação**: JWT
- **Gerenciamento de Dependências**: Poetry

---

## 🚀 Como Executar o Projeto

### 📦 Pré-requisitos
- Docker
- Docker Compose

### ▶️ Subindo o ambiente

1. **Clone o repositório:**
```bash
git clone https://github.com/thaismirandag/postech-fiap.git
cd postech-fiap
```

2. **Configure as variáveis de ambiente:**
```bash
cd backend
cp env.example .env
# Edite o arquivo .env com suas configurações
```

3. **Suba o ambiente com Docker Compose:**
```bash
docker-compose up --build
```

4. **Acesso:**
- API: http://localhost:8000
- Documentação Swagger: http://localhost:8000/docs

5. **Rodar as migrações Alembic**
```bash
docker-compose exec app poetry run alembic upgrade head
```

6. **Popular banco com produtos de exemplo:**
```bash
docker-compose exec app python scripts/popular_tb_produtos.py
```

#### **Executar Linter**
```bash
docker-compose exec app poetry run ruff check src/
docker-compose exec app poetry run ruff check src/ --fix
```

### 🚀 Produção
```bash
# Build da imagem
docker build -f backend/Dockerfile -t fastfood-api ./backend

# Execute com variáveis de ambiente
docker run -p 8000:8000 fastfood-api
```

### ☸️ Kubernetes (Fase 2)
```bash
# Deploy no cluster
cd backend/k8s
./deploy-k8s.sh

# Verifique os recursos
kubectl get all -n fastfood
```

### 🚀 Render (Recomendado - Gratuito)
```bash
# 1. Faça push do código para GitHub
# 2. Acesse render.com e conecte o repositório
# 3. O deploy será automático via render.yaml

# URLs geradas:
# API: https://fastfood-api.onrender.com
# Swagger: https://fastfood-api.onrender.com/docs
```

---

## 🔗 Endpoints da API

### 🌐 Rotas Públicas (Sem Autenticação)

#### 👤 Clientes
- `POST /v1/api/clientes/` – Criar cliente (identificado ou anônimo)
- `POST /v1/api/clientes/` – Criar cliente (identificado ou anônimo)

#### 🍔 Produtos
- `GET /v1/api/produtos/` – Listar produtos disponíveis

#### 🧾 Pedidos
- `POST /v1/api/pedidos/` – Criar pedido (cliente pode ser anônimo)
- `POST /v1/api/pedidos/` – Criar pedido (cliente pode ser anônimo)
- `GET /v1/api/pedidos/{pedido_id}` – Cliente acompanha status do pedido

#### 💳 Pagamento
- `GET /v1/api/pagamentos/{pedido_id}/qrcode` – Gerar QR Code para pagamento (valor automático)
- `GET /v1/api/pagamentos/{pedido_id}/status` – Consultar status do pagamento
- `POST /v1/api/pagamentos/webhook` – Webhook para confirmação de pagamento
- `GET /v1/api/pagamentos/{pedido_id}/qrcode` – Gerar QR Code para pagamento (valor automático)
- `GET /v1/api/pagamentos/{pedido_id}/status` – Consultar status do pagamento
- `POST /v1/api/pagamentos/webhook` – Webhook para confirmação de pagamento

### 🔐 Rotas Administrativas (Com Autenticação)

#### 🔑 Autenticação
- `POST /v1/api/admin/login` – Login de administrador

#### 👥 Gestão de Clientes
- `GET /v1/api/admin/clientes/` – Listar todos os clientes
- `GET /v1/api/admin/clientes/{cpf}` – Buscar cliente por CPF

#### 🍔 Gestão de Produtos
- `POST /v1/api/admin/produtos/` – Criar novo produto
- `DELETE /v1/api/admin/produtos/{produto_id}` – Remover produto

#### 🧾 Gestão de Pedidos
- `GET /v1/api/admin/pedidos/` – Listar todos os pedidos (ordenados)
- `GET /v1/api/admin/pedidos/em-aberto` – Listar pedidos em aberto
- `PATCH /v1/api/admin/pedidos/{pedido_id}/status` – Atualizar status do pedido
- `DELETE /v1/api/admin/pedidos/{pedido_id}` – Deletar pedido

---

## 📋 Collection de APIs

### 🔗 Swagger/OpenAPI
**Documentação Interativa:**
- Local: http://localhost:8000/docs
- Produção: https://fastfood-api.onrender.com/docs

### 📥 Postman Collection
- `docs/postman/api_collection.json` - Todas as APIS para ser usada no postman

---

## 📄 Estrutura do Projeto

```
postech-fiap/
├── backend/
│   ├── alembic/                 # Migrações do banco
│   │   └── versions/            # Versões geradas
│   ├── src/
│   │   ├── clean_architecture/  # Arquitetura limpa
│   │   │   ├── api/            # Controllers da API
│   │   │   │   ├── public/     # Rotas públicas
│   │   │   │   └── admin/      # Rotas administrativas
│   │   │   ├── controllers/    # Orquestradores
│   │   │   ├── dtos/           # Data Transfer Objects
│   │   │   ├── entities/       # Entidades de domínio
│   │   │   ├── enums/          # Enumerações
│   │   │   ├── external/       # Serviços externos (Mercado Pago)
│   │   │   ├── gateways/       # Repositórios
│   │   │   ├── interfaces/     # Contratos/Portas
│   │   │   └── use_cases/      # Casos de uso
│   │   ├── Dockerfile          # Dockerfile
│   │   ├── env.example         # Variáveis de ambiente
│   │   └── pyproject.toml      # Configuração do projeto
│   └── k8s/                    # Configurações Kubernetes
├── docker-compose.yml           # Docker Compose
├── docs/                        # Documentação e diagramas
└── README.md
```

---

## 👥 Desenvolvedores
- Thais Gomes (@thaismirandag)
- Murilo Biss (@murilobiss)
- Matheus Luchiari (@MathLuchiari)

## 📽️ Demo 
- [Demostração do projeto](https://youtu.be/kw20YB7COYY)


## 📊 Diagramas

- `docs/arquitetura-completa-fase2.puml` - **Diagrama de Arquitetura Completa (Fase 2)**
- `docs/fase2/Arquitetura Completa - Sistema de Autoatendimento Fast Food - Fase 2.png` - **Diagrama de Arquitetura Completa (Fase 2)**
- `docs/fase2/event-storming-fase2.puml` - Event Storming detalhado
- `docs/fase2/fluxos-alternativos.puml` - Cenários de erro
- `docs/fase2/arquitetura-kubernetes.puml` - Arquitetura Kubernetes

---





