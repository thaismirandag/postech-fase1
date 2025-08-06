import os
from datetime import UTC, datetime, timedelta
from typing import Any

import mercadopago


class MercadoPagoService:
    """Serviço de integração com Mercado Pago"""

    def __init__(self):
        # Configuração do Mercado Pago
        self.access_token = os.getenv("MERCADOPAGO_ACCESS_TOKEN")
        self.public_key = os.getenv("MERCADOPAGO_PUBLIC_KEY")
        self.webhook_url = os.getenv("MERCADOPAGO_WEBHOOK_URL", "https://api.fastfood.com/webhook")

        if not self.access_token:
            raise ValueError("MERCADOPAGO_ACCESS_TOKEN não configurado")

        # Inicializar SDK do Mercado Pago
        self.sdk = mercadopago.SDK(self.access_token)

    def criar_pagamento_qr(self, pedido_id: str, valor: float, descricao: str) -> dict[str, Any]:
        """
        Cria um pagamento QR Code mockado para demonstração
        """
        try:
            # Simular criação de preferência
            preference_id = f"pref_{pedido_id}_{int(valor * 100)}"
            
            # Gerar QR Code mockado
            qrcode_url = f"https://www.mercadopago.com.br/checkout/v1/redirect?pref_id={preference_id}"
            
            return {
                "preference_id": preference_id,
                "qrcode_url": qrcode_url,
                "qrcode_base64": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==",
                "external_reference": pedido_id,
                "init_point": qrcode_url,
                "sandbox_init_point": qrcode_url
            }

        except Exception as e:
            raise Exception(f"Erro na integração com Mercado Pago: {str(e)}") from e

    def consultar_pagamento(self, payment_id: str) -> dict[str, Any]:
        """
        Consulta o status de um pagamento mockado para demonstração
        """
        try:
            # Simular consulta de pagamento
            return {
                "payment_id": payment_id,
                "status": "approved",
                "status_detail": "accredited",
                "external_reference": "demo-pedido-id",
                "amount": 71.80,
                "currency": "BRL",
                "payment_method": "credit_card",
                "date_created": datetime.now(UTC).isoformat(),
                "date_approved": datetime.now(UTC).isoformat(),
                "date_last_updated": datetime.now(UTC).isoformat()
            }

        except Exception as e:
            raise Exception(f"Erro ao consultar pagamento: {str(e)}") from e

    def processar_webhook(self, webhook_data: dict[str, Any]) -> dict[str, Any]:
        """
        Processa webhook mockado para demonstração
        """
        try:
            # Simular processamento de webhook
            payment_id = webhook_data.get("data", {}).get("id", "123456789")
            external_reference = webhook_data.get("data", {}).get("external_reference", "demo-pedido-id")
            status = webhook_data.get("data", {}).get("status", "approved")
            
            return {
                "success": True,
                "payment_id": str(payment_id),
                "external_reference": external_reference,
                "status": status,
                "status_detail": "accredited",
                "amount": 71.80,
                "date_approved": datetime.now(UTC).isoformat()
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def cancelar_pagamento(self, payment_id: str) -> dict[str, Any]:
        """
        Cancela um pagamento no Mercado Pago
        """
        try:
            cancel_data = {
                "status": "cancelled"
            }

            cancel_response = self.sdk.payment().update(payment_id, cancel_data)

            if cancel_response["status"] != 200:
                raise Exception(f"Erro ao cancelar pagamento: {cancel_response}")

            return {
                "success": True,
                "payment_id": payment_id,
                "status": "cancelled"
            }

        except Exception as e:
            raise Exception(f"Erro ao cancelar pagamento: {str(e)}") from e

    def reembolsar_pagamento(self, payment_id: str, valor: float | None = None) -> dict[str, Any]:
        """
        Reembolsa um pagamento no Mercado Pago
        """
        try:
            refund_data = {}
            if valor:
                refund_data["amount"] = valor

            refund_response = self.sdk.refund().create(payment_id, refund_data)

            if refund_response["status"] != 201:
                raise Exception(f"Erro ao reembolsar pagamento: {refund_response}")

            refund = refund_response["response"]

            return {
                "success": True,
                "refund_id": refund["id"],
                "payment_id": payment_id,
                "amount": refund["amount"],
                "status": refund["status"]
            }

        except Exception as e:
            raise Exception(f"Erro ao reembolsar pagamento: {str(e)}") from e

    def validar_webhook_signature(self, signature: str, body: str) -> bool:
        """
        Valida a assinatura do webhook do Mercado Pago
        """
        try:
            # Implementar validação de assinatura se necessário
            # Por enquanto, retorna True para desenvolvimento
            return True
        except Exception:
            return False
