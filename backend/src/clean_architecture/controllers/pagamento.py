import logging
from uuid import UUID

from sqlalchemy.orm import Session

from src.clean_architecture.external.services.mercadopago_service import (
    MercadoPagoService,
)
from src.clean_architecture.gateways.pagamento import PagamentoGateway
from src.clean_architecture.gateways.pedido import PedidoGateway
from src.clean_architecture.use_cases.pagamento.gerar_qrcode import GerarQRCodeUseCase

logger = logging.getLogger(__name__)


class PagamentoController:
    def exibir_qrcode(self, pedido_id: UUID, db: Session):
        """Gera QR Code real do Mercado Pago (valor calculado automaticamente)"""
        pedido_gateway = PedidoGateway(db)
        pagamento_gateway = PagamentoGateway(db)
        use_case = GerarQRCodeUseCase(pedido_gateway, pagamento_gateway)
        return use_case.execute(pedido_id)

    def consultar_status_pagamento(self, pedido_id: UUID, db: Session):
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

    def processar_webhook(self, webhook_data: dict, db: Session):
        """
        Processa webhook fake para demonstração
        """
        
        logger.info(f"WEBHOOK RECEBIDO: {webhook_data}")
        
        try:
            mercadopago_service = MercadoPagoService()
            resultado = mercadopago_service.processar_webhook(webhook_data)
            
            logger.info(f"RESULTADO PROCESSAMENTO: {resultado}")

            if resultado["success"]:
                logger.info(f"WEBHOOK VÁLIDO - Processando pagamento...")
                
                # Atualizar pagamento no banco
                pagamento_gateway = PagamentoGateway(db)
                pedido_gateway = PedidoGateway(db)

                # Buscar pagamento pelo external_reference
                external_ref = resultado["external_reference"]
                if external_ref == "mock_pedido_id":
                    # Em modo mock, buscar o pagamento mais recente ou usar um ID padrão
                    pagamentos = pagamento_gateway.listar()
                    if pagamentos:
                        pagamento = pagamentos[0]  # Pegar o primeiro pagamento encontrado
                    else:
                        return {
                            "status": "error",
                            "message": "Nenhum pagamento encontrado para processar"
                        }
                else:
                    pagamento = pagamento_gateway.buscar_por_pedido(UUID(external_ref))
                
                logger.info(f"PAGAMENTO ENCONTRADO: {pagamento is not None}")

                if pagamento:
                    logger.info(f"STATUS DO PAGAMENTO: {resultado['status']}")
                    
                    # Atualizar status do pagamento
                    if resultado["status"] == "approved":
                        logger.info(f"PAGAMENTO APROVADO! Atualizando pedido...")
                        
                        pagamento.confirmar_pagamento(
                            resultado["payment_id"],
                            resultado["external_reference"],
                            resultado.get("date_approved")
                        )

                        # Atualizar status do pedido para PAGO
                        pedido = pedido_gateway.buscar_por_id(pagamento.pedido_id)
                        if pedido:
                            from src.clean_architecture.enums.status_pedido import (
                                StatusPedido,
                            )
                            pedido.atualizar_status(StatusPedido.PAGO)
                            pedido_gateway.salvar(pedido)
                            logger.info(f"PEDIDO ATUALIZADO PARA PAGO: {pedido.id}")

                    pagamento_gateway.salvar(pagamento)
                    logger.info(f"PAGAMENTO SALVO NO BANCO")

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
