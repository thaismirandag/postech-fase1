from pydantic import BaseModel
from typing import Optional

class ClienteRequestDTO(BaseModel):
    nome: str
    cpf: str
    email: str
    telefone: Optional[str] = None

class ClienteResponseDTO(ClienteRequestDTO):
    id: int