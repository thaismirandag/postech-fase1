# Tech Challenge - Sistema de Autoatendimento de Fast Food

Este projeto é um sistema de autoatendimento para uma lanchonete, desenvolvido como parte do Tech Challenge da fase 1.

## Tecnologias Utilizadas

- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Docker
- Docker Compose

## Requisitos

- Docker
- Docker Compose

## Como Executar

### 1. Clone o repositório:
```bash
git clone [URL_DO_REPOSITORIO]
cd [NOME_DO_DIRETORIO]
```

### 2. Configure as variáveis de ambiente:
Crie um arquivo `.env` na pasta `backend` com base no `.env-example`.

### 3. Suba o ambiente com Docker Compose:
```bash
docker-compose up --build
```

### 4. Acesse a documentação da API:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 5. (Opcional) Rodar as migrações Alembic manualmente
Se precisar rodar as migrações manualmente, execute:
```bash
docker-compose exec app poetry run alembic upgrade head
```

### 6. Gerar uma nova migração Alembic (após criar/alterar um model)
Sempre que criar ou alterar um modelo de persistência, gere uma nova migração com:
```bash
docker-compose exec app poetry run alembic revision --autogenerate -m "sua mensagem de migração"
```
Depois, aplique a migração normalmente:
```bash
docker-compose exec app poetry run alembic upgrade head
```

### 7. Rodar o Ruff (Linter)
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

## Funcionalidades

- Cadastro e identificação de clientes
- Gerenciamento de produtos e categorias
- Sistema de pedidos
- Acompanhamento de pedidos
- Integração com Mercado Pago (MVP)

## Diagrama de Arquitetura

![Arquitetura do Sistema](docs/Arquitetura%20do%20Sistema.png)