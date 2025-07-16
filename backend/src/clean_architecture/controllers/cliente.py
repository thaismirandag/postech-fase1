from sqlalchemy.orm import Session

from src.clean_architecture.dtos.cliente_dto import ClienteCreate
from src.clean_architecture.gateways.cliente import ClienteGateway
from src.clean_architecture.use_cases.cliente.listar import ListarClienteUseCase
from src.clean_architecture.use_cases.cliente.buscar_cliente_por_cpf import BuscarClientePorCPFUseCase
from src.clean_architecture.use_cases.cliente.criar_ou_obter import CriarOuObterClienteUseCase

class ClienteController:
    def listar_clientes(db: Session):
        gateway = ClienteGateway(db)
        return ListarClienteUseCase.execute(gateway)
    
    def buscar_cliente_por_cpf(cpf: str, db: Session):
        gateway = ClienteGateway(db)
        return BuscarClientePorCPFUseCase.execute(cpf, gateway)
    
    def criar_ou_obter_cliente(dto: ClienteCreate, db: Session):
        gateway = ClienteGateway(db)
        return CriarOuObterClienteUseCase.execute(dto, gateway)