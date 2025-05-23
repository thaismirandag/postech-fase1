from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.adapters.input.dto.cliente_dto import ClienteCreate, ClienteResponse
from src.adapters.output.repositories.cliente_repository import ClienteRepository
from src.application.services.cliente_service import ClienteService
from src.infrastructure.db.session import get_db

router = APIRouter(prefix="/api/clientes", tags=["Clientes"])

def get_cliente_service(db: Session = Depends(get_db)) -> ClienteService:
    repository = ClienteRepository(db)
    return ClienteService(repository)

@router.post("/", response_model=ClienteResponse, summary="Criar cliente")
def criar_cliente(cliente: ClienteCreate, service: ClienteService = Depends(get_cliente_service)):
    return service.criar_cliente(cliente)

@router.get("/{cpf}", response_model=ClienteResponse, summary="Buscar cliente por CPF")
def buscar_cliente(cpf: str, service: ClienteService = Depends(get_cliente_service)):
    return service.buscar_cliente_por_cpf(cpf)
