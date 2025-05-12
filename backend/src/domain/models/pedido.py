import enum
from datetime import datetime


class StatusPedido(str, enum.Enum):
    pendente = "pendente"
    processando = "processando"
    finalizado = "finalizado"

class Pedido:
    def __init__(self, id, cliente_id, status=StatusPedido.pendente, data_criacao=None, itens=None):
        self.id = id
        self.cliente_id = cliente_id
        self.status = status
        self.data_criacao = data_criacao or datetime.utcnow()
        self.itens = itens or []

class ItemPedido:
    def __init__(self, pedido_id, produto_id, quantidade):
        self.pedido_id = pedido_id
        self.produto_id = produto_id
        self.quantidade = quantidade

class FilaPedidos:
    def __init__(self, id, status=StatusPedido.pendente, payload=None):
        self.id = id
        self.status = status
        self.payload = payload
