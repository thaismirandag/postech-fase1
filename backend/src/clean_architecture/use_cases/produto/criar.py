from uuid import uuid4

from ...dtos.produto_dto import ProdutoCreate, ProdutoResponse
from ...entities.produto import Produto
from ...interfaces.gateways.produto import ProdutoGatewayInterface


class CriarProdutoUseCase:
    def execute(self, produto_create: ProdutoCreate, produto_gateway: ProdutoGatewayInterface) -> ProdutoResponse:
        # Validação avançada dos campos
        if not produto_create.nome or len(produto_create.nome.strip()) < 3:
            raise ValueError("Nome do produto deve ter pelo menos 3 caracteres")

        if produto_create.preco <= 0:
            raise ValueError("Preço deve ser maior que zero")

        if produto_create.preco > 1000:
            raise ValueError("Preço não pode exceder R$ 1.000,00")

        # Criação do produto
        produto = Produto(
            id=uuid4(),
            nome=produto_create.nome,
            categoria=produto_create.categoria,
            preco=produto_create.preco
        )
        produto_gateway.salvar(produto)
        return ProdutoResponse(**produto.__dict__)
