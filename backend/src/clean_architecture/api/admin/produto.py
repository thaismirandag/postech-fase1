from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.clean_architecture.dtos.produto_dto import ProdutoCreate, ProdutoResponse
from src.clean_architecture.api.security.jwt_handler import get_current_admin 
from src.clean_architecture.external.db.session import get_db

from src.clean_architecture.controllers.produto import ProdutoController

router = APIRouter(prefix="/v1/api/admin/produtos", tags=["Painel administrativo de Produtos"], dependencies=[Depends(get_current_admin)])

@router.post("/", response_model=ProdutoResponse, summary="Criar novo produto")
def criar_produto( dto: ProdutoCreate, db: Session = Depends(get_db) ):
    return ProdutoController.criar_produto(dto, db)

@router.delete("/{produto_id}", status_code=204, summary="Remover produto")
def deletar_produto( produto_id: UUID, db: Session = Depends(get_db) ):
    ProdutoController.deletar_produto(produto_id, db)
