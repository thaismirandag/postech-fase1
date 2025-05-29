from uuid import UUID

from fastapi import APIRouter, Depends

from src.adapters.input.api.dependencies import get_pagamento_service
from src.adapters.input.dto.pagamento_dto import PagamentoQRCodeResponse
from src.adapters.input.dto.pedido_dto import PedidoResponse
from src.ports.services.pagamento_service_port import PagamentoServicePort

router = APIRouter(prefix="/v1/api/pagamentos", tags=["Pagamentos"])

@router.post("/gerar-qrcode", response_model=PagamentoQRCodeResponse, summary="Simula a geração de QR Code do Mercado Pago")
def gerar_qrcode(service: PagamentoServicePort = Depends(get_pagamento_service)):
    return service.gerar_qrcode()

@router.post("/confirmar-pagamento/{pedido_id}", response_model=PedidoResponse)
def confirmar_pagamento(pedido_id: UUID, service: PagamentoServicePort = Depends(get_pagamento_service)):
    return service.confirmar_pagamento(pedido_id)
