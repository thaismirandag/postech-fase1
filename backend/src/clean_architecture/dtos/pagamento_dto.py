from uuid import UUID

from pydantic import BaseModel


class PagamentoBase(BaseModel):
    status: str
    qrcode_url: str
    qrcode_id: str

class PagamentoCreate(PagamentoBase):
    pass

class PagamentoResponse(PagamentoBase):
    id: UUID


class WebhookData(BaseModel):
    """Modelo para dados do webhook do Mercado Pago"""
    type: str = "payment"
    data: dict
    user_id: int | None = None
    version: str | None = None
    date_created: str | None = None

    class Config:
        json_schema_extra = {
            "example": {
                "type": "payment",
                "data": {
                    "id": "123456789"
                },
                "user_id": 123456,
                "version": "1.0",
                "date_created": "2025-08-06T00:00:00.000-03:00"
            }
        }
