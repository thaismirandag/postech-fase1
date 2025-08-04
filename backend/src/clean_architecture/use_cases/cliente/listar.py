from src.clean_architecture.dtos.cliente_dto import ClienteResponse
from src.clean_architecture.gateways.cliente import ClienteGateway


class ListarClienteUseCase:
    def execute(self, cliente_gateway: ClienteGateway) -> list[ClienteResponse]:
        clientes = cliente_gateway.listar()
        return [ClienteResponse(**c.__dict__) for c in clientes]
