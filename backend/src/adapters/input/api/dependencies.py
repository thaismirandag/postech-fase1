from fastapi import Depends
from sqlalchemy.orm import Session
from src.adapters.output.repositories.cliente_repository import ClienteRepository
from src.adapters.output.repositories.pedido_repository import PedidoRepository
from src.adapters.output.repositories.produto_repository import ProdutoRepository
from src.application.services.cliente_service import ClienteService
from src.application.services.pagamento_service import PagamentoService
from src.application.services.pedido_service import PedidoService
from src.application.services.produto_service import ProdutoService
from src.infrastructure.db.session import get_db
from src.ports.services.cliente_service_port import ClienteServicePort
from src.ports.services.pagamento_service_port import PagamentoServicePort
from src.ports.services.produto_service_port import ProdutoServicePort

def get_cliente_service(db: Session = Depends(get_db)) -> ClienteServicePort:
    cliente_repository = ClienteRepository(db)
    return ClienteService(cliente_repository)

def get_produto_service(db: Session = Depends(get_db)) -> ProdutoServicePort:
    produto_repository = ProdutoRepository(db)
    return ProdutoService(produto_repository)

def get_pedido_service(db: Session = Depends(get_db)) -> PedidoService:
    repository = PedidoRepository(db)
    return PedidoService(repository)

def get_pagamento_service() -> PagamentoServicePort:
    return PagamentoService()
