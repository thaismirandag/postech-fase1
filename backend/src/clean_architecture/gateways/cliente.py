from uuid import UUID
from sqlalchemy.orm import Session

from src.clean_architecture.interfaces.gateways.cliente import ClienteGatewayInterface
from src.clean_architecture.entities.cliente import Cliente

from src.clean_architecture.external.db.models.cliente_model import ClienteModel

class ClienteGateway(ClienteGatewayInterface):
    def __init__(self, db: Session):
        self.db = db

    def salvar(self, cliente: Cliente) -> Cliente:
        cliente_model = ClienteModel(
            id=cliente.id,
            nome=cliente.nome,
            cpf=cliente.cpf,
            email=cliente.email
        )
        self.db.add(cliente_model)
        self.db.commit()
        self.db.refresh(cliente_model)
        return self._to_domain(cliente_model)

    def buscar_por_cpf(self, cpf: str) -> Cliente | None:
        model = self.db.query(ClienteModel).filter_by(cpf=cpf).first()
        return self._to_domain(model) if model else None

    def buscar_por_email(self, email: str) -> Cliente | None:
        model = self.db.query(ClienteModel).filter_by(email=email).first()
        return self._to_domain(model) if model else None

    def buscar_por_id(self, cliente_id: UUID) -> Cliente | None:
        model = self.db.query(ClienteModel).filter_by(id=cliente_id).first()
        return self._to_domain(model) if model else None

    def listar(self) -> list[Cliente]:
        models = self.db.query(ClienteModel).all()
        return [self._to_domain(m) for m in models]

    def _to_domain(self, model: ClienteModel) -> Cliente:
        return Cliente(
            id=model.id,
            nome=model.nome,
            cpf=model.cpf,
            email=model.email
        )

