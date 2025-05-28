from datetime import datetime
from enum import Enum


class StatusPedido(str, Enum):
    RECEBIDO = "Recebido"
    PREPARANDO = "Em preparação"
    PRONTO = "Pronto"
    FINALIZADO = "Finalizado"

class Pedido:
    def __init__(self, id, cliente_id, status=StatusPedido.RECEBIDO, data_criacao=None, itens=None):
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
    def __init__(self, id, status=StatusPedido.RECEBIDO, payload=None):
        self.id = id
        self.status = status
        self.payload = payload
