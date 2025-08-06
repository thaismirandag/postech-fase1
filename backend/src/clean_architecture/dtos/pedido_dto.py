from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from src.clean_architecture.enums.status_pedido import StatusPedido


class ItemPedidoDTO(BaseModel):
    produto_id: UUID
    quantidade: int


class ItemPedidoResponseDTO(BaseModel):
    """DTO para resposta de item do pedido com descrição do produto"""
    produto_id: UUID
    produto_nome: str
    produto_preco: float
    quantidade: int
    subtotal: float


class PedidoCreate(BaseModel):
    cliente_id: UUID | None = None  # Cliente pode ser anônimo
    itens: list[ItemPedidoDTO]
    observacoes: str | None = None


class CheckoutPedidoRequest(BaseModel):
    """DTO para checkout de pedido - Fase 2"""
    cliente_id: UUID | None = None  # Cliente pode ser anônimo
    itens: list[ItemPedidoDTO]
    observacoes: str | None = None


class PedidoResponse(BaseModel):
    """DTO para resposta de pedido com descrições completas"""
    id: UUID
    cliente_id: UUID | None = None  # Cliente pode ser anônimo
    cliente_nome: str | None = None
    status: StatusPedido
    data_criacao: datetime
    itens: list[ItemPedidoResponseDTO]
    valor_total: float
    observacoes: str | None = None


class AtualizarStatusPedidoDTO(BaseModel):
    status: StatusPedido


class StatusPagamentoResponse(BaseModel):
    """DTO para consulta de status de pagamento - Fase 2"""
    pedido_id: UUID
    status_pagamento: str  # "aprovado", "pendente", "rejeitado", "cancelado"
    data_confirmacao: datetime | None = None
    valor: float
    qrcode_url: str | None = None
