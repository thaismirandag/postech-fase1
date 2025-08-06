from uuid import UUID

from src.clean_architecture.dtos.pagamento_dto import PagamentoResponse
from src.clean_architecture.external.services.mercadopago_service import (
    MercadoPagoService,
)
from src.clean_architecture.interfaces.gateways.pagamento import (
    PagamentoGatewayInterface,
)
from src.clean_architecture.interfaces.gateways.pedido import PedidoGatewayInterface


class GerarQRCodeUseCase:
    def __init__(self, pedido_gateway: PedidoGatewayInterface, pagamento_gateway: PagamentoGatewayInterface):
        self.pedido_gateway = pedido_gateway
        self.pagamento_gateway = pagamento_gateway
        self.mercadopago_service = MercadoPagoService()

    def execute(self, pedido_id: UUID) -> PagamentoResponse:
        """
        Gera QR Code real do Mercado Pago para pagamento (valor calculado automaticamente)
        """
        # Buscar pedido
        pedido = self.pedido_gateway.buscar_por_id(pedido_id)
        if not pedido:
            raise ValueError("Pedido não encontrado")

        # Calcular valor total do pedido automaticamente
        valor_total = sum(item.produto_preco * item.quantidade for item in pedido.itens)
        
        # Verificar se já existe pagamento para este pedido
        pagamento_existente = self.pagamento_gateway.buscar_por_pedido(pedido_id)
        if pagamento_existente:
            # Retornar QR Code existente se ainda válido
            if pagamento_existente.esta_pendente():
                return PagamentoResponse(
                    id=pagamento_existente.id,
                    status="ok",
                    qrcode_url=pagamento_existente.qrcode_url,
                    qrcode_id=pagamento_existente.qrcode_id
                )

        # Criar QR Code no Mercado Pago
        descricao = f"Pedido #{pedido_id} - Fast Food"
        qr_data = self.mercadopago_service.criar_pagamento_qr(
            str(pedido_id),
            valor_total,
            descricao
        )

        # Criar entidade de pagamento
        from src.clean_architecture.entities.pagamento import Pagamento
        pagamento = Pagamento.criar(
            pedido_id=pedido_id,
            valor=valor_total,
            qrcode_url=qr_data["qrcode_url"],
            qrcode_id=qr_data["preference_id"]
        )

        # Salvar pagamento
        pagamento = self.pagamento_gateway.salvar(pagamento)

        return PagamentoResponse(
            id=pagamento.id,
            status="ok",
            qrcode_url=qr_data["qrcode_url"],
            qrcode_id=qr_data["preference_id"]
        )
