from uuid import UUID

from pydantic import BaseModel, EmailStr


class ClienteBase(BaseModel):
    nome: str
    cpf: str
    email: EmailStr
    telefone: str | None = None

class ClienteCreate(ClienteBase):
    pass

class ClienteResponse(ClienteBase):
    id: UUID
