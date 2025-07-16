from ...interfaces.gateways.produto import ProdutoGatewayInterface

class DeletarProdutoUseCase:
    def execute(self, produto_id: str, produto_gateway: ProdutoGatewayInterface) -> None:
        produto_gateway.deletar(produto_id)
