from src.clean_architecture.dtos.cliente_dto import ClienteResponse
from src.clean_architecture.gateways.cliente import ClienteGateway

class BuscarClientePorEmailUseCase:
    def execute(self, email: str, cliente_gateway: ClienteGateway) -> ClienteResponse | None:
        cliente = cliente_gateway.buscar_por_email(email)
        if cliente:
            return ClienteResponse(**cliente.__dict__)
        return None