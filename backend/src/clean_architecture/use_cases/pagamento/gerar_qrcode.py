from uuid import UUID, uuid4
from src.clean_architecture.dtos.pagamento_dto import PagamentoResponse
from src.clean_architecture.enums.status_pedido import StatusPedido

class GerarQRCodePagamentoUseCase:
    def __init__(self):
        pass
    
    def execute(self) -> PagamentoResponse:
        qrcode_id = str(uuid4())
        return PagamentoResponse(
            status="ok",
            qrcode_url=f"https://mercadopago.com/qrcode/{qrcode_id}",
            qrcode_id=qrcode_id
        )