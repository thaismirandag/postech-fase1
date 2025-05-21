from fastapi import APIRouter, HTTPException
from .cliente_dto import ClienteRequestDTO, ClienteResponseDTO
from ...output.repositories.cliente_repository import ClienteRepository
from ....application.services.cliente_service import ClientService
from ....domain.models.cliente import Cliente

router = APIRouter()
client_service = ClientService(ClienteRepository())

@router.get("/client/{cpf}", response_model=ClienteResponseDTO)
def getClientByCPF(cpf: str):
    try:
        cliente = client_service.getClientByCPF(cpf)
        return ClienteResponseDTO(
            id=cliente.id,
            nome=cliente.nome,
            cpf=cliente.cpf,
            email=cliente.email,
            telefone=cliente.telefone
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/client", response_model=ClienteResponseDTO, status_code=201)
def saveClient(dto: ClienteRequestDTO):
    try:
        cliente = Cliente(id=None, **dto.dict())
        cliente = client_service.saveClient(cliente)
        return ClienteResponseDTO(
            id=cliente.id,
            nome=cliente.nome,
            cpf=cliente.cpf,
            email=cliente.email,
            telefone=cliente.telefone
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))