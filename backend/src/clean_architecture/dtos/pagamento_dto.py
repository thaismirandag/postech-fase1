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
