# 🧾 Tech Challenge - Sistema de Autoatendimento de Fast Food

Este projeto é um sistema de autoatendimento para uma lanchonete, desenvolvido como parte do Tech Challenge da fase 1. O sistema visa facilitar o controle de pedidos, gerenciamento de produtos, e simulação de pagamento via QR Code do Mercado Pago.


## ⚙️ Tecnologias Utilizadas

- Python 3.11
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL
- Docker & Docker Compose
- Pydantic


---

## 🧩 Arquitetura Hexagonal

O projeto segue os princípios da arquitetura hexagonal (Ports & Adapters), dividindo as responsabilidades entre camadas:    
- `domain/`: Entidades e regras de negócio puras
- `application/services/`: Orquestração da lógica
- `ports/`: Interfaces de entrada e saída
- `adapters/input/`: Controllers (FastAPI)
- `adapters/output/`: Implementações de repositórios
- `infrastructure/db/`: Modelos ORM e config de banco

---

## 🚀 Como executar o projeto

### 📦 Pré-requisitos

- Docker
- Docker Compose

### ▶️ Subindo o ambiente

### 1. Clone o repositório:
```bash
git clone https://github.com/thaismirandag/postech-fase1.git
```
### 2. Configure as variáveis de ambiente:
Crie um arquivo `.env` na pasta `backend` com base no `.env-example`.

### 3. Suba o ambiente com Docker Compose:
```bash
docker-compose up --build
```

### 🌐 Acesso
- API: http://localhost:8000
- Documentação Swagger: http://localhost:8000/docs

### 4. (Opcional) Rodar as migrações Alembic manualmente
Se precisar rodar as migrações manualmente, execute:
```bash
docker-compose exec app poetry run alembic upgrade head
```

### 5. Gerar uma nova migração Alembic (após criar/alterar um model)
Sempre que criar ou alterar um modelo de persistência, gere uma nova migração com:
```bash
docker-compose exec app poetry run alembic revision --autogenerate -m "sua mensagem de migração"
```
Depois, aplique a migração normalmente:
```bash
docker-compose exec app poetry run alembic upgrade head
```

### 6. Rodar o Ruff (Linter)
Para verificar a qualidade e padronização do código Python, utilize o Ruff:
```bash
docker-compose exec app poetry run ruff check src/
```
Se quiser corrigir automaticamente alguns problemas encontrados:
```bash
docker-compose exec app poetry run ruff check src/ --fix
```

## Estrutura do Projeto

```
postech-fase1/
├── backend/
│   ├── alembic/                 # Migrações do banco de dados
│   │   └── versions/            # Arquivos de versões das migrações
│   ├── src/
│   │   ├── domain/              # Modelos de domínio (entidades de negócio)
│   │   │   └── models/
│   │   ├── application/         # Serviços de aplicação
│   │   ├── adapters/            # Adaptadores (input/output)
│   │   ├── infrastructure/      # Infraestrutura
│   │   │   ├── db/
│   │   │   │   ├── models/      # Modelos de persistência (SQLAlchemy)
│   │   │   │   ├── session.py   # Configuração da sessão do banco
│   │   │   │   └── base.py      # Declarative base do SQLAlchemy
│   │   │   └── config.py        # Configurações gerais
│   │   └── ...
│   ├── tests/                   # Testes
│   ├── .env                     # Variáveis de ambiente
│   ├── Dockerfile               # Configuração do Docker
│   ├── pyproject.toml           # Configuração do Poetry
│   └── README.md                # Documentação do backend
├── docs/                        # Documentação, diagramas e arquivos auxiliares
├── docker-compose.yml           # Configuração do Docker Compose
└── README.md                    # Documentação do projeto

```

## 🔗 Endpoints principais

### Clientes
- `POST /api/clientes/` – Criar cliente
- `GET /api/clientes/{cpf}` – Buscar cliente por CPF

### Produtos
- `POST /api/produtos/` – Criar produto
- `GET /api/produtos/categoria/{categoria}` – Buscar produtos por categoria

### Pedidos
- `POST /api/pedidos/` – Criar pedido (checkout fake)
- `GET /api/pedidos/` – Listar todos os pedidos
- `PATCH /api/pedidos/{id}/status` – Atualizar status do pedido

### Pagamento
- `POST /api/pagamentos/gerar-qrcode` – Simula geração de QR Code (Mercado Pago)


## 👥 Desenvolvedores

- Integrantes do Grupo: @thaismirandag, @murilobiss, @MathLuchiari

## 📄 Documentação

- [Documentação do Projeto](docs/README.md)
- [Diagrama de Arquitetura](docs/arquitetura.png)
