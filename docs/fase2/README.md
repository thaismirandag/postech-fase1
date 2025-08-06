# Fase 2 — Sistema de Autoatendimento Fast Food

## Visão Geral
Esta fase evolui o sistema para uma **Clean Architecture** avançada, implementando todos os requisitos da Fase 2 do Tech Challenge com regras de negócio robustas, validações avançadas, documentação rica em diagramas e suporte completo a deploy em produção com Kubernetes.

## Funcionalidades da Fase 2

### ✅ APIs Implementadas
- **Checkout de Pedido**: Recebe produtos e retorna identificação do pedido
- **Consulta Status de Pagamento**: Verifica se pagamento foi aprovado (REAL)
- **Webhook Pagamento**: Recebe confirmações do Mercado Pago (REAL)
- **Listagem Ordenada**: Pedidos ordenados por status e data
- **Atualização de Status**: Com validações de transição
- **Regras de Negócio Avançadas**: Valor mínimo/máximo, limites, horários
- **Integração Mercado Pago**: QR Code e webhooks reais

### ✅ Arquitetura
- **Clean Architecture**: Separação clara de responsabilidades
- **Use Cases Organizados**: Casos de uso bem definidos
- **Validações no Domínio**: Regras de negócio robustas
- **Kubernetes**: Deploy completo com HPA, ConfigMaps, Secrets
- **Render**: Deploy gratuito e simples (alternativa ao Kubernetes)

## Estrutura do Projeto (Fase 2)

```
src/clean_architecture/
├── api/                # Controllers HTTP (admin)
├── controllers/        # Orquestradores
├── dtos/              # Data Transfer Objects
├── entities/          # Entidades de domínio
├── enums/             # Enumerações
├── external/          # Serviços externos (Mercado Pago)
├── gateways/          # Implementações de repositórios
├── interfaces/        # Contratos/Portas
└── use_cases/         # Casos de uso organizados
```

## APIs Principais (Fase 2)

### 🚀 Checkout de Pedido (NOVO)
```bash
POST /v1/api/admin/pedidos/checkout
{
  "cliente_id": "uuid",  # opcional (cliente anônimo)
  "itens": [
    {"produto_id": "uuid", "quantidade": 2}
  ],
  "observacoes": "string"  # opcional
}
```

### 💳 Consulta Status Pagamento (NOVO)
```bash
GET /v1/api/admin/pagamento/{pedido_id}/status
```

### 🔔 Webhook Mercado Pago (NOVO)
```bash
POST /v1/api/admin/pagamento/webhook
```

### 📋 Listar Pedidos (ATUALIZADO)
```bash
GET /v1/api/admin/pedidos/
# Ordenação: Pronto > Em Preparação > Recebido
```

## Documentação Visual

### Diagramas Disponíveis
- `arquitetura-completa-fase2.puml` - **Diagrama de Arquitetura Completa (Fase 2)**
- `event-storming-fase2.puml` - Event Storming completo da Fase 2
- `fluxos-alternativos.puml` - Fluxos alternativos e cenários de erro
- `arquitetura-kubernetes.puml` - Arquitetura Kubernetes detalhada

### Diagrama de Arquitetura Completa
![Arquitetura Completa - Sistema de Autoatendimento Fast Food - Fase 2](Arquitetura%20Completa%20-%20Sistema%20de%20Autoatendimento%20Fast%20Food%20-%20Fase%202.png)

### Como Visualizar os Diagramas
1. **VS Code**: Instale a extensão PlantUML e pressione `Alt+D`
2. **Online**: Use o [PlantUML Online Server](http://www.plantuml.com/plantuml/uml/)
3. **Local**: Use o [PlantUML Viewer](https://plantuml.com/plantuml/uml/)

### Collection Postman
- `postman-collection.json` - Collection completa com todas as APIs e exemplos

### Guia de Execução
- `guia-execucao.md` - Instruções detalhadas de execução e ordem das APIs
- `mercadopago-integration.md` - Documentação completa da integração real com Mercado Pago
- `deploy-render.md` - Guia completo de deploy no Render (gratuito)

## Como Executar

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

#### 🚀 Render (Recomendado - Gratuito)
```bash
# 1. Push para GitHub
git push origin main

# 2. Conecte no Render
# - Acesse render.com
# - Conecte o repositório
# - Deploy automático via render.yaml

# 3. URLs geradas
# API: https://fastfood-api.onrender.com
# Swagger: https://fastfood-api.onrender.com/docs
```

#### 🐳 Docker
```bash
# Build da imagem
docker build -f backend/Dockerfile -t fastfood-api ./backend

# Execute com variáveis de ambiente
docker run -p 8000:8000 fastfood-api
```

#### ☸️ Kubernetes
```bash
# Deploy no cluster
cd backend/k8s
./deploy-k8s.sh

# Verifique os recursos
kubectl get all -n fastfood
```

## Diferenciais da Fase 2

### ✅ Requisitos Funcionais
- [x] Checkout de pedido com identificação
- [x] Consulta de status de pagamento
- [x] Webhook para confirmação de pagamento
- [x] Listagem ordenada de pedidos
- [x] Atualização de status com validações
- [x] Integração Mercado Pago (REAL)
- [x] Cliente anônimo no checkout

### ✅ Requisitos de Infraestrutura
- [x] Kubernetes com HPA
- [x] ConfigMaps e Secrets
- [x] Deployments e Services
- [x] Escalabilidade automática
- [x] Boas práticas de segurança
- [x] Render (alternativa gratuita)

### ✅ Clean Architecture
- [x] Separação de responsabilidades
- [x] Use cases bem definidos
- [x] Entidades de domínio robustas
- [x] Validações no domínio
- [x] Controllers unificados

### ✅ Documentação
- [x] Event Storming detalhado
- [x] Fluxos alternativos mapeados
- [x] Diagramas PlantUML
- [x] Documentação de APIs
- [x] Guia de deploy no Render

## Status do Projeto

**Fase 2 - COMPLETA** ✅

- [x] APIs conforme especificação
- [x] Arquitetura Kubernetes
- [x] Documentação completa
- [x] Regras de negócio implementadas
- [x] Validações avançadas
- [x] Event Storming detalhado
- [x] Fluxos alternativos mapeados
- [x] Integração REAL com Mercado Pago
- [x] Deploy no Render (gratuito)

## Como Evoluímos da Fase 1

### 🔄 Refatoração Arquitetural
- **Fase 1**: Arquitetura hexagonal básica
- **Fase 2**: Clean Architecture avançada com use cases organizados

### 🚀 Novas Funcionalidades
- **Fase 1**: Sistema básico de pedidos
- **Fase 2**: Checkout, webhook, consulta de status

### 🛡️ Validações
- **Fase 1**: Validações básicas
- **Fase 2**: Regras de negócio robustas no domínio

### ☸️ Infraestrutura
- **Fase 1**: Docker para desenvolvimento
- **Fase 2**: Kubernetes para produção + Render (gratuito)

### 📚 Documentação
- **Fase 1**: Documentação básica
- **Fase 2**: Event Storming, fluxos alternativos e guias de deploy

## Próximos Passos

Para evolução futura:
1. ✅ Integração real com Mercado Pago (IMPLEMENTADA)
2. Implementação de filas de mensageria
3. Métricas e monitoramento
4. Testes de carga
5. CI/CD pipeline

---

**✅ Fase 2 completa com deploy gratuito no Render!** 