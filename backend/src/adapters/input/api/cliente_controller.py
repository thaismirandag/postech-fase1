from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ....infrastructure.db.session import SessionLocal
from .cliente_dto import ClienteRequestDTO, ClienteResponseDTO
from ...output.repositories.cliente_repository import ClienteRepository
from ....application.services.cliente_service import ClientService
from ....domain.models.cliente import Cliente

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/client/{cpf}", response_model=ClienteResponseDTO)
def getClientByCPF(cpf: str, db: Session = Depends(get_db)):
    service = ClientService(ClienteRepository(db))
    try:
        cliente = service.getClientByCPF(cpf)
        return ClienteResponseDTO(**cliente.__dict__)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/client", response_model=ClienteResponseDTO, status_code=201)
def saveClient(dto: ClienteRequestDTO, db: Session = Depends(get_db)):
    service = ClientService(ClienteRepository(db))
    try:
        cliente = Cliente(id=None, **dto.dict())
        cliente = service.saveClient(cliente)
        return ClienteResponseDTO(**cliente.__dict__)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))