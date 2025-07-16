from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.clean_architecture.dtos.produto_dto import ProdutoResponse
from src.clean_architecture.controllers.produto import ProdutoController

from src.clean_architecture.external.db.session import get_db

router = APIRouter(prefix="/v1/api/public/produtos", tags=["Painel de Produtos"])

@router.get("/", response_model=list[ProdutoResponse], summary="Listar produtos disponíveis")
def listar_produtos(db: Session = Depends(get_db)):
    return ProdutoController.listar_produtos(db)
