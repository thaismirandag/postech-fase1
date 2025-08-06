# 🎬 ROTEIRO PARA APRESENTAÇÃO EM VÍDEO - FASE 2
## Sistema de Autoatendimento Fast Food - Tech Challenge FIAP

---

## 📋 INFORMAÇÕES GERAIS

**Título:** Demonstração do Sistema de Autoatendimento Fast Food - Fase 2  
**Duração:** 20-25 minutos  
**Plataforma:** Minikube (Kubernetes Local)  
**Foco:** Arquitetura, APIs e Infraestrutura  

---

## 🎯 1. INTRODUÇÃO (2-3 minutos)

### Apresentação do Projeto
```
"Olá! Sou [Seu Nome] e hoje vou demonstrar o Sistema de Autoatendimento 
Fast Food desenvolvido para a Fase 2 do Tech Challenge da FIAP.

Este projeto resolve um problema real: uma lanchonete em expansão que 
precisava de um sistema para controlar pedidos e evitar o caos no 
atendimento."
```

### Problema de Negócio Identificado
- ❌ **Atendimento caótico** sem sistema de controle
- ❌ **Pedidos perdidos** ou mal interpretados
- ❌ **Problemas de performance** nos horários de pico
- ❌ **Clientes insatisfeitos** e perda de negócios

### Solução Implementada
- ✅ **Sistema de autoatendimento** completo
- ✅ **Clean Architecture** com refatoração
- ✅ **Kubernetes** com HPA para escalabilidade
- ✅ **Integração Mercado Pago** (mock/real)
- ✅ **APIs robustas** conforme especificação

---

## 🏗️ 2. DEMONSTRAÇÃO DA ARQUITETURA (3-4 minutos)

### Mostrar o Diagrama de Arquitetura
```
"Vamos começar visualizando nossa arquitetura completa. Como vocês podem 
ver, implementamos uma solução robusta que atende todos os requisitos."
```

**Apresentar:**
- 📊 **Diagrama de arquitetura** (PNG)
- ☸️ **Componentes Kubernetes** detalhados
- ⚡ **HPA como solução** para performance
- 🌐 **Integração com serviços** externos

### Explicar os Componentes Principais
```
"Na infraestrutura Kubernetes temos:
- Namespace isolado para organização
- Deployment com 2-10 réplicas controladas pelo HPA
- Service para load balancing
- ConfigMap e Secret para segurança
- PostgreSQL com persistência"
```

**Componentes Destacados:**
- **Namespace:** `fastfood` (isolamento)
- **Deployment:** `fastfood-app` (2-10 réplicas)
- **Service:** `fastfood-service` (ClusterIP)
- **HPA:** `fastfood-hpa` (escalabilidade automática)
- **ConfigMap:** `fastfood-config` (variáveis)
- **Secret:** `fastfood-secret` (dados sensíveis)

---

## ☸️ 3. DEMONSTRAÇÃO DO MINIKUBE (4-5 minutos)

### Iniciar Minikube
```bash
# Comandos para mostrar no terminal
minikube start
kubectl get nodes
```

**Explicar:**
```
"Vamos iniciar nosso cluster Kubernetes local usando Minikube. 
Isso simula um ambiente de produção em nossa máquina local."
```

### Aplicar Configurações Kubernetes
```bash
# Mostrar os arquivos YAML e aplicar
kubectl apply -f backend/k8s/namespace.yaml
kubectl apply -f backend/k8s/configmap.yaml
kubectl apply -f backend/k8s/secret.yaml
kubectl apply -f backend/k8s/app.yaml
```

**Explicar cada arquivo:**
- **namespace.yaml:** Criação do namespace isolado
- **configmap.yaml:** Variáveis de ambiente
- **secret.yaml:** Dados sensíveis (senhas, tokens)
- **app.yaml:** Deployment, Service e HPA

### Verificar Deploy
```bash
# Mostrar status dos recursos
kubectl get all -n fastfood
kubectl get hpa -n fastfood
kubectl describe deployment fastfood-app -n fastfood
```

### Explicar HPA (Horizontal Pod Autoscaler)
```
"O HPA é nossa solução para problemas de performance. Ele monitora 
CPU e memória e escala automaticamente de 2 a 10 réplicas conforme 
a demanda, resolvendo os problemas de lentidão nos horários de pico."
```

**Configurações do HPA:**
- **Min Replicas:** 2 (disponibilidade mínima)
- **Max Replicas:** 10 (escala máxima)
- **Target CPU:** 70% (escala baseada em CPU)
- **Target Memory:** 80% (escala baseada em memória)
- **Scale Up:** 30s (resposta rápida)
- **Scale Down:** 300s (estabilidade)

---

## 🔧 4. BUILD E DEPLOY DA APLICAÇÃO (2-3 minutos)

### Build da Imagem Docker
```bash
# Mostrar no terminal
cd backend
docker build -t fastfood-app:latest .
minikube image load fastfood-app:latest
```

**Explicar:**
```
"Vamos construir nossa imagem Docker e carregá-la no Minikube. 
Isso simula o processo de CI/CD em um ambiente real."
```

### Verificar Deploy
```bash
# Mostrar logs e status
kubectl logs -f deployment/fastfood-app -n fastfood
kubectl get pods -n fastfood
```

**Verificar:**
- ✅ Pods em estado Running
- ✅ Logs sem erros
- ✅ Health checks passando

---

## 🌐 5. TESTE DAS APIs (6-8 minutos)

### Acessar Swagger UI
```
"Agora vamos testar nossas APIs. Primeiro, vou acessar o Swagger UI 
para demonstrar a documentação interativa."
```

```bash
# Port forward para acessar a aplicação
kubectl port-forward -n fastfood svc/fastfood-service 8000:80
```

**Acessar:** `http://localhost:8000/docs`

### Demonstrar APIs Públicas

#### 1. Listar Produtos
```bash
curl -X GET "http://localhost:8000/v1/api/produtos/" \
  -H "accept: application/json"
```

**Explicar:**
```
"Este endpoint retorna todos os produtos disponíveis para o cliente 
escolher no totem de autoatendimento."
```

#### 2. Criar Cliente
```bash
curl -X POST "http://localhost:8000/v1/api/clientes/" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João Silva",
    "email": "joao@email.com",
    "cpf": "12345678901"
  }'
```

**Explicar:**
```
"O cliente pode se cadastrar opcionalmente. Isso permite campanhas 
promocionais e acompanhamento de pedidos."
```

#### 3. Criar Pedido (Checkout) - REQUISITO i
```bash
curl -X POST "http://localhost:8000/v1/api/pedidos/" \
  -H "Content-Type: application/json" \
  -d '{
    "cliente_id": "uuid-do-cliente",
    "itens": [
      {
        "produto_id": "uuid-do-produto",
        "quantidade": 2
      }
    ],
    "observacoes": "Sem cebola"
  }'
```

**Explicar:**
```
"Este é o endpoint de checkout que recebe os produtos e retorna a 
identificação do pedido, conforme solicitado nos requisitos da Fase 2."
```

**Resposta Esperada:**
```json
{
  "id": "uuid-do-pedido",
  "cliente_id": "uuid-do-cliente",
  "status": "RECEBIDO",
  "data_criacao": "2025-01-20T10:00:00",
  "itens": [...],
  "valor_total": 25.50
}
```

#### 4. Gerar QR Code - REQUISITO vi (Mercado Pago)
```bash
curl -X GET "http://localhost:8000/v1/api/pagamentos/{pedido_id}/qrcode" \
  -H "accept: application/json"
```

**Explicar:**
```
"O QR Code é gerado automaticamente com o valor calculado do pedido. 
A integração com Mercado Pago está funcionando em modo mock para 
demonstração, mas pode ser facilmente configurada para produção."
```

**Resposta Esperada:**
```json
{
  "id": "uuid-do-pagamento",
  "status": "ok",
  "qrcode_url": "https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=MOCK_PAYMENT_{pedido_id}",
  "qrcode_id": "mock-preference-id"
}
```

### Demonstrar APIs Administrativas

#### 5. Login Admin
```bash
curl -X POST "http://localhost:8000/v1/api/admin/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123"
  }'
```

**Explicar:**
```
"Autenticação JWT para acesso às funcionalidades administrativas."
```

#### 6. Listar Pedidos (Ordenados) - REQUISITO iv
```bash
curl -X GET "http://localhost:8000/v1/api/admin/pedidos/" \
  -H "Authorization: Bearer {token}"
```

**Explicar:**
```
"Os pedidos são retornados ordenados conforme especificação:
1. Pronto > Em Preparação > Recebido
2. Pedidos mais antigos primeiro
3. Pedidos Finalizados não aparecem na lista"
```

**Resposta Esperada:**
```json
[
  {
    "id": "uuid-1",
    "status": "PRONTO",
    "data_criacao": "2025-01-20T09:00:00",
    "cliente_nome": "João Silva",
    "valor_total": 25.50
  },
  {
    "id": "uuid-2", 
    "status": "PREPARANDO",
    "data_criacao": "2025-01-20T09:30:00",
    "cliente_nome": "Maria Santos",
    "valor_total": 18.75
  }
]
```

#### 7. Atualizar Status do Pedido - REQUISITO v
```bash
curl -X PATCH "http://localhost:8000/v1/api/admin/pedidos/{pedido_id}/status" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "PREPARANDO"
  }'
```

**Explicar:**
```
"Este endpoint permite que a cozinha atualize o status do pedido. 
O fluxo completo é: RECEBIDO → PREPARANDO → PRONTO → FINALIZADO"
```

---

## 🔔 7. DEMONSTRAÇÃO DO WEBHOOK (2-3 minutos)

### Simular Webhook do Mercado Pago - REQUISITO iii
```bash
curl -X POST "http://localhost:8000/v1/api/pagamentos/webhook" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "payment",
    "data": {
      "id": "123456789"
    },
    "user_id": 123456,
    "version": "1.0",
    "date_created": "2025-01-20T10:00:00.000-03:00"
  }'
```

**Explicar:**
```
"Este webhook simula a confirmação de pagamento do Mercado Pago. 
Quando recebido, o sistema:
1. Consulta o status do pagamento
2. Atualiza o pedido para PAGO se aprovado
3. Permite que a cozinha inicie a preparação"
```

**Resposta Esperada:**
```json
{
  "status": "success",
  "message": "Webhook processado com sucesso. Status: approved",
  "pedido_id": "uuid-do-pedido",
  "payment_id": "123456789"
}
```

### Verificar Status do Pagamento - REQUISITO ii
```bash
curl -X GET "http://localhost:8000/v1/api/pagamentos/{pedido_id}/status" \
  -H "accept: application/json"
```

**Explicar:**
```
"Este endpoint permite consultar se o pagamento foi aprovado ou não, 
conforme especificado nos requisitos."
```

---

## ⚡ 8. DEMONSTRAÇÃO DO HPA (2-3 minutos)

### Simular Carga para Testar Escalabilidade
```bash
# Mostrar como gerar carga para testar HPA
for i in {1..50}; do
  curl -X GET "http://localhost:8000/v1/api/produtos/" &
done
```

### Monitorar HPA em Tempo Real
```bash
# Mostrar escalabilidade automática
kubectl get hpa -n fastfood -w
kubectl get pods -n fastfood
```

**Explicar:**
```
"Como vocês podem ver, o HPA detectou o aumento de carga e escalou 
de 2 para 6 réplicas automaticamente. Isso resolve os problemas de 
performance nos horários de pico, conforme especificado nos requisitos."
```

**Mostrar:**
- 📈 **CPU/Memory** aumentando
- 🔄 **Pods** sendo criados automaticamente
- ⚡ **Tempo de resposta** melhorando
- 📊 **Métricas** do HPA

---

## 🔒 9. VERIFICAÇÃO DE SEGURANÇA (1-2 minutos)

### Mostrar ConfigMap e Secret
```bash
# Mostrar configurações (sem expor dados sensíveis)
kubectl get configmap -n fastfood
kubectl get secret -n fastfood
```

**Explicar:**
```
"Implementamos boas práticas de segurança conforme especificado:
- ConfigMap para variáveis de ambiente
- Secret para dados sensíveis como senhas e tokens
- Namespace isolado para organização"
```

### Verificar Configurações
```bash
# Mostrar estrutura (sem expor valores)
kubectl describe configmap fastfood-config -n fastfood
kubectl describe secret fastfood-secret -n fastfood
```

---

## 📚 10. DEMONSTRAÇÃO DA DOCUMENTAÇÃO (1-2 minutos)

### Mostrar README Principal
```
"Vamos ver nossa documentação completa no README."
```

**Apresentar:**
- 📊 **Diagrama de arquitetura** integrado
- 📋 **Collection Postman** completa
- 📖 **Guia de execução** detalhado
- 🔗 **Endpoints documentados** com exemplos

### Mostrar Collection Postman
```
"Aqui está nossa collection completa do Postman com todos os 
endpoints e exemplos de requisição, conforme solicitado nos requisitos."
```

**Arquivos de Documentação:**
- `README.md` - Documentação principal
- `docs/postman/api_collection.json` - Collection Postman
- `docs/fase2/guia-execucao.md` - Guia completo
- `docs/fase2/mercadopago-integration.md` - Integração Mercado Pago

---

## 🎯 11. CONCLUSÃO (1-2 minutos)

### Resumo dos Requisitos Atendidos
```
"Vamos recapitular o que implementamos para a Fase 2:

✅ Clean Architecture com refatoração completa do código
✅ APIs conforme especificação:
  - Checkout de pedido (recebe produtos, retorna ID)
  - Consulta status de pagamento (aprovado/não)
  - Webhook para confirmação de pagamento
  - Listagem ordenada de pedidos (Pronto > Preparando > Recebido)
  - Atualização de status com validações

✅ Kubernetes com todos os requisitos:
  - HPA para escalabilidade automática
  - ConfigMap e Secret para segurança
  - Deployment e Service para exposição
  - Namespace isolado para organização

✅ Integração Mercado Pago (mock funcional)
✅ Documentação completa com diagramas
✅ Collection Postman com exemplos funcionais"
```

### Demonstração Prática
```
"Como vocês puderam ver, o sistema está funcionando perfeitamente:
- APIs respondendo corretamente a todos os requisitos
- HPA escalando automaticamente conforme demanda
- Webhook processando pagamentos adequadamente
- Pedidos sendo gerenciados com ordenação correta
- Segurança implementada com ConfigMap e Secret"
```

### Próximos Passos
```
"O sistema está pronto para produção e pode ser facilmente 
deployado em qualquer cluster Kubernetes (AKS, EKS, GKE) 
ou plataformas como Render."
```

---

## 📝 ROTEIRO DE GRAVAÇÃO

### Preparação Prévia:
1. ✅ **Minikube funcionando** e limpo
2. ✅ **Imagens Docker** buildadas
3. ✅ **Arquivos YAML** prontos e testados
4. ✅ **Swagger UI** acessível
5. ✅ **Collection Postman** carregada
6. ✅ **Terminal configurado** com fontes legíveis

### Ordem de Gravação:
1. **Introdução** (2-3 min) - Apresentação e contexto
2. **Arquitetura** (3-4 min) - Diagrama e componentes
3. **Minikube Setup** (4-5 min) - Configuração inicial
4. **Build/Deploy** (2-3 min) - Construção da aplicação
5. **APIs Públicas** (4-5 min) - Testes dos endpoints
6. **APIs Admin** (2-3 min) - Funcionalidades administrativas
7. **Webhook** (2-3 min) - Integração de pagamento
8. **HPA Demo** (2-3 min) - Escalabilidade automática
9. **Segurança** (1-2 min) - ConfigMap e Secret
10. **Documentação** (1-2 min) - README e Collection
11. **Conclusão** (1-2 min) - Resumo e fechamento

### Dicas para Gravação:
- 🎥 **Use tela cheia** para melhor visualização
- 🔊 **Fale claramente** e explique cada passo
- ⏱️ **Mantenha ritmo** constante (não muito rápido)
- 🎯 **Foque nos requisitos** principais da Fase 2
- 🔄 **Teste tudo** antes de gravar
- 📊 **Mostre resultados** das APIs
- ⚡ **Demonstre HPA** em ação

### Pontos de Atenção:
- **Tempo total:** 20-25 minutos
- **Qualidade:** 1080p ou superior
- **Áudio:** Claro e sem ruídos
- **Foco:** Requisitos da Fase 2
- **Demonstração:** Funcionalidades reais

---

## 🏆 CRITÉRIOS DE AVALIAÇÃO

### Requisitos Funcionais (40%):
- ✅ Checkout de pedido implementado
- ✅ Consulta status de pagamento
- ✅ Webhook para confirmação
- ✅ Listagem ordenada de pedidos
- ✅ Atualização de status
- ✅ Integração Mercado Pago

### Requisitos de Infraestrutura (40%):
- ✅ Kubernetes configurado
- ✅ HPA implementado
- ✅ ConfigMap e Secret
- ✅ Deployment e Service
- ✅ Namespace isolado

### Documentação (20%):
- ✅ README completo
- ✅ Collection Postman
- ✅ Guia de execução
- ✅ Diagrama de arquitetura

---

**🎬 Este roteiro garante que todos os requisitos da Fase 2 sejam demonstrados de forma clara e profissional!** 