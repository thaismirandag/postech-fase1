from fastapi import APIRouter, Depends

from src.adapters.input.api.dependencies import get_produto_service
from src.adapters.input.dto.produto_dto import ProdutoCreate, ProdutoResponse
from src.application.services.produto_service import ProdutoService

router = APIRouter(prefix="/api/produtos", tags=["Produtos"])

@router.post("/", response_model=ProdutoResponse, summary="Criar Produto")
def criar_produto(
    produto: ProdutoCreate,
    service: ProdutoService = Depends(get_produto_service),
):
    return service.criar_produto(produto)

@router.get("/", response_model=list[ProdutoResponse], summary="Listar Produtos")
def listar_produtos(
    service: ProdutoService = Depends(get_produto_service),
):
    return service.listar_produtos()

@router.get("/{produto_id}", response_model=ProdutoResponse, summary="Buscar Produto por ID")
def buscar_produto(
    produto_id: str,
    service: ProdutoService = Depends(get_produto_service),
):
    return service.buscar_produto(produto_id)

@router.get("/categoria/{categoria}", response_model=list[ProdutoResponse], summary="Buscar produtos por categoria")
def buscar_por_categoria(categoria: str, service: ProdutoService = Depends(get_produto_service)):
    return service.buscar_por_categoria(categoria)

@router.delete("/{produto_id}", status_code=204, summary="Deletar Produto")
def deletar_produto(
    produto_id: str,
    service: ProdutoService = Depends(get_produto_service),
):
    service.deletar_produto(produto_id)


