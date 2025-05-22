from fastapi import FastAPI
from .infrastructure.db.session import engine
from .infrastructure.db.models.base import Base
from .adapters.input.api import cliente_controller

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistema de Autoatendimento de Fast Food",
    description="API para sistema de autoatendimento de fast food",
    version="1.0.0"
)
app.include_router(cliente_controller.router)

@app.get("/")
async def root():
    return {"message": "Bem-vindo ao Sistema de Autoatendimento de Fast Food"}
