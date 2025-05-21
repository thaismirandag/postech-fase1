from fastapi import FastAPI
from .adapters.input.api import cliente_controller

app = FastAPI(
    title="Sistema de Autoatendimento de Fast Food",
    description="API para sistema de autoatendimento de fast food",
    version="1.0.0"
)
app.include_router(cliente_controller.router)

@app.get("/")
async def root():
    return {"message": "Bem-vindo ao Sistema de Autoatendimento de Fast Food"}
