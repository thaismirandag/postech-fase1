from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.clean_architecture.controllers.produto import ProdutoController
from src.clean_architecture.dtos.produto_dto import ProdutoResponse
from src.clean_architecture.external.db.session import get_db

router = APIRouter(prefix="/v1/api/produtos", tags=["Produtos"])

@router.get("/", response_model=list[ProdutoResponse], summary="Listar produtos disponíveis")
def listar_produtos(db: Session = Depends(get_db)):
    """Endpoint público para listar produtos disponíveis"""
    return ProdutoController.listar_produtos(db)
