from uuid import UUID, uuid4

from src.adapters.input.dto.pagamento_dto import PagamentoQRCodeResponse
from src.domain.models.pedido import StatusPedido
from src.ports.services.pagamento_service_port import PagamentoServicePort


class PagamentoService(PagamentoServicePort):
    def gerar_qrcode(self) -> PagamentoQRCodeResponse:
        qrcode_id = str(uuid4())
        return PagamentoQRCodeResponse(
            status="ok",
            qrcode_url=f"https://mercadopago.com/qrcode/{qrcode_id}",
            qrcode_id=qrcode_id
        )

    def confirmar_pagamento(self, pedido_id: UUID):
        pedido = self.pedido_repository.buscar_por_id(pedido_id)
        if not pedido:
            raise Exception("Pedido não encontrado")

        pedido.status = StatusPedido.PAGO
        self.pedido_repository.salvar(pedido)
        return pedido
