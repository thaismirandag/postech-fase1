# 🚀 Guia Completo de Execução - Fase 2

Este guia fornece instruções detalhadas para executar o sistema de autoatendimento Fast Food da Fase 2, incluindo a ordem correta de execução das APIs.

## 📋 Pré-requisitos

### Software Necessário
- Docker e Docker Compose
- Python 3.11+ (para desenvolvimento local)
- kubectl (para Kubernetes)
- Postman ou similar (para testar APIs)

### Configuração Inicial
```bash
# Clone o repositório
git clone https://github.com/thaismirandag/postech-fase1.git
cd postech-fase1

# Configure as variáveis de ambiente
cd backend
cp env.example .env
```

## 🏃‍♂️ Execução Local (Desenvolvimento)

### 1. Subir Ambiente
```bash
# Na raiz do projeto
docker-compose up -d

# Verificar se os containers estão rodando
docker-compose ps
```

### 2. Executar Migrações
```bash
# Executar migrações do banco
docker-compose exec app poetry run alembic upgrade head

# Verificar se as tabelas foram criadas
docker-compose exec db psql -U postgres -d tech_challenge -c "\dt"
```

### 3. Popular Dados Iniciais (Opcional)
```bash
# Executar script de popular produtos
docker-compose exec app python scripts/popular_tb_produtos.py
```

## 🔄 Ordem de Execução das APIs

### **PASSO 1: Autenticação**
```bash
# 1.1 - Login do Administrador
curl -X POST "http://localhost:8000/v1/api/admin/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"

# Resposta esperada:
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}

# Salve o token para usar nas próximas requisições
export ADMIN_TOKEN="seu_token_aqui"
```

### **PASSO 2: Gestão de Produtos**
```bash
# 2.1 - Listar produtos existentes
curl -X GET "http://localhost:8000/v1/api/admin/produtos/"

# 2.2 - Criar novo produto (requer autenticação)
curl -X POST "http://localhost:8000/v1/api/admin/produtos/" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{
    "nome": "X-Burger",
    "categoria": "Lanche",
    "preco": 25.90,
    "descricao": "Hambúrguer com queijo e salada"
  }'

# Salve o ID do produto criado
export PRODUTO_ID="uuid_do_produto_criado"
```

### **PASSO 3: Gestão de Clientes**
```bash
# 3.1 - Criar ou obter cliente
curl -X POST "http://localhost:8000/v1/api/admin/clientes/" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João Silva",
    "cpf": "12345678901",
    "email": "joao@email.com"
  }'

# Salve o ID do cliente criado
export CLIENTE_ID="uuid_do_cliente_criado"

# 3.2 - Listar clientes (admin)
curl -X GET "http://localhost:8000/v1/api/admin/clientes/" \
  -H "Authorization: Bearer $ADMIN_TOKEN"
```

### **PASSO 4: Criação de Pedidos**
```bash
# 4.1 - Criar pedido básico
curl -X POST "http://localhost:8000/v1/api/admin/pedidos/" \
  -H "Content-Type: application/json" \
  -d '{
    "cliente_id": "'$CLIENTE_ID'",
    "itens": [
      {
        "produto_id": "'$PRODUTO_ID'",
        "quantidade": 2
      }
    ],
    "observacoes": "Sem cebola"
  }'

# Salve o ID do pedido criado
export PEDIDO_ID="uuid_do_pedido_criado"
```

### **PASSO 5: Checkout (Fase 2)**
```bash
# 5.1 - Checkout de pedido (funcionalidade da Fase 2)
curl -X POST "http://localhost:8000/v1/api/admin/pedidos/checkout" \
  -H "Content-Type: application/json" \
  -d '{
    "cliente_id": "'$CLIENTE_ID'",
    "itens": [
      {
        "produto_id": "'$PRODUTO_ID'",
        "quantidade": 1
      }
    ],
    "observacoes": "Bem passado"
  }'

# Salve o ID do pedido do checkout
export PEDIDO_CHECKOUT_ID="uuid_do_pedido_checkout"
```

### **PASSO 6: Pagamento Real com Mercado Pago**
```bash
# 6.1 - Gerar QR Code Real do Mercado Pago
curl -X GET "http://localhost:8000/v1/api/admin/pagamento/qrcode?pedido_id=$PEDIDO_ID&valor=45.50"

# Configure as variáveis do Mercado Pago no .env:
# MERCADOPAGO_ACCESS_TOKEN=TEST-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
# MERCADOPAGO_PUBLIC_KEY=TEST-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
# MERCADOPAGO_WEBHOOK_URL=https://api.fastfood.com/webhook

# 6.2 - Consultar status de pagamento (Fase 2)
curl -X GET "http://localhost:8000/v1/api/admin/pagamento/$PEDIDO_CHECKOUT_ID/status"

# 6.3 - Simular webhook de pagamento (Fase 2)
curl -X POST "http://localhost:8000/v1/api/admin/pagamento/webhook" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "id": "123456789",
      "external_reference": "'$PEDIDO_CHECKOUT_ID'",
      "status": "approved",
      "amount": 25.90
    }
  }'
```

### **PASSO 7: Acompanhamento de Pedidos**
```bash
# 7.1 - Buscar pedido por ID
curl -X GET "http://localhost:8000/v1/api/admin/pedidos/$PEDIDO_ID"

# 7.2 - Listar todos os pedidos (admin)
curl -X GET "http://localhost:8000/v1/api/admin/pedidos/" \
  -H "Authorization: Bearer $ADMIN_TOKEN"

# 7.3 - Listar pedidos em aberto (admin)
curl -X GET "http://localhost:8000/v1/api/admin/pedidos/em-aberto" \
  -H "Authorization: Bearer $ADMIN_TOKEN"
```

### **PASSO 8: Atualização de Status**
```bash
# 8.1 - Atualizar status para "em_preparacao"
curl -X PATCH "http://localhost:8000/v1/api/admin/pedidos/$PEDIDO_ID/status" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{"status": "em_preparacao"}'

# 8.2 - Atualizar status para "pronto"
curl -X PATCH "http://localhost:8000/v1/api/admin/pedidos/$PEDIDO_ID/status" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{"status": "pronto"}'

# 8.3 - Atualizar status para "finalizado"
curl -X PATCH "http://localhost:8000/v1/api/admin/pedidos/$PEDIDO_ID/status" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -d '{"status": "finalizado"}'
```

## ☸️ Execução no Kubernetes (Produção)

### 1. Preparar Cluster
```bash
# Verificar se o kubectl está configurado
kubectl cluster-info

# Criar namespace
kubectl apply -f backend/k8s/namespace.yaml
```

### 2. Deploy da Aplicação
```bash
# Executar script de deploy
cd backend/k8s
./deploy-k8s.sh

# Verificar recursos criados
kubectl get all -n fastfood
```

### 3. Verificar Status
```bash
# Verificar pods
kubectl get pods -n fastfood

# Verificar serviços
kubectl get svc -n fastfood

# Verificar HPA
kubectl get hpa -n fastfood
```

### 4. Acessar Aplicação
```bash
# Port-forward para acessar localmente
kubectl port-forward svc/fastfood-service 8000:8000 -n fastfood

# Acessar API
curl http://localhost:8000/health
```

## 🧪 Testes de Validação

### Teste 1: Fluxo Completo
```bash
# Script de teste automatizado
cd backend/scripts
python test-validations.py
```

### Teste 2: Validações de Regras de Negócio
```bash
# Testar valor mínimo (deve falhar se < R$ 5,00)
curl -X POST "http://localhost:8000/v1/api/admin/pedidos/checkout" \
  -H "Content-Type: application/json" \
  -d '{
    "cliente_id": "'$CLIENTE_ID'",
    "itens": [
      {
        "produto_id": "'$PRODUTO_ID'",
        "quantidade": 1
      }
    ]
  }'

# Testar limite de itens (deve falhar se > 20 itens)
curl -X POST "http://localhost:8000/v1/api/admin/pedidos/checkout" \
  -H "Content-Type: application/json" \
  -d '{
    "cliente_id": "'$CLIENTE_ID'",
    "itens": [
      {
        "produto_id": "'$PRODUTO_ID'",
        "quantidade": 25
      }
    ]
  }'
```

## 📊 Monitoramento

### Logs da Aplicação
```bash
# Logs em desenvolvimento
docker-compose logs -f app

# Logs no Kubernetes
kubectl logs -f deployment/fastfood-deployment -n fastfood
```

### Métricas do Kubernetes
```bash
# Verificar uso de recursos
kubectl top pods -n fastfood

# Verificar eventos
kubectl get events -n fastfood --sort-by='.lastTimestamp'
```

## 🔧 Troubleshooting

### Problema: Aplicação não inicia
```bash
# Verificar logs
docker-compose logs app

# Verificar variáveis de ambiente
docker-compose exec app env | grep DB_
```

### Problema: Banco não conecta
```bash
# Verificar se o PostgreSQL está rodando
docker-compose ps db

# Testar conexão
docker-compose exec db psql -U postgres -d tech_challenge -c "SELECT 1;"
```

### Problema: APIs retornam erro 500
```bash
# Verificar logs da aplicação
docker-compose logs app

# Verificar se as migrações foram executadas
docker-compose exec app poetry run alembic current
```

## 📚 Documentação Adicional

### Swagger UI
```
http://localhost:8000/docs
```

### Health Check
```
http://localhost:8000/health
```

### Collection Postman
```
docs/fase2/postman-collection.json
```

## ✅ Checklist de Validação

- [ ] Ambiente Docker subiu corretamente
- [ ] Migrações executadas sem erro
- [ ] Login admin funcionando
- [ ] CRUD de produtos funcionando
- [ ] CRUD de clientes funcionando
- [ ] Criação de pedidos funcionando
- [ ] Checkout funcionando (Fase 2)
- [ ] Consulta status pagamento funcionando (Fase 2)
- [ ] Webhook funcionando (Fase 2)
- [ ] Atualização de status funcionando
- [ ] Listagem ordenada funcionando (Fase 2)
- [ ] Kubernetes deployado (se aplicável)
- [ ] HPA funcionando (se aplicável)

---

**🎯 Este guia garante que todas as funcionalidades da Fase 2 sejam testadas na ordem correta!** 