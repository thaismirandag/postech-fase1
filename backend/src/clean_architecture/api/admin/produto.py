from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.clean_architecture.api.security.jwt_handler import get_current_admin
from src.clean_architecture.controllers.produto import ProdutoController
from src.clean_architecture.dtos.produto_dto import ProdutoCreate, ProdutoResponse
from src.clean_architecture.external.db.session import get_db

router = APIRouter(prefix="/v1/api/admin/produtos", tags=["Painel de Produtos - Admin"])

# Rotas administrativas (com autenticação)
@router.post("/", response_model=ProdutoResponse, summary="Criar novo produto", dependencies=[Depends(get_current_admin)])
def criar_produto(dto: ProdutoCreate, db: Session = Depends(get_db)):
    """Cria um novo produto (apenas admin)"""
    return ProdutoController.criar_produto(dto, db)

@router.delete("/{produto_id}", status_code=204, summary="Remover produto", dependencies=[Depends(get_current_admin)])
def deletar_produto(produto_id: UUID, db: Session = Depends(get_db)):
    """Remove um produto (apenas admin)"""
    ProdutoController.deletar_produto(produto_id, db)
