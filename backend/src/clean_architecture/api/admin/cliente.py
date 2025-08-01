from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.clean_architecture.external.db.session import get_db
from src.clean_architecture.api.security.jwt_handler import get_current_admin 
from src.clean_architecture.dtos.cliente_dto import ClienteCreate, ClienteResponse
from src.clean_architecture.controllers.cliente import ClienteController

router = APIRouter(prefix="/v1/api/admin/clientes", tags=["Painel de Clientes"])

# Rotas públicas (sem autenticação)
@router.post("/", response_model=ClienteResponse, summary="Criar ou obter cliente")
def criar_ou_obter_cliente(dto: ClienteCreate, db: Session = Depends(get_db)):
    return ClienteController.criar_ou_obter_cliente(dto, db)

# Rotas administrativas (com autenticação)
@router.get("/", response_model=list[ClienteResponse], summary="Listar todos os clientes", dependencies=[Depends(get_current_admin)])
def listar_clientes(db: Session = Depends(get_db)):
    return ClienteController.listar_clientes(db)

@router.get("/{cpf}", response_model=ClienteResponse, summary="Buscar cliente por CPF", dependencies=[Depends(get_current_admin)])
def buscar_cliente_por_cpf(cpf: str, db: Session = Depends(get_db)):
    return ClienteController.buscar_cliente_por_cpf(cpf, db)
