from uuid import UUID
from sqlalchemy.orm import Session
from datetime import datetime

from src.clean_architecture.dtos.pedido_dto import StatusPagamentoResponse
from src.clean_architecture.gateways.pagamento import PagamentoGateway
from src.clean_architecture.gateways.pedido import PedidoGateway
from src.clean_architecture.use_cases.pagamento.gerar_qrcode import GerarQRCodeUseCase
from src.clean_architecture.use_cases.pagamento.confirmar import ConfirmarPagamentoUseCase
from src.clean_architecture.external.services.mercadopago_service import MercadoPagoService

class PagamentoController:
    def exibir_qrcode(pedido_id: UUID, valor: float, db: Session):
        """Gera QR Code real do Mercado Pago"""
        pedido_gateway = PedidoGateway(db)
        pagamento_gateway = PagamentoGateway(db)
        use_case = GerarQRCodeUseCase(pedido_gateway, pagamento_gateway)
        return use_case.execute(pedido_id, valor)
    
    def consultar_status_pagamento(pedido_id: UUID, db: Session):
        """Consulta status de pagamento real do Mercado Pago"""
        try:
            # Buscar pagamento no banco
            pagamento_gateway = PagamentoGateway(db)
            pagamento = pagamento_gateway.buscar_por_pedido(pedido_id)
            
            if not pagamento:
                return {
                    "pedido_id": str(pedido_id),
                    "status_pagamento": "nao_encontrado",
                    "data_confirmacao": None,
                    "valor": 0.0,
                    "qrcode_url": None
                }
            
            # Se tem payment_id, consultar no Mercado Pago
            if pagamento.payment_id:
                mercadopago_service = MercadoPagoService()
                payment_info = mercadopago_service.consultar_pagamento(pagamento.payment_id)
                
                return {
                    "pedido_id": str(pedido_id),
                    "status_pagamento": payment_info["status"],
                    "data_confirmacao": payment_info.get("date_approved"),
                    "valor": payment_info["amount"],
                    "qrcode_url": pagamento.qrcode_url
                }
            
            # Se não tem payment_id, retornar status do banco
            return {
                "pedido_id": str(pedido_id),
                "status_pagamento": pagamento.status.value,
                "data_confirmacao": pagamento.data_processamento,
                "valor": pagamento.valor,
                "qrcode_url": pagamento.qrcode_url
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
        Processa webhook real do Mercado Pago
        """
        try:
            mercadopago_service = MercadoPagoService()
            resultado = mercadopago_service.processar_webhook(webhook_data)
            
            if resultado["success"]:
                # Atualizar pagamento no banco
                pagamento_gateway = PagamentoGateway(db)
                pedido_gateway = PedidoGateway(db)
                
                # Buscar pagamento pelo external_reference
                pagamento = pagamento_gateway.buscar_por_pedido(UUID(resultado["external_reference"]))
                
                if pagamento:
                    # Atualizar status do pagamento
                    if resultado["status"] == "approved":
                        pagamento.confirmar_pagamento(
                            resultado["payment_id"],
                            resultado["external_reference"],
                            resultado.get("date_approved")
                        )
                        
                        # Atualizar status do pedido para PAGO
                        pedido = pedido_gateway.buscar_por_id(pagamento.pedido_id)
                        if pedido:
                            from src.clean_architecture.enums.status_pedido import StatusPedido
                            pedido.atualizar_status(StatusPedido.PAGO)
                            pedido_gateway.salvar(pedido)
                    
                    pagamento_gateway.salvar(pagamento)
                
                return {
                    "status": "success",
                    "message": f"Webhook processado com sucesso. Status: {resultado['status']}",
                    "pedido_id": resultado["external_reference"],
                    "payment_id": resultado["payment_id"]
                }
            else:
                return {
                    "status": "error",
                    "message": resultado.get("message", "Erro ao processar webhook"),
                    "error": resultado.get("error")
                }
                
        except Exception as e:
            return {
                "status": "error",
                "message": f"Erro interno ao processar webhook: {str(e)}"
            }