from uuid import uuid4

from src.adapters.input.dto.pagamento_dto import PagamentoQRCodeResponse
from src.ports.services.pagamento_service_port import PagamentoServicePort


class PagamentoService(PagamentoServicePort):
    def gerar_qrcode(self) -> PagamentoQRCodeResponse:
        qrcode_id = str(uuid4())
        return PagamentoQRCodeResponse(
            status="ok",
            qrcode_url=f"https://mercadopago.com/qrcode/{qrcode_id}",
            qrcode_id=qrcode_id
        )
