import os
import uuid
from typing import Optional, Dict, Any
from datetime import datetime, UTC, timedelta

import mercadopago
from mercadopago.config import RequestOptions

from src.clean_architecture.entities.pagamento import Pagamento, StatusPagamento


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
    
    def criar_pagamento_qr(self, pedido_id: str, valor: float, descricao: str) -> Dict[str, Any]:
        """
        Cria um pagamento QR Code no Mercado Pago
        """
        try:
            # Criar preferência de pagamento
            preference_data = {
                "items": [
                    {
                        "title": f"Pedido #{pedido_id}",
                        "description": descricao,
                        "quantity": 1,
                        "currency_id": "BRL",
                        "unit_price": float(valor)
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
            
            # Criar preferência
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
                "preference_id": preference["id"],
                "qrcode_url": qr_data.get("qr_code", ""),
                "qrcode_base64": qr_data.get("qr_code_base64", ""),
                "external_reference": pedido_id,
                "init_point": preference.get("init_point", ""),
                "sandbox_init_point": preference.get("sandbox_init_point", "")
            }
            
        except Exception as e:
            raise Exception(f"Erro na integração com Mercado Pago: {str(e)}")
    
    def consultar_pagamento(self, payment_id: str) -> Dict[str, Any]:
        """
        Consulta o status de um pagamento no Mercado Pago
        """
        try:
            payment_response = self.sdk.payment().get(payment_id)
            
            if payment_response["status"] != 200:
                raise Exception(f"Erro ao consultar pagamento: {payment_response}")
            
            payment = payment_response["response"]
            
            return {
                "payment_id": payment["id"],
                "status": payment["status"],
                "status_detail": payment["status_detail"],
                "external_reference": payment.get("external_reference"),
                "amount": payment["transaction_amount"],
                "currency": payment["currency_id"],
                "payment_method": payment.get("payment_method", {}).get("type"),
                "date_created": payment["date_created"],
                "date_approved": payment.get("date_approved"),
                "date_last_updated": payment["date_last_updated"]
            }
            
        except Exception as e:
            raise Exception(f"Erro ao consultar pagamento: {str(e)}")
    
    def processar_webhook(self, webhook_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Processa webhook do Mercado Pago
        """
        try:
            # Verificar tipo de notificação
            if webhook_data.get("type") == "payment":
                payment_id = webhook_data["data"]["id"]
                
                # Consultar detalhes do pagamento
                payment_info = self.consultar_pagamento(payment_id)
                
                return {
                    "success": True,
                    "payment_id": payment_id,
                    "external_reference": payment_info["external_reference"],
                    "status": payment_info["status"],
                    "status_detail": payment_info["status_detail"],
                    "amount": payment_info["amount"],
                    "date_approved": payment_info.get("date_approved")
                }
            
            return {
                "success": False,
                "message": "Tipo de notificação não suportado"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def cancelar_pagamento(self, payment_id: str) -> Dict[str, Any]:
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
            raise Exception(f"Erro ao cancelar pagamento: {str(e)}")
    
    def reembolsar_pagamento(self, payment_id: str, valor: Optional[float] = None) -> Dict[str, Any]:
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
            raise Exception(f"Erro ao reembolsar pagamento: {str(e)}")
    
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