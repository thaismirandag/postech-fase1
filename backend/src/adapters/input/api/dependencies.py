from src.adapters.output.repositories.cliente_repository import ClienteRepository
from src.adapters.output.repositories.produto_repository import ProdutoRepository
from src.application.services.cliente_service import ClienteService
from src.application.services.produto_service import ProdutoService
from src.ports.services.cliente_service_port import ClienteServicePort
from src.ports.services.produto_service_port import ProdutoServicePort


def get_cliente_service() -> ClienteServicePort:
    cliente_repository = ClienteRepository()
    return ClienteService(cliente_repository)

def get_produto_service() -> ProdutoServicePort:
    produto_repository = ProdutoRepository()
    return ProdutoService(produto_repository)
