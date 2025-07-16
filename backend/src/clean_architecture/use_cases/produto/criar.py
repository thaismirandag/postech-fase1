from uuid import uuid4

from ...dtos.produto_dto import ProdutoCreate, ProdutoResponse
from ...entities.produto import Produto

from ...interfaces.gateways.produto import ProdutoGatewayInterface

class CriarProdutoUseCase:
    def execute(self, produto_create: ProdutoCreate, produto_gateway: ProdutoGatewayInterface) -> ProdutoResponse:
        produto = Produto(
            id=uuid4(),
            nome=produto_create.nome,
            categoria=produto_create.categoria,
            preco=produto_create.preco
        )
        produto_gateway.salvar(produto)
        return ProdutoResponse(**produto.__dict__)
