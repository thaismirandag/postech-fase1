from fastapi import APIRouter

router = APIRouter(prefix="/v1/api/public/pagamento", tags=["Painel de Pagamento"])

@router.get("/qrcode", summary="Exibir QRCode do Mercado Pago (fake)")
def exibir_qrcode():
    return {"qrcode": "https://mercadopago.com/qrcode-simulado"}
