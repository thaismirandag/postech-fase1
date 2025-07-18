from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.clean_architecture.controllers.pagamento import PagamentoController
from src.clean_architecture.dtos.pedido_dto import StatusPagamentoResponse
from src.clean_architecture.external.db.session import get_db

router = APIRouter(prefix="/v1/api/public/pagamento", tags=["Painel de Pagamento"])

@router.get("/qrcode", summary="Exibir QRCode do Mercado Pago (fake)")
def exibir_qrcode():
    # {"qrcode": "https://mercadopago.com/qrcode-simulado"}
    return PagamentoController.exibir_qrcode()

@router.get("/{pedido_id}/status", response_model=StatusPagamentoResponse, summary="Consultar status de pagamento - Fase 2")
def consultar_status_pagamento(pedido_id: UUID, db: Session = Depends(get_db)):
    """Consulta status de pagamento do pedido - Fase 2"""
    return PagamentoController.consultar_status_pagamento(pedido_id, db)

@router.post("/webhook", summary="Webhook para confirmação de pagamento - Fase 2")
def webhook_pagamento(webhook_data: dict, db: Session = Depends(get_db)):
    """
    Webhook para receber confirmação de pagamento aprovado ou recusado - Fase 2
    Implementação clara quanto ao Webhook conforme especificação
    """
    return PagamentoController.processar_webhook(webhook_data, db)
