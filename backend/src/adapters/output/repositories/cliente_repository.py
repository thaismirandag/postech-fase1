from uuid import UUID

from sqlalchemy.orm import Session

from src.domain.models.cliente import Cliente
from src.infrastructure.db.models.cliente_model import ClienteModel
from src.ports.repositories.cliente_repository_port import ClienteRepositoryPort


class ClienteRepository(ClienteRepositoryPort):
    def __init__(self, db: Session):
        self.db = db

    def salvar(self, cliente: Cliente) -> None:
        cliente_model = ClienteModel(**cliente.__dict__)
        self.db.add(cliente_model)
        self.db.commit()

    def buscar_por_cpf(self, cpf: str) -> Cliente | None:
        model = self.db.query(ClienteModel).filter_by(cpf=cpf).first()
        if model:
            return Cliente(**model.__dict__)
        return None

    def buscar_por_email(self, email: str) -> Cliente | None:
        model = self.db.query(ClienteModel).filter_by(email=email).first()
        if model:
            return Cliente(**model.__dict__)
        return None

    def buscar_por_id(self, cliente_id: UUID) -> Cliente | None:
        model = self.db.query(ClienteModel).filter_by(id=cliente_id).first()
        if model:
            return Cliente(**model.__dict__)
        return None

