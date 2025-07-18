from src.clean_architecture.dtos.produto_dto import ProdutoResponse
from src.clean_architecture.interfaces.gateways.produto import ProdutoGatewayInterface

class BuscarProdutoPorCategoriaUseCase:
    def __init__(self, produto_gateway: ProdutoGatewayInterface):
        self.produto_gateway = produto_gateway

    def execute(self, categoria: str) -> list[ProdutoResponse]:
        produtos = self.produto_gateway.buscar_por_categoria(categoria)
        return [ProdutoResponse(**p.__dict__) for p in produtos]
