from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from src.clean_architecture.enums.status_pedido import StatusPedido

class ItemPedidoDTO(BaseModel):
    produto_id: UUID
    quantidade: int


class PedidoCreate(BaseModel):
    cliente_id: UUID
    itens: list[ItemPedidoDTO]


class CheckoutPedidoRequest(BaseModel):
    """DTO para checkout de pedido - Fase 2"""
    cliente_id: UUID | None = None  # Cliente pode ser anônimo
    itens: list[ItemPedidoDTO]
    observacoes: str | None = None


class PedidoResponse(BaseModel):
    id: UUID
    cliente_id: UUID
    status: StatusPedido
    data_criacao: datetime
    itens: list[ItemPedidoDTO]


class AtualizarStatusPedidoDTO(BaseModel):
    status: StatusPedido


class StatusPagamentoResponse(BaseModel):
    """DTO para consulta de status de pagamento - Fase 2"""
    pedido_id: UUID
    status_pagamento: str  # "aprovado", "pendente", "rejeitado", "cancelado"
    data_confirmacao: datetime | None = None
    valor: float
    qrcode_url: str | None = None
