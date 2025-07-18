from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.clean_architecture.api.admin.auth import router as auth_router
from src.clean_architecture.api.admin.cliente import router as cliente_router
from src.clean_architecture.api.admin.pedido import router as pedido_router
from src.clean_architecture.api.admin.produto import router as produto_router
from src.clean_architecture.api.admin.pagamento import router as pagamento_router

from script.popular_tb_produtos import popular_produtos

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

# Todas as rotas unificadas (públicas e administrativas)
app.include_router(auth_router)
app.include_router(cliente_router)
app.include_router(produto_router)
app.include_router(pedido_router)
app.include_router(pagamento_router)