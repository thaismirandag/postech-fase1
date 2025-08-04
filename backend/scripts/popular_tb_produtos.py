import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.clean_architecture.external.db.models.produto_model import ProdutoModel
import uuid

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/tech_challenge")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


CATEGORIAS = {
    "lanche": uuid.UUID("fcab78d9-c377-41f4-bf34-03d1a8bdbd89"),
    "acompanhamento": uuid.UUID("e8b1d3d4-738b-4207-9b2b-2c087858d7a7"),
    "bebida": uuid.UUID("6b2e43a7-8764-48ec-8f7a-65134c8c1b9e"),
    "sobremesa": uuid.UUID("d290f1ee-6c54-4b01-90e6-d701748f0851"),
}

produtos = [
    {"nome": "X-Burguer", "descricao": "Hambúrguer com queijo e salada", "categoria_id": CATEGORIAS["lanche"], "preco": 15.90, "status": True, "estoque_disponivel": 50},
    {"nome": "X-Salada", "descricao": "Hambúrguer com queijo, salada e tomate", "categoria_id": CATEGORIAS["lanche"], "preco": 16.90, "status": True, "estoque_disponivel": 45},
    {"nome": "Batata Frita", "descricao": "Batatas fritas crocantes", "categoria_id": CATEGORIAS["acompanhamento"], "preco": 9.90, "status": True, "estoque_disponivel": 100},
    {"nome": "Refrigerante", "descricao": "Refrigerante 350ml", "categoria_id": CATEGORIAS["bebida"], "preco": 6.00, "status": True, "estoque_disponivel": 80},
    {"nome": "Suco Natural", "descricao": "Suco natural de laranja 300ml", "categoria_id": CATEGORIAS["bebida"], "preco": 7.50, "status": True, "estoque_disponivel": 60},
    {"nome": "Sorvete", "descricao": "Sorvete de creme com calda", "categoria_id": CATEGORIAS["sobremesa"], "preco": 8.00, "status": True, "estoque_disponivel": 30},
]

def popular_produtos():
    session = SessionLocal()
    try:
        for p in produtos:
            produto = ProdutoModel(
                nome=p["nome"], 
                descricao=p["descricao"],
                categoria_id=p["categoria_id"], 
                preco=p["preco"],
                status=p["status"],
                estoque_disponivel=p["estoque_disponivel"]
            )
            session.add(produto)
        session.commit()
        print("Produtos inseridos com sucesso.")
    except Exception as e:
        session.rollback()
        print("Erro ao inserir produtos:", e)
    finally:
        session.close()

if __name__ == "__main__":
    popular_produtos()
