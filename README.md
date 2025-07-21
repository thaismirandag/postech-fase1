# 📟 Tech Challenge - Sistema de Autoatendimento de Fast Food

Este projeto é um sistema de autoatendimento desenvolvido para uma lanchonete, implementado em duas fases do Tech Challenge da pós de arquitetura de software da FIAP. O sistema visa facilitar o gerenciamento de pedidos, produtos e a simulação de pagamento via QR Code do Mercado Pago.

## 📃 Sumário

- [📟 Sobre o Projeto](#-tech-challenge---sistema-de-autoatendimento-de-fast-food)
- [🎯 Fases do Projeto](#-fases-do-projeto)
- [⚙️ Tecnologias Utilizadas](#⚙️-tecnologias-utilizadas)
- [🧹 Arquitetura Hexagonal](#-arquitetura-hexagonal)
- [🚀 Como Executar o Projeto](#-como-executar-o-projeto)
- [🔗 Endpoints Principais](#-endpoints-principais)
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
- ✅ **Regras de Negócio Avançadas**: Valor mínimo/máximo, limites, horários
- ✅ **Kubernetes**: Deploy completo com HPA, ConfigMaps, Secrets

---

## ⚙️ Tecnologias Utilizadas

- **Backend**: Python 3.11, FastAPI, SQLAlchemy, Alembic
- **Banco de Dados**: PostgreSQL
- **Containerização**: Docker & Docker Compose
- **Orquestração**: Kubernetes
- **Pagamentos**: Mercado Pago SDK (Integração REAL)
- **Validação**: Pydantic
- **Autenticação**: JWT

---

## 🧹 Arquitetura Hexagonal

O projeto segue os princípios da arquitetura hexagonal (Ports & Adapters), organizando as responsabilidades por camadas:

- `domain/`: Entidades e regras de negócio
- `application/services/`: Orquestração da lógica de negócio
- `ports/`: Interfaces de entrada e saída (contracts)
- `adapters/input/`: Controllers (FastAPI)
- `adapters/output/`: Repositórios e serviços externos
- `infrastructure/db/`: Modelos ORM, sessão e configurações do banco

---

## 🚀 Como executar o projeto

### 📦 Pré-requisitos
- Docker
- Docker Compose

### ▶️ Subindo o ambiente

1. **Clone o repositório:**
```bash
git clone https://github.com/thaismirandag/postech-fiap.git
```

2. **Configure as variáveis de ambiente:**
Crie um arquivo `.env` na pasta `backend` com base no `env.example`.

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

6. **Gerar nova migração Alembic:**
```bash
docker-compose exec app poetry run alembic revision --autogenerate -m "mensagem de migração"
docker-compose exec app poetry run alembic upgrade head
```

7. **Executar Ruff (linter):**
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

## 🔗 Endpoints Principais

### 👤 Clientes
- `POST /v1/api/admin/clientes/` – Criar ou obter cliente (identificado ou anônimo)
- `GET /v1/api/admin/clientes/` – Listar todos os clientes (admin)
- `GET /v1/api/admin/clientes/{cpf}` – Buscar cliente por cpf (admin)

### 🍔 Produtos
- `GET /v1/api/admin/produtos/` – Listar produtos disponíveis
- `POST /v1/api/admin/produtos/` – Criar produto (admin)
- `DELETE /v1/api/admin/produtos/{produto_id}` – Remover produto (admin)

### 🧾 Pedidos
- `POST /v1/api/admin/pedidos/` – Cliente cria um pedido
- `GET /v1/api/admin/pedidos/{pedido_id}` – Cliente acompanha status do pedido
- `GET /v1/api/admin/pedidos/` – Listar todos os pedidos (admin)
- `GET /v1/api/admin/pedidos/em-aberto` – Listar pedidos em aberto (admin)
- `PATCH /v1/api/admin/pedidos/{pedido_id}/status` – Atualizar status do pedido (admin)
- `DELETE /v1/api/admin/pedidos/{pedido_id}` – Deletar pedido (admin)

### 💳 Pagamento
- `GET /v1/api/admin/pagamento/qrcode` – Gerar QRCode real do Mercado Pago

### 🚀 Fase 2 - Endpoints Avançados
- `POST /v1/api/admin/pedidos/checkout` – Checkout de pedido com identificação
- `GET /v1/api/admin/pagamento/{pedido_id}/status` – Consulta status de pagamento real
- `POST /v1/api/admin/pagamento/webhook` – Webhook real para confirmação de pagamento

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
- [Demostração do projeto](https://youtu.be/2qGpN0MsCpQ)

## 📚 Documentação Adicional

### Swagger/OpenAPI
```
http://localhost:8000/docs
```

### Documentação Completa da Fase 2
```
docs/fase2/README.md
docs/fase2/mercadopago-integration.md
```

### Diagramas
- `docs/arquitetura.png` - Diagrama de Arquitetura
- `docs/fase2/event-storming-fase2.puml` - Event Storming detalhado
- `docs/fase2/fluxos-alternativos.puml` - Cenários de erro
- `docs/architecture.puml` - Arquitetura geral
- **[Event Storming Fase 1 - Miro](https://miro.com/app/board/uXjVI2n2GlA=/)** - Diagrama interativo DDD

---

## 🎯 Status do Projeto

**Fase 1 - COMPLETA** ✅  
**Fase 2 - COMPLETA** ✅

- [x] APIs conforme especificação
- [x] Arquitetura Kubernetes
- [x] Documentação completa
- [x] Regras de negócio implementadas
- [x] Validações avançadas
- [x] Event Storming detalhado
- [x] Fluxos alternativos mapeados
- [x] **Integração REAL com Mercado Pago**

## 🔮 Próximos Passos

Para evolução futura:
1. ✅ Integração real com Mercado Pago (IMPLEMENTADA)
2. Implementação de filas de mensageria
3. Métricas e monitoramento
4. Testes de carga
5. CI/CD pipeline

---

**Desenvolvido para o Tech Challenge - Fases 1 e 2**  
*Clean Architecture | DDD | Kubernetes | FastAPI | Mercado Pago*



