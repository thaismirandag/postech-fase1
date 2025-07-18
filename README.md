# Sistema de Autoatendimento Fast Food - Fase 2

## Visão Geral
Sistema completo de autoatendimento para fast food desenvolvido com Clean Architecture, implementando todos os requisitos da Fase 2 do Tech Challenge.

## Funcionalidades da Fase 2

### ✅ APIs Implementadas
- **Checkout de Pedido**: Recebe produtos e retorna identificação do pedido
- **Consulta Status de Pagamento**: Verifica se pagamento foi aprovado
- **Webhook Pagamento**: Recebe confirmações do Mercado Pago
- **Listagem Ordenada**: Pedidos ordenados por status e data
- **Atualização de Status**: Com validações de transição

### ✅ Regras de Negócio
- Valor mínimo/máximo de pedidos
- Limite de itens e quantidades
- Horário de funcionamento
- Validações de CPF, email, dados
- Transições de status validadas

### ✅ Arquitetura
- **Clean Architecture/Hexagonal**: Separação clara de responsabilidades
- **DDD**: Entidades, agregados e repositórios bem definidos
- **Validações Avançadas**: No domínio e use-cases
- **Kubernetes**: Deploy completo com HPA, ConfigMaps, Secrets

## Estrutura do Projeto

```
postech-fase1/
├── backend/
│   ├── src/
│   │   ├── clean_architecture/
│   │   │   ├── api/           # Controllers HTTP
│   │   │   ├── dtos/          # Data Transfer Objects
│   │   │   ├── entities/      # Entidades de domínio
│   │   │   ├── use_cases/     # Casos de uso
│   │   │   ├── gateways/      # Implementações de repositórios
│   │   │   └── interfaces/    # Contratos/Portas
│   │   └── main.py           # Aplicação FastAPI
│   ├── k8s/                  # Manifests Kubernetes
│   ├── scripts/              # Scripts de automação
│   └── Dockerfile.prod       # Docker multi-stage
├── docs/
│   ├── fase2/               # Documentação específica da Fase 2
│   └── *.puml               # Diagramas PlantUML
└── docker-compose.yml       # Ambiente de desenvolvimento
```

## Como Executar

### Pré-requisitos
- Docker e Docker Compose
- Python 3.11+
- PostgreSQL (via Docker)

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

### Produção
```bash
# Build da imagem
docker build -f backend/Dockerfile.prod -t fastfood-api .

# Execute com variáveis de ambiente
docker run -p 8000:8000 fastfood-api
```

### Kubernetes
```bash
# Deploy no cluster
cd backend/k8s
./deploy-k8s.sh

# Verifique os recursos
kubectl get all -n fastfood
```

## APIs Principais

### Checkout de Pedido (NOVO)
```bash
POST /v1/api/public/pedidos/checkout
{
  "cliente_id": "uuid",
  "itens": [
    {"produto_id": "uuid", "quantidade": 2}
  ]
}
```

### Consulta Status Pagamento (NOVO)
```bash
GET /v1/api/public/pagamento/{pedido_id}/status
```

### Webhook Mercado Pago (NOVO)
```bash
POST /v1/api/public/pagamento/webhook
```

### Listar Pedidos (ATUALIZADO)
```bash
GET /v1/api/admin/pedidos/
# Ordenação: Pronto > Em Preparação > Recebido
```

## Documentação

### Swagger/OpenAPI
```
http://localhost:8000/docs
```

### Documentação Completa da Fase 2
```
docs/fase2/README.md
docs/fase2/API_DOCUMENTATION.md
```

### Diagramas
- `docs/fase2/event-storming-fase2.puml` - Event Storming detalhado
- `docs/fase2/fluxos-alternativos.puml` - Cenários de erro
- `docs/architecture.puml` - Arquitetura geral

## Diferenciais da Fase 2

### ✅ Requisitos Funcionais
- [x] Checkout de pedido com identificação
- [x] Consulta de status de pagamento
- [x] Webhook para confirmação de pagamento
- [x] Listagem ordenada de pedidos
- [x] Atualização de status com validações
- [x] Integração Mercado Pago (mock)

### ✅ Requisitos de Infraestrutura
- [x] Kubernetes com HPA
- [x] ConfigMaps e Secrets
- [x] Deployments e Services
- [x] Escalabilidade automática
- [x] Boas práticas de segurança

### ✅ Clean Architecture
- [x] Separação de responsabilidades
- [x] Use cases bem definidos
- [x] Entidades de domínio robustas
- [x] Validações no domínio
- [x] Testes automatizados

## Status do Projeto

**Fase 2 - COMPLETA** ✅

- [x] APIs conforme especificação
- [x] Arquitetura Kubernetes
- [x] Documentação completa
- [x] Regras de negócio implementadas
- [x] Validações avançadas
- [x] Event Storming detalhado
- [x] Fluxos alternativos mapeados

## Próximos Passos

Para evolução futura:
1. Integração real com Mercado Pago
2. Implementação de filas de mensageria
3. Métricas e monitoramento
4. Testes de carga
5. CI/CD pipeline

---

**Desenvolvido para o Tech Challenge - Fase 2**  
*Clean Architecture | DDD | Kubernetes | FastAPI*



