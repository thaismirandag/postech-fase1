from fastapi import APIRouter, Depends
from uuid import UUID
from src.adapters.input.api.dependencies import get_produto_service
from src.adapters.input.dto.produto_dto import ProdutoCreate, ProdutoResponse
from src.ports.services.produto_service_port import ProdutoServicePort

router = APIRouter(prefix="/v1/api/admin/produtos", tags=["Painel administrativo de Produtos"])

@router.post("/", response_model=ProdutoResponse, summary="Criar novo produto")
def criar_produto(dto: ProdutoCreate, service: ProdutoServicePort = Depends(get_produto_service)):
    return service.criar_produto(dto)

@router.delete("/{produto_id}", status_code=204, summary="Remover produto")
def deletar_produto(produto_id: UUID, service: ProdutoServicePort = Depends(get_produto_service)):
    service.deletar_produto(produto_id)