from src.adapters.input.dto.cliente_dto import ClienteResponse
from src.ports.repositories.cliente_repository_port import ClienteRepositoryPort

class BuscarClientePorCPFUseCase:
    def __init__(self, cliente_repository: ClienteRepositoryPort):
        self.cliente_repository = cliente_repository

    def execute(self, cpf: str) -> ClienteResponse | None:
        cliente = self.cliente_repository.buscar_por_cpf(cpf)
        if cliente:
            return ClienteResponse(**cliente.__dict__)
        return None