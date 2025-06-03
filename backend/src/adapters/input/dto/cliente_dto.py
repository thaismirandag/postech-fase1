from uuid import UUID
from typing import Optional

from pydantic import BaseModel, EmailStr


class ClienteBase(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    cpf: Optional[str] = None  

class ClienteCreate(ClienteBase):
    pass

class ClienteResponse(ClienteBase):
    id: UUID
