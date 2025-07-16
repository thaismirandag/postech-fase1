from fastapi import APIRouter

from src.clean_architecture.controllers.pagamento import PagamentoController

router = APIRouter(prefix="/v1/api/public/pagamento", tags=["Painel de Pagamento"])

@router.get("/qrcode", summary="Exibir QRCode do Mercado Pago (fake)")
def exibir_qrcode():
    # {"qrcode": "https://mercadopago.com/qrcode-simulado"}
    return PagamentoController.exibir_qrcode()
