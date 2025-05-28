from fastapi import APIRouter, Depends

from src.adapters.input.api.dependencies import get_pagamento_service
from src.adapters.input.dto.pagamento_dto import PagamentoQRCodeResponse
from src.ports.services.pagamento_service_port import PagamentoServicePort

router = APIRouter(prefix="/api/pagamentos", tags=["Pagamentos"])

@router.post("/gerar-qrcode", response_model=PagamentoQRCodeResponse, summary="Simula a geração de QR Code do Mercado Pago")
def gerar_qrcode(service: PagamentoServicePort = Depends(get_pagamento_service)):
    return service.gerar_qrcode()
