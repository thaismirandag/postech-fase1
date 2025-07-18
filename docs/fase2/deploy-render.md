# 🚀 Deploy no Render - Fase 2

Este guia mostra como fazer o deploy do sistema de autoatendimento Fast Food no **Render**, uma plataforma gratuita e simples para deploy de aplicações.

## 🎯 Por que Render?

- ✅ **Gratuito** para projetos pequenos
- ✅ **Deploy automático** via Git
- ✅ **PostgreSQL gerenciado** incluído
- ✅ **SSL automático** (HTTPS)
- ✅ **Muito mais simples** que Kubernetes
- ✅ **Suporte nativo** a Python/FastAPI
- ✅ **Webhooks funcionam** perfeitamente

## 📋 Pré-requisitos

1. **Conta no Render** (gratuita)
2. **Repositório no GitHub** com o código
3. **Credenciais do Mercado Pago** (para integração real)

## 🔧 Passo a Passo

### 1. Preparar o Repositório

Certifique-se de que o repositório contém:
- ✅ `render.yaml` (configuração do Render)
- ✅ `requirements.txt` (dependências Python)
- ✅ `src/main.py` (aplicação FastAPI)
- ✅ `alembic/` (migrações do banco)

### 2. Criar Conta no Render

1. Acesse [render.com](https://render.com)
2. Clique em "Get Started for Free"
3. Faça login com GitHub
4. Autorize o acesso ao repositório

### 3. Deploy Automático

1. **No dashboard do Render:**
   - Clique em "New +"
   - Selecione "Blueprint"
   - Conecte seu repositório GitHub
   - O Render detectará automaticamente o `render.yaml`

2. **Configure as variáveis:**
   - `MERCADOPAGO_ACCESS_TOKEN`: Sua chave de acesso
   - `MERCADOPAGO_PUBLIC_KEY`: Sua chave pública
   - `JWT_SECRET`: Será gerado automaticamente

3. **Clique em "Create New Resources"**

### 4. Configuração Automática

O Render criará automaticamente:
- ✅ **Web Service**: API FastAPI
- ✅ **PostgreSQL Database**: Banco de dados
- ✅ **Environment Variables**: Configuradas
- ✅ **SSL Certificate**: HTTPS automático

## 🔗 URLs Geradas

Após o deploy, você terá:
- **API**: `https://fastfood-api.onrender.com`
- **Swagger**: `https://fastfood-api.onrender.com/docs`
- **Health Check**: `https://fastfood-api.onrender.com/health`

## 🗄️ Banco de Dados

### Migrações Automáticas

O Render executará automaticamente:
```bash
alembic upgrade head
```

### Acesso ao Banco

- **Host**: `dpg-xxxxx-a.oregon-postgres.render.com`
- **Port**: `5432`
- **Database**: `fastfood_db`
- **User**: `fastfood_user`
- **Password**: Gerado automaticamente

## 🔧 Configuração do Mercado Pago

### 1. Obter Credenciais

1. Acesse [Mercado Pago Developers](https://www.mercadopago.com.br/developers)
2. Crie uma conta ou faça login
3. Acesse suas credenciais de teste

### 2. Configurar no Render

No dashboard do Render, vá em **Environment Variables**:

```bash
MERCADOPAGO_ACCESS_TOKEN=TEST-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
MERCADOPAGO_PUBLIC_KEY=TEST-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
MERCADOPAGO_WEBHOOK_URL=https://fastfood-api.onrender.com/v1/api/admin/pagamento/webhook
```

### 3. Testar Integração

```bash
# Testar QR Code
curl "https://fastfood-api.onrender.com/v1/api/admin/pagamento/qrcode?pedido_id=123&valor=45.50"

# Testar Status
curl "https://fastfood-api.onrender.com/v1/api/admin/pagamento/123/status"
```

## 📊 Monitoramento

### Logs em Tempo Real

No dashboard do Render:
- **Logs**: Visualize logs em tempo real
- **Metrics**: CPU, memória, requisições
- **Health Checks**: Status da aplicação

### Alertas

Configure alertas para:
- ✅ Falhas de deploy
- ✅ Erros de aplicação
- ✅ Banco de dados offline

## 🔄 Deploy Contínuo

### Atualizações Automáticas

1. **Faça push** para o branch `main`
2. **Render detecta** automaticamente
3. **Build e deploy** automático
4. **Health check** confirma sucesso

### Rollback

Se algo der errado:
1. Vá em **Deploys**
2. Clique em **Rollback**
3. Volta para versão anterior

## 🧪 Testando o Deploy

### 1. Health Check
```bash
curl https://fastfood-api.onrender.com/health
```

### 2. Swagger UI
```
https://fastfood-api.onrender.com/docs
```

### 3. APIs Principais
```bash
# Login Admin
curl -X POST "https://fastfood-api.onrender.com/v1/api/admin/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"

# Listar Produtos
curl "https://fastfood-api.onrender.com/v1/api/admin/produtos/"

# Criar Pedido
curl -X POST "https://fastfood-api.onrender.com/v1/api/admin/pedidos/checkout" \
  -H "Content-Type: application/json" \
  -d '{"itens":[{"produto_id":"uuid","quantidade":2}]}'
```

## 🔒 Segurança

### SSL Automático
- ✅ HTTPS habilitado automaticamente
- ✅ Certificado válido
- ✅ Redirecionamento HTTP → HTTPS

### Variáveis Sensíveis
- ✅ `JWT_SECRET`: Gerado automaticamente
- ✅ `DATABASE_URL`: Configurado automaticamente
- ✅ Credenciais do Mercado Pago: Configuradas manualmente

## 💰 Custos

### Plano Gratuito
- ✅ **Web Service**: 750 horas/mês
- ✅ **PostgreSQL**: 90 dias
- ✅ **SSL**: Incluído
- ✅ **Custom Domains**: Incluído

### Limitações
- ⚠️ **Sleep após 15 min** de inatividade
- ⚠️ **512MB RAM** por serviço
- ⚠️ **0.1 CPU** por serviço

## 🚀 Vantagens vs Kubernetes

| Aspecto | Render | Kubernetes |
|---------|--------|------------|
| **Complexidade** | ⭐ Simples | ⭐⭐⭐⭐⭐ Complexo |
| **Setup** | ⭐ 5 minutos | ⭐⭐⭐⭐⭐ 2+ horas |
| **Custo** | ⭐ Gratuito | ⭐⭐⭐ Pago |
| **Manutenção** | ⭐ Automática | ⭐⭐⭐⭐⭐ Manual |
| **Escalabilidade** | ⭐⭐ Limitada | ⭐⭐⭐⭐⭐ Ilimitada |
| **Controle** | ⭐⭐ Básico | ⭐⭐⭐⭐⭐ Total |

## 🔧 Troubleshooting

### Erro: "Build Failed"
**Solução:**
1. Verifique o `requirements.txt`
2. Confirme que `src/main.py` existe
3. Verifique os logs de build

### Erro: "Database Connection Failed"
**Solução:**
1. Aguarde o banco inicializar (2-3 min)
2. Verifique se as migrações rodaram
3. Confirme a `DATABASE_URL`

### Erro: "Mercado Pago Integration Failed"
**Solução:**
1. Configure as variáveis do Mercado Pago
2. Verifique se as credenciais são válidas
3. Teste com credenciais de TEST

## 📈 Próximos Passos

### Para Produção
1. **Upgrade para plano pago** (se necessário)
2. **Configure domínio customizado**
3. **Implemente monitoramento avançado**
4. **Configure backups automáticos**

### Melhorias
1. **CDN** para assets estáticos
2. **Cache** para melhor performance
3. **Rate limiting** para APIs
4. **Logs estruturados**

---

**✅ Deploy no Render: Simples, rápido e gratuito!**  
*Perfeito para projetos acadêmicos e MVPs* 