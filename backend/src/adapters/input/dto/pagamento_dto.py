from pydantic import BaseModel


class PagamentoQRCodeResponse(BaseModel):
    status: str
    qrcode_url: str
    qrcode_id: str
