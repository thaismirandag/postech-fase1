from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.adapters.input.api.admin.cliente_controller import router as admin_clientes
from src.adapters.input.api.admin.pedido_controller import router as admin_pedidos
from src.adapters.input.api.admin.produto_controller import router as admin_produtos
from src.adapters.input.api.public.cliente_controller import router as public_cliente
from src.adapters.input.api.public.pagamento_controller import (
    router as public_pagamento,
)
from src.adapters.input.api.public.pedido_controller import router as public_pedidos
from src.adapters.input.api.public.produto_controller import router as public_produtos
from src.adapters.input.api.public.auth_controller import router as public_login


app = FastAPI(
    title="API Autoatendimento Fast Food",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rotas públicas
app.include_router(public_login)
app.include_router(public_cliente)
app.include_router(public_produtos)
app.include_router(public_pedidos)
app.include_router(public_pagamento)


# Rotas administrativas
app.include_router(admin_pedidos)
app.include_router(admin_clientes)
app.include_router(admin_produtos)

