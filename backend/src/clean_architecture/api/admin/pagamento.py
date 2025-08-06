from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from src.clean_architecture.controllers.pagamento import PagamentoController
from src.clean_architecture.external.db.session import get_db

router = APIRouter(prefix="/v1/api/admin/pagamento", tags=["Pagamento - Administrativo"])

@router.get("/qrcode", summary="Gerar QRCode do Mercado Pago (Mock)")
def exibir_qrcode(
    db: Session = Depends(get_db),
    pedido_id: UUID = Query(..., description="ID do pedido"),
    valor: float = Query(..., description="Valor do pedido", gt=0)
):
    """Gera QR Code fake para demonstração"""
    try:
        return PagamentoController.exibir_qrcode(pedido_id, valor, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

@router.get("/{pedido_id}/status", summary="Consultar status de pagamento (Mock)")
def consultar_status_pagamento(pedido_id: UUID, db: Session = Depends(get_db)):
    """Consulta status de pagamento fake para demonstração"""
    try:
        return PagamentoController.consultar_status_pagamento(pedido_id, db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

@router.post("/webhook", summary="Webhook para confirmação de pagamento (Mock)")
def webhook_pagamento(webhook_data: dict, db: Session = Depends(get_db)):
    """Processa webhook fake para demonstração"""
    try:
        return PagamentoController.processar_webhook(webhook_data, db)
    except Exception as e:
        return {
            "status": "error",
            "message": "Erro ao processar webhook fake",
            "error": str(e)
        } 