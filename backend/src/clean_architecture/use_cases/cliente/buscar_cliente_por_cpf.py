from src.clean_architecture.dtos.cliente_dto import ClienteResponse
from src.clean_architecture.gateways.cliente import ClienteGateway

class BuscarClientePorCPFUseCase:
    def execute(self, cpf: str, cliente_gateway: ClienteGateway) -> ClienteResponse | None:
        cliente = cliente_gateway.buscar_por_cpf(cpf)
        if cliente:
            return ClienteResponse(**cliente.__dict__)
        return None