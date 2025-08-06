from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.clean_architecture.controllers.pagamento import PagamentoController
from src.clean_architecture.dtos.pagamento_dto import WebhookData
from src.clean_architecture.external.db.session import get_db

router = APIRouter(prefix="/v1/api/pagamentos", tags=["Pagamentos"])


@router.get("/{pedido_id}/qrcode", summary="Gerar QR Code para pagamento")
def gerar_qrcode(pedido_id: UUID, db: Session = Depends(get_db)):
    """Endpoint para gerar QR Code de pagamento (valor calculado automaticamente)"""
    return PagamentoController.exibir_qrcode(pedido_id, db)

@router.get("/{pedido_id}/status", summary="Consultar status do pagamento")
def consultar_status(pedido_id: UUID, db: Session = Depends(get_db)):
    """Endpoint para consultar status do pagamento"""
    return PagamentoController.consultar_status_pagamento(pedido_id, db)

@router.post("/webhook", summary="Webhook real para confirmação de pagamento")
def webhook_pagamento(webhook_data: WebhookData, db: Session = Depends(get_db)):
    """Webhook real para receber confirmação de pagamento do Mercado Pago"""
    return PagamentoController.processar_webhook(webhook_data.dict(), db)
