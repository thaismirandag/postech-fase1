# 📚 Documentação do Projeto

Este diretório contém toda a documentação do sistema de autoatendimento de fast food, organizada por fases de desenvolvimento.

## 📁 Estrutura da Documentação

```
docs/
├── README.md                    # Este arquivo
├── fase1/                       # Documentação da Fase 1
│   ├── README.md               # Documentação específica da Fase 1
│   ├── architecture.puml       # Diagrama de arquitetura
│   ├── arquitetura.png         # Arquitetura em PNG
│   ├── fluxo_pedido_pagamento.puml
│   └── fluxo_preparo_entrega_pedido.puml
└── fase2/                       # Documentação da Fase 2
    ├── README.md               # Documentação específica da Fase 2
    ├── event-storming-fase2.puml
    └── fluxos-alternativos.puml
```

## 🎯 Fases do Projeto

### 📋 Fase 1 - Sistema Básico
- **Arquitetura**: Hexagonal básica
- **Funcionalidades**: CRUD de clientes, produtos, pedidos
- **Tecnologias**: FastAPI, PostgreSQL, Docker
- **Documentação**: Diagramas de arquitetura e fluxos básicos

**📖 [Ver documentação da Fase 1](fase1/README.md)**

### 🚀 Fase 2 - Sistema Avançado
- **Arquitetura**: Clean Architecture avançada
- **Funcionalidades**: Checkout, webhook, validações robustas
- **Tecnologias**: Kubernetes, validações avançadas
- **Documentação**: Event Storming, fluxos alternativos

**📖 [Ver documentação da Fase 2](fase2/README.md)**

## 📊 Diagramas Disponíveis

### Fase 1
- **Arquitetura Geral**: `fase1/architecture.puml` - Estrutura hexagonal do sistema
- **Fluxo de Pedido**: `fase1/fluxo_pedido_pagamento.puml` - Processo de pedido e pagamento
- **Fluxo de Preparo**: `fase1/fluxo_preparo_entrega_pedido.puml` - Preparo e entrega
- **Event Storming**: [Miro - Fase 1](https://miro.com/app/board/uXjVI2n2GlA=/) - Diagrama interativo DDD

### Fase 2
- **Event Storming**: `fase2/event-storming-fase2.puml` - Análise completa de eventos
- **Fluxos Alternativos**: `fase2/fluxos-alternativos.puml` - Cenários de erro e exceções

## 🔍 Como Visualizar os Diagramas

### 📊 Diagramas PlantUML

#### Opção 1: VS Code
1. Instale a extensão **PlantUML**
2. Abra qualquer arquivo `.puml`
3. Pressione `Alt+D` para visualizar

#### Opção 2: Online
- Use o [PlantUML Online Server](http://www.plantuml.com/plantuml/uml/)
- Cole o conteúdo do arquivo `.puml`

#### Opção 3: Local
- Use o [PlantUML Viewer](https://plantuml.com/plantuml/uml/)
- Instale o PlantUML localmente

## 📈 Evolução do Projeto

### Fase 1 → Fase 2
- **Arquitetura**: Hexagonal → Clean Architecture
- **Funcionalidades**: Básicas → Avançadas (checkout, webhook)
- **Infraestrutura**: Docker → Kubernetes
- **Documentação**: Básica → Event Storming + fluxos alternativos

## 🎯 Próximos Passos

Para evolução futura:
1. **Fase 3**: Integração real com Mercado Pago
2. **Fase 4**: Implementação de filas de mensageria
3. **Fase 5**: Métricas e monitoramento avançado

---

**📖 Para detalhes específicos de cada fase, consulte os READMEs individuais:**
- [Fase 1 - Sistema Básico](fase1/README.md)
- [Fase 2 - Sistema Avançado](fase2/README.md) 