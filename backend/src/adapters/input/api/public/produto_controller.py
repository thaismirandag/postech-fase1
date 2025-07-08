from fastapi import APIRouter

from src.adapters.input.dto.produto_dto import ProdutoResponse
from src.application.use_cases.produto.listar import ListarProdutoUseCase

router = APIRouter(prefix="/v1/api/public/produtos", tags=["Painel de Produtos"])

@router.get("/", response_model=list[ProdutoResponse], summary="Listar produtos disponíveis")
def listar_produtos(
        listarProdutoUseCase: ListarProdutoUseCase
    ):
    return listarProdutoUseCase.execute()
