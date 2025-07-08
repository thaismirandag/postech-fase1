from fastapi import APIRouter, Depends

from src.adapters.input.dto.cliente_dto import ClienteCreate, ClienteResponse
from src.application.use_cases.cliente.criar_ou_obter import CriarOuObterClienteUseCase

router = APIRouter(
    prefix="/v1/api/public/clientes",
    tags=["Painel de Clientes"]
)

@router.post("/", response_model=ClienteResponse, summary="Criar ou obter cliente")
def criar_ou_obter_cliente(
    dto: ClienteCreate,
    criarOuObterClienteUseCase: CriarOuObterClienteUseCase
):
    return criarOuObterClienteUseCase.execute(dto)
