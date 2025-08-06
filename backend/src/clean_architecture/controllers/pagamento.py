from uuid import UUID

from sqlalchemy.orm import Session

from src.clean_architecture.external.services.mercadopago_service import (
    MercadoPagoService,
)
from src.clean_architecture.gateways.pagamento import PagamentoGateway
from src.clean_architecture.gateways.pedido import PedidoGateway
from src.clean_architecture.use_cases.pagamento.gerar_qrcode import GerarQRCodeUseCase


class PagamentoController:
    def exibir_qrcode(pedido_id: UUID, valor: float, db: Session):
        """Gera QR Code fake para demonstração"""
        try:
            # QR Code fake simples para demonstração
            qrcode_id = f"qrcode_fake_{pedido_id}_{int(valor * 100)}"
            qrcode_url = f"https://www.mercadopago.com.br/checkout/v1/redirect?pref_id={qrcode_id}"
            
            return {
                "status": "ok",
                "qrcode_url": qrcode_url,
                "qrcode_id": qrcode_id,
                "external_reference": str(pedido_id),
                "init_point": qrcode_url,
                "sandbox_init_point": qrcode_url,
                "message": "QR Code fake gerado com sucesso para demonstração"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Erro ao gerar QR Code: {str(e)}",
                "qrcode_url": None,
                "qrcode_id": None
            }

    def consultar_status_pagamento(pedido_id: UUID, db: Session):
        """Consulta status de pagamento fake para demonstração"""
        try:
            # Status fake para demonstração
            return {
                "pedido_id": str(pedido_id),
                "status_pagamento": "approved",
                "data_confirmacao": "2024-01-15T10:30:00Z",
                "valor": 71.80,
                "qrcode_url": f"https://www.mercadopago.com.br/checkout/v1/redirect?pref_id=qrcode_fake_{pedido_id}_7180",
                "message": "Status fake consultado com sucesso para demonstração"
            }
        except Exception as e:
            return {
                "pedido_id": str(pedido_id),
                "status_pagamento": "erro",
                "data_confirmacao": None,
                "valor": 0.0,
                "qrcode_url": None,
                "erro": str(e)
            }

    def processar_webhook(webhook_data: dict, db: Session):
        """
        Processa webhook fake para demonstração
        """
        try:
            # Webhook fake para demonstração
            payment_id = webhook_data.get("data", {}).get("id", "123456789")
            external_reference = webhook_data.get("data", {}).get("external_reference", "demo-pedido-id")
            
            return {
                "status": "success",
                "message": "Webhook fake processado com sucesso para demonstração",
                "pedido_id": external_reference,
                "payment_id": str(payment_id),
                "status_pagamento": "approved",
                "data_confirmacao": "2024-01-15T10:30:00Z"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Erro interno ao processar webhook: {str(e)}"
            }
