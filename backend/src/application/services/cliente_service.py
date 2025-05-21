from ...domain.models.cliente import Cliente
from ...ports.repositories import cliente_repository_port

class ClientService:
    def __init__(self, clientRepository: cliente_repository_port):
        self.clientRepository = clientRepository

    def getClientByCPF(self, cpf: str) -> Cliente:
        cliente: Cliente = self.clientRepository.getClientByCPF(cpf)
        if not cliente:
            raise ValueError("Cliente não encontrado")
        return cliente
    
    def saveClient(self, cliente: Cliente):
        if not self.clientRepository.getClientByCPF(cliente.cpf):
            raise ValueError("Cliente não encontrado")
        self.clientRepository.save(cliente)