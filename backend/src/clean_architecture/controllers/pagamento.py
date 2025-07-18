from uuid import UUID
from sqlalchemy.orm import Session
from datetime import datetime

from src.clean_architecture.dtos.pedido_dto import StatusPagamentoResponse
from src.clean_architecture.gateways.pagamento import PagamentoGateway
from src.clean_architecture.gateways.pedido import PedidoGateway
from src.clean_architecture.use_cases.pagamento.consultar_status import ConsultarStatusPagamentoUseCase
from src.clean_architecture.use_cases.pagamento.webhook import ProcessarWebhookUseCase

class PagamentoController:
    def exibir_qrcode():
        """Mock do QRCode do Mercado Pago"""
        return {
            "qrcode": "https://mercadopago.com/qrcode-simulado",
            "qrcode_id": "mp_qrcode_123456",
            "status": "pendente"
        }
    
    def consultar_status_pagamento(pedido_id, db):
        """Consulta status de pagamento do pedido - Fase 2 (Mock)"""
        return {
            "pedido_id": str(pedido_id),
            "status_pagamento": "pendente",
            "data_confirmacao": None,
            "valor": 45.50,
            "qrcode_url": "https://mercadopago.com/qrcode/123456"
        }
    
    def processar_webhook(webhook_data, db):
        """
        Processa webhook do Mercado Pago - Fase 2 (Mock)
        Implementação clara quanto ao Webhook conforme especificação
        """
        return {
            "status": "success",
            "message": "Webhook processado com sucesso. Status: approved",
            "pedido_id": webhook_data.get("data", {}).get("external_reference", "unknown"),
            "payment_id": webhook_data.get("data", {}).get("id", "unknown")
        }