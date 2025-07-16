from ...dtos.produto_dto import ProdutoResponse

from ...interfaces.gateways.produto import ProdutoGatewayInterface

class ListarProdutoUseCase:
    def execute(produto_gateway: ProdutoGatewayInterface) -> list[ProdutoResponse]:
        produtos = produto_gateway.listar()
        return [ProdutoResponse(**p.__dict__) for p in produtos]
