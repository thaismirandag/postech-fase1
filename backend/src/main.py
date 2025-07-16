from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.clean_architecture.api.admin.cliente import router as admin_clientes
from src.clean_architecture.api.admin.pedido import router as admin_pedidos
from src.clean_architecture.api.admin.produto import router as admin_produtos
from src.clean_architecture.api.public.cliente import router as public_cliente
from src.clean_architecture.api.public.pagamento import (
    router as public_pagamento,
)
from src.clean_architecture.api.public.pedido import router as public_pedidos
from src.clean_architecture.api.public.produto import router as public_produtos
from src.clean_architecture.api.public.auth import router as public_login

from script.popular_tb_produtos import popular_produtos

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


popular_produtos()
print("Produtos populares inseridos com sucesso.")