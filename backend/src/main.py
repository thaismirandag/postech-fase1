from fastapi import FastAPI

app = FastAPI(
    title="Sistema de Autoatendimento de Fast Food",
    description="API para sistema de autoatendimento de fast food",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {"message": "Bem-vindo ao Sistema de Autoatendimento de Fast Food"}