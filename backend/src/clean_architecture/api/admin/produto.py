from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.clean_architecture.dtos.produto_dto import ProdutoCreate, ProdutoResponse
from src.clean_architecture.api.security.jwt_handler import get_current_admin 
from src.clean_architecture.external.db.session import get_db

from src.clean_architecture.controllers.produto import ProdutoController

router = APIRouter(prefix="/v1/api/admin/produtos", tags=["Painel de Produtos"])

# Rotas públicas (sem autenticação)
@router.get("/", response_model=list[ProdutoResponse], summary="Listar produtos disponíveis")
def listar_produtos(db: Session = Depends(get_db)):
    return ProdutoController.listar_produtos(db)

# Rotas administrativas (com autenticação)
@router.post("/", response_model=ProdutoResponse, summary="Criar novo produto", dependencies=[Depends(get_current_admin)])
def criar_produto(dto: ProdutoCreate, db: Session = Depends(get_db)):
    return ProdutoController.criar_produto(dto, db)

@router.delete("/{produto_id}", status_code=204, summary="Remover produto", dependencies=[Depends(get_current_admin)])
def deletar_produto(produto_id: UUID, db: Session = Depends(get_db)):
    ProdutoController.deletar_produto(produto_id, db)
