# Fase 1 — Sistema de Autoatendimento Fast Food

## Visão Geral
Esta fase implementa o sistema básico de autoatendimento para fast food com arquitetura hexagonal, funcionalidades essenciais de gestão de pedidos, produtos e clientes.

## Funcionalidades da Fase 1

### ✅ APIs Implementadas
- **Gestão de Clientes**: Cadastro e consulta de clientes (identificados ou anônimos)
- **Gestão de Produtos**: CRUD completo de produtos
- **Gestão de Pedidos**: Criação, consulta e acompanhamento de pedidos
- **Simulação de Pagamento**: QR Code do Mercado Pago (mock)
- **Painel Administrativo**: Interface para gestão do sistema

### ✅ Arquitetura
- **Arquitetura Hexagonal**: Separação entre domínio, aplicação e infraestrutura
- **DDD Básico**: Entidades e repositórios bem definidos
- **FastAPI**: API REST moderna e performática
- **PostgreSQL**: Banco de dados robusto
- **Docker**: Containerização para desenvolvimento

## Estrutura do Projeto (Fase 1)

```
src/
├── domain/              # Entidades e regras de negócio
├── application/         # Orquestração da lógica de negócio
├── ports/              # Interfaces de entrada e saída (contracts)
├── adapters/input/     # Controllers (FastAPI)
├── adapters/output/    # Repositórios e serviços externos
└── infrastructure/db/  # Modelos ORM, sessão e configurações
```

## APIs Principais

### 👤 Clientes
- `POST /v1/api/public/clientes/` – Criar ou obter cliente
- `GET /v1/api/admin/clientes/` – Listar todos os clientes (admin)
- `GET /v1/api/admin/clientes/{cpf}` – Buscar cliente por cpf (admin)

### 🍔 Produtos
- `GET /v1/api/public/produtos/` – Listar produtos disponíveis
- `POST /v1/api/admin/produtos/` – Criar produto (admin)
- `DELETE /v1/api/admin/produtos/{produto_id}` – Remover produto (admin)

### 🧾 Pedidos
- `POST /v1/api/public/pedidos/` – Cliente cria um pedido
- `GET /v1/api/public/pedidos/{pedido_id}` – Cliente acompanha status do pedido
- `GET /v1/api/admin/pedidos/` – Listar todos os pedidos (admin)
- `GET /v1/api/admin/pedidos/em-aberto` – Listar pedidos em aberto (admin)
- `PATCH /v1/api/admin/pedidos/{pedido_id}/status` – Atualizar status do pedido (admin)
- `DELETE /v1/api/admin/pedidos/{pedido_id}` – Deletar pedido (admin)

### 💳 Pagamento
- `GET /v1/api/public/pagamento/qrcode` – Exibir QRCode do Mercado Pago

## Documentação Visual

### Diagramas Disponíveis
- `architecture.puml` - Arquitetura geral do sistema
- `arquitetura.png` - Diagrama de arquitetura em PNG
- `fluxo_pedido_pagamento.puml` - Fluxo de pedido e pagamento
- `fluxo_preparo_entrega_pedido.puml` - Fluxo de preparo e entrega
- `event-storming-fase1.puml` - Event Storming da Fase 1 (DDD)

### 📋 Event Storming no Miro
- **[Event Storming Fase 1 - Miro](https://miro.com/app/board/uXjVI2n2GlA=/)** - Diagrama interativo com todos os fluxos da Fase 1

### Como Visualizar os Diagramas
1. **VS Code**: Instale a extensão PlantUML e pressione `Alt+D`
2. **Online**: Use o [PlantUML Online Server](http://www.plantuml.com/plantuml/uml/)
3. **Local**: Use o [PlantUML Viewer](https://plantuml.com/plantuml/uml/)

## Como Executar

### Pré-requisitos
- Docker e Docker Compose
- Python 3.11+

### Desenvolvimento
```bash
# Clone o repositório
git clone <repository-url>
cd postech-fase1

# Execute com Docker Compose
docker-compose up -d

# Acesse a API
curl http://localhost:8000/health
```

### Documentação da API
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Diferenciais da Fase 1

### ✅ Funcionalidades Básicas
- [x] Cadastro e consulta de clientes
- [x] Gerenciamento de produtos
- [x] Criação e acompanhamento de pedidos
- [x] Simulação de pagamento via QR Code
- [x] Painel administrativo
- [x] Arquitetura hexagonal básica

### ✅ Tecnologias
- [x] FastAPI para API REST
- [x] SQLAlchemy para ORM
- [x] PostgreSQL para banco de dados
- [x] Docker para containerização
- [x] Alembic para migrações
- [x] Pydantic para validação

## Status do Projeto

**Fase 1 - COMPLETA** ✅

- [x] APIs conforme especificação
- [x] Arquitetura hexagonal implementada
- [x] Documentação básica
- [x] Funcionalidades essenciais
- [x] Ambiente de desenvolvimento

## Evolução para Fase 2

A Fase 2 evolui este sistema com:
- Clean Architecture avançada
- Regras de negócio robustas
- Validações avançadas
- Kubernetes para produção
- Documentação visual ampliada
- Event Storming detalhado

---

**Desenvolvido para o Tech Challenge - Fase 1**  
*Arquitetura Hexagonal | FastAPI | PostgreSQL | Docker* 