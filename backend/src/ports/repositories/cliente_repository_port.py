from abc import ABC, abstractmethod
from ...domain.models.cliente import Cliente

class ClienteRepositoryPort(ABC):
    @abstractmethod
    def getClientByCPF(self, cpf: str) -> Cliente | None:
        pass

    @abstractmethod
    def save(self, cliente: Cliente) -> None:
        pass