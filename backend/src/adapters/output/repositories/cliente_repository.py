from ....ports.repositories.cliente_repository_port import ClienteRepositoryPort
from ....domain.models.cliente import Cliente

client_db = {}
next_id = 1

class ClienteRepository(ClienteRepositoryPort):
    def getClientByCPF(self, cpf) -> Cliente | None:
        data: Cliente = client_db.get(cpf)

        if data:
            return Cliente(**data)
        return None
    
    def save(self, cliente: Cliente) -> None:
        global next_id
        cliente.id = next_id
        client_db[cliente.cpf] = {
            "id": cliente.id,
            "nome": cliente.nome,
            "cpf": cliente.cpf,
            "email": cliente.email,
            "telefone": cliente.telefone
        }
        next_id += 1
