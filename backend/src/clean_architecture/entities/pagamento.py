from dataclasses import dataclass
from uuid import UUID

@dataclass
class Pagamento:
    id: UUID
    pedido_id: UUID
    status: str
    qrcode_url: str
    qrcode_id: str