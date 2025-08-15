# Design do Banco de Dados - Fase 3

## 🎯 **Escolha do Banco: PostgreSQL (RDS)**

### **Justificativa da Escolha:**

1. **Consistência ACID**: Garante integridade dos dados em transações complexas
2. **Suporte a JSON**: Flexibilidade para dados semi-estruturados
3. **Performance**: Excelente para consultas complexas e relatórios
4. **Escalabilidade**: Suporte a replicação e sharding
5. **Maturidade**: Sistema robusto e bem estabelecido
6. **Integração AWS**: RDS oferece backup automático, patches e monitoramento
7. **Compatibilidade**: Mantém compatibilidade com a estrutura atual (SQLAlchemy + Alembic)

## 📊 **Modelo de Dados Atualizado**

### **Diagrama ER:**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     CLIENTE     │    │    CATEGORIA    │    │     PRODUTO     │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ id (UUID)       │    │ id (UUID)       │    │ id (UUID)       │
│ cpf (VARCHAR)   │    │ nome (VARCHAR)  │    │ nome (VARCHAR)  │
│ nome (VARCHAR)  │    │ descricao (TEXT)│    │ descricao (TEXT)│
│ email (VARCHAR) │    │ ativo (BOOLEAN) │    │ preco (DECIMAL) │
│ ativo (BOOLEAN) │    │ created_at      │    │ categoria_id    │
│ created_at      │    │ updated_at      │    │ ativo (BOOLEAN) │
│ updated_at      │    └─────────────────┘    │ imagem_url      │
└─────────────────┘           │               │ estoque         │
                              │               │ created_at      │
                              │               │ updated_at      │
                              │               └─────────────────┘
                              │                       │
                              └───────────────────────┘
                                                      │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     PEDIDO      │    │   ITEM_PEDIDO   │    │   PAGAMENTO     │
├─────────────────┤    ├─────────────────┤    ├─────────────────┘
│ id (UUID)       │    │ id (UUID)       │    │ id (UUID)       │
│ cliente_id      │    │ pedido_id       │    │ pedido_id       │
│ status          │    │ produto_id      │    │ valor (DECIMAL) │
│ valor_total     │    │ quantidade      │    │ status          │
│ created_at      │    │ preco_unitario  │    │ preference_id   │
│ updated_at      │    │ created_at      │    │ qrcode_url      │
└─────────────────┘    └─────────────────┘    │ created_at      │
         │                       │            │ updated_at      │
         └───────────────────────┘            └─────────────────┘
```

## 🗃️ **Esquemas das Tabelas**

### **1. Tabela: `clientes`**
```sql
CREATE TABLE clientes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    cpf VARCHAR(11) UNIQUE NOT NULL,
    nome VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE,
    ativo BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices
CREATE INDEX idx_clientes_cpf ON clientes(cpf);
CREATE INDEX idx_clientes_email ON clientes(email);
CREATE INDEX idx_clientes_ativo ON clientes(ativo);
```

### **2. Tabela: `categorias`**
```sql
CREATE TABLE categorias (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome VARCHAR(100) NOT NULL UNIQUE,
    descricao TEXT,
    ativo BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Dados iniciais
INSERT INTO categorias (nome, descricao) VALUES
    ('Lanche', 'Hambúrgueres, sanduíches e similares'),
    ('Acompanhamento', 'Batatas fritas, saladas e similares'),
    ('Bebida', 'Refrigerantes, sucos e similares'),
    ('Sobremesa', 'Sorvetes, bolos e similares');
```

### **3. Tabela: `produtos`**
```sql
CREATE TABLE produtos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    nome VARCHAR(255) NOT NULL,
    descricao TEXT,
    preco DECIMAL(10,2) NOT NULL CHECK (preco > 0),
    categoria_id UUID NOT NULL REFERENCES categorias(id),
    ativo BOOLEAN DEFAULT true,
    imagem_url TEXT,
    estoque_disponivel INTEGER DEFAULT 0 CHECK (estoque_disponivel >= 0),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices
CREATE INDEX idx_produtos_categoria ON produtos(categoria_id);
CREATE INDEX idx_produtos_ativo ON produtos(ativo);
CREATE INDEX idx_produtos_preco ON produtos(preco);
```

### **4. Tabela: `pedidos`**
```sql
CREATE TABLE pedidos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    cliente_id UUID REFERENCES clientes(id),
    status VARCHAR(50) NOT NULL DEFAULT 'Recebido',
    valor_total DECIMAL(10,2) NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT chk_status CHECK (status IN ('Recebido', 'Em preparação', 'Pronto', 'Finalizado'))
);

-- Índices
CREATE INDEX idx_pedidos_cliente ON pedidos(cliente_id);
CREATE INDEX idx_pedidos_status ON pedidos(status);
CREATE INDEX idx_pedidos_created_at ON pedidos(created_at);
```

### **5. Tabela: `itens_pedido`**
```sql
CREATE TABLE itens_pedido (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    pedido_id UUID NOT NULL REFERENCES pedidos(id) ON DELETE CASCADE,
    produto_id UUID NOT NULL REFERENCES produtos(id),
    quantidade INTEGER NOT NULL CHECK (quantidade > 0),
    preco_unitario DECIMAL(10,2) NOT NULL CHECK (preco_unitario > 0),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices
CREATE INDEX idx_itens_pedido_pedido ON itens_pedido(pedido_id);
CREATE INDEX idx_itens_pedido_produto ON itens_pedido(produto_id);
```

### **6. Tabela: `pagamentos`**
```sql
CREATE TABLE pagamentos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    pedido_id UUID NOT NULL REFERENCES pedidos(id),
    valor DECIMAL(10,2) NOT NULL CHECK (valor > 0),
    status VARCHAR(50) NOT NULL DEFAULT 'Pendente',
    preference_id VARCHAR(255),
    qrcode_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    CONSTRAINT chk_pagamento_status CHECK (status IN ('Pendente', 'Aprovado', 'Rejeitado', 'Cancelado'))
);

-- Índices
CREATE INDEX idx_pagamentos_pedido ON pagamentos(pedido_id);
CREATE INDEX idx_pagamentos_status ON pagamentos(status);
```

## 🔄 **Migração da Estrutura Atual**

### **1. Alembic Migrations**
**Atual:**
- ✅ Alembic configurado em `backend/alembic/`
- ✅ Migrations existentes
- ✅ SQLAlchemy models definidos

**Evolução para Fase 3:**
```bash
# Estrutura de migrations para RDS
backend/alembic/
├── versions/
│   ├── 001_initial_schema.py
│   ├── 002_add_authentication.py
│   └── 003_optimize_performance.py
├── env.py
├── script.py.mako
└── alembic.ini
```

### **2. SQLAlchemy Models**
**Atual:**
- ✅ Models em `backend/src/clean_architecture/external/db/models/`
- ✅ Relacionamentos definidos
- ✅ Constraints implementados

**Evolução para Fase 3:**
```python
# Adicionar ao backend/src/clean_architecture/external/db/models/
from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

class ClienteModel(Base):
    __tablename__ = "clientes"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cpf = Column(String(11), unique=True, nullable=False, index=True)
    nome = Column(String(255), nullable=False)
    email = Column(String(255), unique=True)
    ativo = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
```

## 🔄 **Triggers e Functions**

### **1. Trigger para `updated_at`**
```sql
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Aplicar em todas as tabelas
CREATE TRIGGER update_clientes_updated_at BEFORE UPDATE ON clientes FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_produtos_updated_at BEFORE UPDATE ON produtos FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_pedidos_updated_at BEFORE UPDATE ON pedidos FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_pagamentos_updated_at BEFORE UPDATE ON pagamentos FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

### **2. Function para calcular valor total do pedido**
```sql
CREATE OR REPLACE FUNCTION calcular_valor_total_pedido(pedido_uuid UUID)
RETURNS DECIMAL AS $$
DECLARE
    total DECIMAL(10,2);
BEGIN
    SELECT COALESCE(SUM(quantidade * preco_unitario), 0)
    INTO total
    FROM itens_pedido
    WHERE pedido_id = pedido_uuid;
    
    UPDATE pedidos SET valor_total = total WHERE id = pedido_uuid;
    RETURN total;
END;
$$ LANGUAGE plpgsql;
```

## 📈 **Otimizações de Performance**

### **1. Índices Compostos**
```sql
-- Para consultas de pedidos por cliente e status
CREATE INDEX idx_pedidos_cliente_status ON pedidos(cliente_id, status);

-- Para consultas de produtos por categoria e preço
CREATE INDEX idx_produtos_categoria_preco ON produtos(categoria_id, preco);

-- Para consultas de itens por pedido e produto
CREATE INDEX idx_itens_pedido_produto ON itens_pedido(pedido_id, produto_id);
```

### **2. Particionamento (Futuro)**
```sql
-- Particionamento por data para tabela de pedidos (quando crescer)
CREATE TABLE pedidos_2024 PARTITION OF pedidos
FOR VALUES FROM ('2024-01-01') TO ('2025-01-01');
```

## 🔒 **Segurança**

### **1. Row Level Security (RLS)**
```sql
-- Permitir que clientes vejam apenas seus próprios pedidos
ALTER TABLE pedidos ENABLE ROW LEVEL SECURITY;

CREATE POLICY pedidos_cliente_policy ON pedidos
    FOR ALL USING (cliente_id = current_setting('app.current_user_id')::UUID);
```

### **2. Encryption**
- **Em trânsito**: SSL/TLS obrigatório
- **Em repouso**: Encryption automática do RDS
- **CPF**: Hash com salt para armazenamento seguro

### **3. Integração com AWS Secrets Manager**
```python
# Evolução do backend/src/clean_architecture/external/db/session.py
import boto3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def get_database_url():
    # Buscar credenciais do AWS Secrets Manager
    client = boto3.client('secretsmanager')
    secret = client.get_secret_value(SecretId='/postech/database/credentials')
    credentials = json.loads(secret['SecretString'])
    
    return f"postgresql://{credentials['username']}:{credentials['password']}@{credentials['host']}:{credentials['port']}/{credentials['database']}"

engine = create_engine(get_database_url())
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

## 📊 **Backup e Recovery**

### **1. Backup Automático**
- **Backup diário**: Retenção de 7 dias
- **Backup semanal**: Retenção de 4 semanas
- **Backup mensal**: Retenção de 12 meses

### **2. Point-in-Time Recovery**
- **Retenção**: 35 dias
- **Granularidade**: 5 minutos

## 🔍 **Monitoramento**

### **1. Métricas Importantes**
- **Connections**: Número de conexões ativas
- **CPU**: Utilização do processador
- **Memory**: Utilização de memória
- **Storage**: Espaço em disco
- **I/O**: Operações de entrada/saída

### **2. Alertas**
- **CPU > 80%**: Por 5 minutos
- **Storage > 85%**: Espaço em disco
- **Connections > 80%**: Do limite máximo
- **Replication lag > 30s**: Para read replicas

## 🔄 **Plano de Migração do Banco**

### **Fase 1: Preparação**
1. ✅ Documentar estrutura atual
2. 🔄 Configurar RDS PostgreSQL
3. 🔄 Configurar AWS Secrets Manager
4. 🔄 Testar conectividade

### **Fase 2: Migração**
1. 🔄 Executar migrations no RDS
2. 🔄 Migrar dados existentes (se houver)
3. 🔄 Atualizar configurações da aplicação
4. 🔄 Testar funcionalidades

### **Fase 3: Otimização**
1. 🔄 Configurar índices
2. 🔄 Configurar triggers
3. 🔄 Configurar backup
4. 🔄 Configurar monitoramento

---

**Próximo**: Implementar migrations e configurar CI/CD para o banco
