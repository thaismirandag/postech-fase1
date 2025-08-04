from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.clean_architecture.api.security.jwt_handler import get_current_admin
from src.clean_architecture.controllers.cliente import ClienteController
from src.clean_architecture.dtos.cliente_dto import ClienteResponse
from src.clean_architecture.external.db.session import get_db

router = APIRouter(prefix="/v1/api/admin/clientes", tags=["Painel de Clientes - Admin"])

# Rotas administrativas (com autenticação)
@router.get("/", response_model=list[ClienteResponse], summary="Listar todos os clientes", dependencies=[Depends(get_current_admin)])
def listar_clientes(db: Session = Depends(get_db)):
    """Lista todos os clientes (apenas admin)"""
    return ClienteController.listar_clientes(db)

@router.get("/{cpf}", response_model=ClienteResponse, summary="Buscar cliente por CPF", dependencies=[Depends(get_current_admin)])
def buscar_cliente_por_cpf(cpf: str, db: Session = Depends(get_db)):
    """Busca cliente por CPF (apenas admin)"""
    return ClienteController.buscar_cliente_por_cpf(cpf, db)
