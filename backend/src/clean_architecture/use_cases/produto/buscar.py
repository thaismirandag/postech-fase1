from src.clean_architecture.dtos.produto_dto import ProdutoResponse
from src.clean_architecture.interfaces.gateways.produto import ProdutoGatewayInterface


class BuscarProdutoUseCase:
    def __init__(self, produto_gateway: ProdutoGatewayInterface):
        self.produto_gateway = produto_gateway

    def execute(self, produto_id: str) -> ProdutoResponse | None:
        produto = self.produto_gateway.buscar_por_id(produto_id)
        if produto:
            return ProdutoResponse(**produto.__dict__)
        return None
