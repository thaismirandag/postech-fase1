from fastapi import Depends
from sqlalchemy.orm import Session

from src.clean_architecture.external.db.session import get_db

def get_db_session() -> Session:
    return Depends(get_db)