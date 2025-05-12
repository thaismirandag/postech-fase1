
class Cliente:
    def __init__(self, id, nome, cpf, email, telefone=None):
        self.id = id
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.telefone = telefone
