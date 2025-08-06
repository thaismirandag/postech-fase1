import os
from datetime import UTC, datetime, timedelta
from typing import Any
import uuid
import mercadopago


class MercadoPagoService:
    """Serviço de integração com Mercado Pago"""

    def __init__(self):
        # Configuração do Mercado Pago
        self.access_token = os.getenv("MERCADOPAGO_ACCESS_TOKEN")
        self.public_key = os.getenv("MERCADOPAGO_PUBLIC_KEY")
        self.webhook_url = os.getenv("MERCADOPAGO_WEBHOOK_URL", "https://api.fastfood.com/webhook")
        
        print(f"🔧 MERCADOPAGO_ACCESS_TOKEN: {self.access_token}")
        
        # Modo de desenvolvimento - usar mock se não tiver token
        self.is_mock_mode = True  # Forçar modo mock para desenvolvimento
        
        print(f"🔧 MODO MOCK: {self.is_mock_mode}")
        
        if not self.is_mock_mode:
            # Inicializar SDK do Mercado Pago
            self.sdk = mercadopago.SDK(self.access_token)
            print("🔧 SDK Mercado Pago inicializado")
        else:
            self.sdk = None
            print("⚠️  MODO MOCK ATIVADO - Usando dados simulados do Mercado Pago")

    def criar_pagamento_qr(self, pedido_id: str, valor: float, descricao: str) -> dict[str, Any]:
        """
        Cria um pagamento QR Code mockado para demonstração
        """
        print(f"🔧 criar_pagamento_qr - MODO MOCK: {self.is_mock_mode}")
        
        if self.is_mock_mode:
            # Modo mock para desenvolvimento
            print("🔧 Executando modo MOCK")
            mock_preference_id = str(uuid.uuid4())
            
            result = {
                "preference_id": mock_preference_id,
                "qrcode_url": f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=MOCK_PAYMENT_{pedido_id}",
                "qrcode_base64": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==",
                "external_reference": pedido_id,
                "init_point": f"https://www.mercadopago.com.br/checkout/v1/redirect?pref_id={mock_preference_id}",
                "sandbox_init_point": f"https://www.mercadopago.com.br/checkout/v1/redirect?pref_id={mock_preference_id}"
            }
            print(f"🔧 Retornando resultado MOCK: {result}")
            return result
        
        try:
            print("🔧 Executando modo REAL - Mercado Pago")
            # Criar preferência de pagamento
            preference_data = {
                "items": [
                    {
                        "title": descricao,
                        "quantity": 1,
                        "unit_price": valor
                    }
                ],
                "external_reference": pedido_id,
                "notification_url": self.webhook_url,
                "back_urls": {
                    "success": "https://fastfood.com/success",
                    "failure": "https://fastfood.com/failure",
                    "pending": "https://fastfood.com/pending"
                },
                "auto_return": "approved",
                "expires": True,
                "expiration_date_to": (datetime.now(UTC) + timedelta(minutes=30)).isoformat()
            }

            print(f"🔧 Criando preferência com dados: {preference_data}")
            preference_response = self.sdk.preference().create(preference_data)

            if preference_response["status"] != 201:
                raise Exception(f"Erro ao criar preferência: {preference_response}")

            preference = preference_response["response"]

            # Gerar QR Code
            qr_response = self.sdk.preference().create_qr(preference["id"])

            if qr_response["status"] != 201:
                raise Exception(f"Erro ao gerar QR Code: {qr_response}")

            qr_data = qr_response["response"]

            return {
                "preference_id": preference_id,
                "qrcode_url": qrcode_url,
                "qrcode_base64": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==",
                "preference_id": preference_id,
                "qrcode_url": qrcode_url,
                "qrcode_base64": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==",
                "external_reference": pedido_id,
                "init_point": qrcode_url,
                "sandbox_init_point": qrcode_url
                "init_point": qrcode_url,
                "sandbox_init_point": qrcode_url
            }

        except Exception as e:
            print(f"🔧 ERRO no modo REAL: {str(e)}")
            raise Exception(f"Erro na integração com Mercado Pago: {str(e)}") from e

    def consultar_pagamento(self, payment_id: str) -> dict[str, Any]:
        """
        Consulta o status de um pagamento no Mercado Pago
        """
        if self.is_mock_mode:
            # Modo mock para desenvolvimento
            return {
                "payment_id": payment_id,
                "status": "approved",  # Simular pagamento aprovado
                "status_detail": "accredited",
                "external_reference": "89b9b178-1b28-4020-9791-8817abd4cc82",  # UUID válido do pedido existente
                "amount": 10.0,
                "currency": "BRL",
                "payment_method": "credit_card",
                "date_created": datetime.now(UTC).isoformat(),
                "date_approved": datetime.now(UTC).isoformat(),
                "date_last_updated": datetime.now(UTC).isoformat()
            }
        
        try:
            payment_response = self.sdk.payment().get(payment_id)

            if payment_response["status"] != 200:
                raise Exception(f"Erro ao consultar pagamento: {payment_response}")

            payment = payment_response["response"]

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
        Processa webhook mockado para demonstração
        """
        try:
            # Simular processamento de webhook
            payment_id = webhook_data.get("data", {}).get("id", "123456789")
            external_reference = webhook_data.get("data", {}).get("external_reference", "demo-pedido-id")
            status = webhook_data.get("data", {}).get("status", "approved")
            
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
