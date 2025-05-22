import uuid

from sqlalchemy import Column, String, Integer

from .base import Base

class ClienteModel(Base):
    __tablename__ = "clientes"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    nome = Column(String, nullable=False)
    cpf = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    telefone = Column(String, nullable=True)
