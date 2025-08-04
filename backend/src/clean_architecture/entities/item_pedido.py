from dataclasses import dataclass
from uuid import UUID


@dataclass
class ItemPedido:
    produto_id: UUID
    quantidade: int
    produto_nome: str | None = None
    produto_preco: float | None = None

    def calcular_subtotal(self) -> float:
        """Calcula o subtotal do item"""
        if self.produto_preco is None:
            return 0.0
        return self.produto_preco * self.quantidade

