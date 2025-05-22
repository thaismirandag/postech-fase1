from sqlalchemy.orm import Session
from ....ports.repositories.cliente_repository_port import ClienteRepositoryPort
from ....domain.models.cliente import Cliente
from ....infrastructure.db.models.cliente_model import ClienteModel

client_db = {}
next_id = 1

class ClienteRepository(ClienteRepositoryPort):
    def __init__(self, db: Session):
        self.db = db

    def getClientByCPF(self, cpf) -> Cliente | None:
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
    
    def save(self, cliente: Cliente) -> None:
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
        return cliente
