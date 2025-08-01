from uuid import UUID

from src.clean_architecture.enums.status_pedido import StatusPedido

class FilaPedidos:
    def __init__(self, id: UUID, status: StatusPedido = StatusPedido.RECEBIDO, payload=None):
        self.id = id
        self.status = status
        self.payload = payload
