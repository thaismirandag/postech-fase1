from uuid import uuid4

from src.clean_architecture.dtos.cliente_dto import ClienteCreate, ClienteResponse
from src.clean_architecture.entities.cliente import Cliente
from src.clean_architecture.gateways.cliente import ClienteGateway
from src.clean_architecture.use_cases.cliente.buscar_cliente_por_cpf import (
    BuscarClientePorCPFUseCase,
)
from src.clean_architecture.use_cases.cliente.buscar_por_email import (
    BuscarClientePorEmailUseCase,
)


class CriarOuObterClienteUseCase:
    def execute(self, cliente_create: ClienteCreate, cliente_gateway: ClienteGateway) -> ClienteResponse:

        if cliente_create.cpf:
            # Validação básica de CPF (em produção seria mais robusta)
            if len(cliente_create.cpf.replace('.', '').replace('-', '')) != 11:
                raise ValueError("CPF deve ter 11 dígitos")

            use_case = BuscarClientePorCPFUseCase()
            cliente = use_case.execute(cliente_create.cpf, cliente_gateway)
            if cliente:
                return ClienteResponse(**cliente.__dict__)

        if cliente_create.email:
            # Validação básica de email
            if '@' not in cliente_create.email or '.' not in cliente_create.email:
                raise ValueError("Email deve ter formato válido")

            use_case = BuscarClientePorEmailUseCase()
            cliente = use_case.execute(cliente_create.email, cliente_gateway)
            if cliente:
                return ClienteResponse(**cliente.__dict__)

        # Cria cliente novo (ou anônimo)
        cliente = Cliente(
            id=uuid4(),
            nome=cliente_create.nome,
            cpf=cliente_create.cpf,
            email=cliente_create.email,
        )
        cliente_gateway.salvar(cliente)
        return ClienteResponse(**cliente.__dict__)
