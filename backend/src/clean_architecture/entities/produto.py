from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

@dataclass
class Produto:
    id: UUID
    nome: str
    categoria: str
    preco: Decimal

    def __post_init__(self):
        if not self.nome:
            raise ValueError("Nome do produto é obrigatório")
        if not self.categoria:
            raise ValueError("Categoria do produto é obrigatória")
        if self.preco <= 0:
            raise ValueError("Preço do produto deve ser maior que zero")
