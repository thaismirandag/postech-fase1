# 📟 Tech Challenge - Sistema de Autoatendimento de Fast Food

Este projeto é um sistema de autoatendimento desenvolvido para uma lanchonete, como parte da Fase 1 do Tech Challenge da pós de arquitetura de software da FIAP. O sistema visa facilitar o gerenciamento de pedidos, produtos e a simulação de pagamento via QR Code do Mercado Pago.

## 📃 Sumário

- [📟 Sobre o Projeto](#-tech-challenge---sistema-de-autoatendimento-de-fast-food)
- [⚙️ Tecnologias Utilizadas](#⚙%ef%b8%8f-tecnologias-utilizadas)
- [🧹 Arquitetura Hexagonal](#-arquitetura-hexagonal)
- [🚀 Como Executar o Projeto](#-como-executar-o-projeto)
- [🔗 Endpoints Principais](#-endpoints-principais)
- [👥 Desenvolvedores](#-desenvolvedores)
- [📄 Documentação](#-documentação)

---

## ⚙️ Tecnologias Utilizadas

- Python 3.11
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL
- Docker & Docker Compose
- Pydantic

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
git clone https://github.com/thaismirandag/postech-fase1.git
```

2. **Configure as variáveis de ambiente:**
Crie um arquivo `.env` na pasta `backend` com base no `.env-example`.

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

---

## 🔗 Endpoints principais

### 👤 Clientes
- `POST /v1/api/public/clientes/` – Criar cliente (identificado ou anônimo)
- GET /v1/api/admin/clientes/{cpf}
- `GET /v1/api/admin/clientes/{cpf}` – Buscar cliente por CPF

### 🍔 Produtos
- `POST /v1/api/admin/produtos/` – Criar produto (admin)
- `GET /v1/api/public/produtos/categoria/{categoria}` – Buscar produtos por categoria

### 🛂 Pedidos
- `POST /v1/api/public/pedidos/` – Criar pedido (checkout)
- `GET /v1/api/admin/pedidos/` – Listar todos os pedidos (admin)
- `PATCH /v1/api/admin/pedidos/{id}/status` – Atualizar status do pedido (admin)
- `GET /v1/api/public/pedidos/{id}` – Acompanhar pedido (cliente)

### 💳 Pagamento
- `POST /v1/api/public/pagamentos/gerar-qrcode` – Simular pagamento via QR Code

---

## 📄 Estrutura do Projeto

```
postech-fase1/
├── backend/
│   ├── alembic/                 # Migrações do banco
│   │   └── versions/            # Versões geradas
│   ├── src/
│   │   ├── domain/              # Entidades de negócio
│   │   │   └── models/
│   │   ├── application/         # Serviços de aplicação
│   │   ├── adapters/            # Controllers e repositórios
│   │   ├── infrastructure/      # Banco de dados, configs
│   │   │   ├── db/
│   │   │   │   ├── models/
│   │   │   │   ├── session.py
│   ├── Dockerfile               # Dockerfile
│   ├── .env                     # Variáveis de ambiente
│   ├── pyproject.toml           # Configuração do projeto
├── docker-compose.yml           # Docker Compose
├── docs/                        # Documentação e diagramas
└── README.md
```

---

## 👥 Desenvolvedores
- Thais Gomes (@thaismirandag)
- Murilo Biss (@murilobiss)
- Matheus Luchiari (@MathLuchiari)

## 📄 Documentação
- [Documentação do Projeto](docs/README.md)
- [Diagrama de Arquitetura](docs/arquitetura.png)
