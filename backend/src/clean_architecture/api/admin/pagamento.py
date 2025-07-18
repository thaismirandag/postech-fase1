from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from src.clean_architecture.controllers.pagamento import PagamentoController
from src.clean_architecture.dtos.pedido_dto import StatusPagamentoResponse
from src.clean_architecture.external.db.session import get_db

router = APIRouter(prefix="/v1/api/admin/pagamento", tags=["Painel de Pagamento"])

@router.get("/qrcode", summary="Gerar QRCode real do Mercado Pago")
def exibir_qrcode(
    pedido_id: UUID = Query(..., description="ID do pedido"),
    valor: float = Query(..., description="Valor do pedido", gt=0)
):
    """Gera QR Code real do Mercado Pago para pagamento"""
    try:
        return PagamentoController.exibir_qrcode(pedido_id, valor, get_db())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{pedido_id}/status", response_model=StatusPagamentoResponse, summary="Consultar status de pagamento real - Fase 2")
def consultar_status_pagamento(pedido_id: UUID, db: Session = Depends(get_db)):
    """Consulta status de pagamento real do Mercado Pago - Fase 2"""
    return PagamentoController.consultar_status_pagamento(pedido_id, db)

@router.post("/webhook", summary="Webhook real para confirmação de pagamento - Fase 2")
def webhook_pagamento(webhook_data: dict, db: Session = Depends(get_db)):
    """
    Webhook real para receber confirmação de pagamento do Mercado Pago - Fase 2
    Implementação real conforme especificação
    """
    return PagamentoController.processar_webhook(webhook_data, db) 