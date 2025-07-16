from dataclasses import dataclass
from uuid import UUID

@dataclass
class Cliente:
    id: UUID
    nome: str
    cpf: str
    email: str
