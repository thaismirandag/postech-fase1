from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.clean_architecture.controllers.cliente import ClienteController
from src.clean_architecture.dtos.cliente_dto import ClienteCreate, ClienteResponse
from src.clean_architecture.external.db.session import get_db

router = APIRouter(prefix="/v1/api/clientes", tags=["Clientes"])

@router.post("/", response_model=ClienteResponse, summary="Criar cliente")
def criar_cliente(dto: ClienteCreate, db: Session = Depends(get_db)):
    """Endpoint público para criar cliente"""
    return ClienteController.criar_ou_obter_cliente(dto, db)
