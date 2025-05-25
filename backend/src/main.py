import uvicorn
from fastapi import FastAPI

from src.adapters.input.api.cliente_controller import router as cliente_router
from src.adapters.input.api.produto_controller import router as produto_router
from src.adapters.input.api.pedido_controller import router as pedido_router
from src.infrastructure.db.session import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistema de Autoatendimento de Fast Food",
    description="API para sistema de autoatendimento de fast food",
    version="1.0.0"
)

# Inclui os routers com prefixo e tags
app.include_router(cliente_router)
app.include_router(produto_router)
app.include_router(pedido_router)

@app.get("/")
async def root():
    return {"message": "Bem-vindo ao Sistema de Autoatendimento de Fast Food"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
