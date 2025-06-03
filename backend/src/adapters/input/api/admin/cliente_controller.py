from uuid import UUID

from fastapi import APIRouter, Depends

from src.adapters.input.api.dependencies import get_cliente_service
from src.adapters.input.dto.cliente_dto import ClienteResponse
from src.ports.services.cliente_service_port import ClienteServicePort

router = APIRouter(prefix="/v1/api/admin/clientes", tags=["Painel administrativo de Clientes"])

@router.get("/", response_model=list[ClienteResponse], summary="Listar todos os clientes")
def listar_clientes(service: ClienteServicePort = Depends(get_cliente_service)):
    return service.listar_clientes()

@router.get("/{cliente_id}", response_model=ClienteResponse, summary="Buscar cliente por ID")
def buscar_cliente(cliente_id: UUID, service: ClienteServicePort = Depends(get_cliente_service)):
    return service.buscar_por_id(cliente_id)
