
from sqlalchemy.orm import Session

from src.domain.models.cliente import Cliente
from src.infrastructure.db.models.cliente_model import ClienteModel
from src.ports.repositories.cliente_repository_port import ClienteRepositoryPort


class ClienteRepository(ClienteRepositoryPort):
    def __init__(self, db: Session):
        self.db = db

    def buscar_por_cpf(self, cpf: str) -> Cliente | None:
        model = self.db.query(ClienteModel).filter_by(cpf=cpf).first()
        if model:
            return Cliente(
                id=model.id,
                nome=model.nome,
                cpf=model.cpf,
                email=model.email,
                telefone=model.telefone
            )
        return None

    def salvar(self, cliente: Cliente) -> None:
        model = ClienteModel(
            nome=cliente.nome,
            cpf=cliente.cpf,
            email=cliente.email,
            telefone=cliente.telefone
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)
        cliente.id = model.id

