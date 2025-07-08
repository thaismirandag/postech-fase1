from src.adapters.input.dto.cliente_dto import ClienteResponse
from src.ports.repositories.cliente_repository_port import ClienteRepositoryPort

class ListarClienteUseCase:
    def __init__(self, cliente_repository: ClienteRepositoryPort):
        self.cliente_repository = cliente_repository

    def execute(self) -> list[ClienteResponse]:
        clientes = self.cliente_repository.listar()
        return [ClienteResponse(**c.__dict__) for c in clientes]