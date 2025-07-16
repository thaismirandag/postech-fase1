from uuid import UUID, uuid4

from src.adapters.input.dto.pagamento_dto import PagamentoResponse
from src.domain.models.pedido import StatusPedido
from src.ports.services.pagamento_service_port import PagamentoServicePort

class GerarQRCodePagamentoUseCase:
    def __init__():
        pass
    
    def execute(self) -> PagamentoResponse:
        qrcode_id = str(uuid4())
        return PagamentoResponse(
            status="ok",
            qrcode_url=f"https://mercadopago.com/qrcode/{qrcode_id}",
            qrcode_id=qrcode_id
        )