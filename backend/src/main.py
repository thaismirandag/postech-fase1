import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from logging.config import dictConfig
from src.logging_config import LOGGING_CONFIG

dictConfig(LOGGING_CONFIG)  # Configura o logging

logger = logging.getLogger(__name__)


# Rotas administrativas (com autenticação)
from src.clean_architecture.api.admin.auth import router as auth_router
from src.clean_architecture.api.admin.cliente import router as admin_cliente_router
from src.clean_architecture.api.admin.pedido import router as admin_pedido_router
from src.clean_architecture.api.admin.produto import router as admin_produto_router
from src.clean_architecture.api.admin.pagamento import router as admin_pagamento_router
from src.clean_architecture.api.public.cliente import router as public_cliente_router
from src.clean_architecture.api.public.pagamento import (
    router as public_pagamento_router,
)

# Rotas públicas (sem autenticação)
from src.clean_architecture.api.public.pedido import router as public_pedido_router
from src.clean_architecture.api.public.produto import router as public_produto_router

app = FastAPI(
    title="Postech Fast Food API",
    description="API para sistema de autoatendimento de fast food",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint para Kubernetes probes
@app.get("/health")
def health_check():
    """Endpoint de health check para Kubernetes probes"""
    return {"status": "healthy", "version": "2.0.0"}

app.include_router(public_pedido_router)
app.include_router(public_produto_router)
app.include_router(public_cliente_router)
app.include_router(public_pagamento_router)


app.include_router(auth_router)
app.include_router(admin_cliente_router)
app.include_router(admin_pedido_router)
app.include_router(admin_produto_router)
app.include_router(admin_pagamento_router)
