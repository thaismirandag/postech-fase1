from fastapi import APIRouter, Depends

from src.adapters.input.api.dependencies import get_cliente_service
from src.adapters.input.dto.cliente_dto import ClienteCreate, ClienteResponse
from src.application.services.cliente_service import ClienteService

router = APIRouter(prefix="/v1/api/clientes", tags=["Clientes"])


@router.post("/", response_model=ClienteResponse, summary="Criar cliente")
def criar_cliente(cliente: ClienteCreate, service: ClienteService = Depends(get_cliente_service)):
    return service.criar_cliente(cliente)

@router.get("/{cpf}", response_model=ClienteResponse, summary="Buscar cliente por CPF")
def buscar_cliente(cpf: str, service: ClienteService = Depends(get_cliente_service)):
    return service.buscar_cliente_por_cpf(cpf)
