from uuid import UUID

from sqlalchemy.orm import Session

from src.clean_architecture.entities.pagamento import Pagamento, StatusPagamento
from src.clean_architecture.external.db.models.pagamento_model import PagamentoModel
from src.clean_architecture.interfaces.gateways.pagamento import (
    PagamentoGatewayInterface,
)


class PagamentoGateway(PagamentoGatewayInterface):
    def __init__(self, db: Session):
        self.db = db

    def salvar(self, pagamento: Pagamento) -> Pagamento:
        pagamento_model = self.db.query(PagamentoModel).filter_by(id=pagamento.id).first()

        if not pagamento_model:
            pagamento_model = PagamentoModel(
                id=pagamento.id,
                pedido_id=pagamento.pedido_id,
                status=pagamento.status.value,
                data_criacao=pagamento.data_criacao,
                data_confirmacao=pagamento.data_processamento,
                qrcode_url=pagamento.qrcode_url,
                qrcode_id=pagamento.qrcode_id,
                external_reference=pagamento.external_reference,
                payment_id=pagamento.payment_id,
                valor=pagamento.valor
            )
            self.db.add(pagamento_model)
        else:
            pagamento_model.status = pagamento.status.value
            pagamento_model.data_confirmacao = pagamento.data_processamento
            pagamento_model.qrcode_url = pagamento.qrcode_url
            pagamento_model.qrcode_id = pagamento.qrcode_id
            pagamento_model.external_reference = pagamento.external_reference
            pagamento_model.payment_id = pagamento.payment_id
            pagamento_model.valor = pagamento.valor

        self.db.commit()
        self.db.refresh(pagamento_model)
        return self._converter_para_entidade(pagamento_model)

    def buscar_por_id(self, pagamento_id: UUID) -> Pagamento | None:
        model = self.db.query(PagamentoModel).filter_by(id=pagamento_id).first()
        if model:
            return self._converter_para_entidade(model)
        return None

    def buscar_por_pedido(self, pedido_id: UUID) -> Pagamento | None:
        model = self.db.query(PagamentoModel).filter_by(pedido_id=pedido_id).first()
        if model:
            return self._converter_para_entidade(model)
        return None

    def atualizar_status(self, pagamento_id: UUID, status: str) -> None:
        pagamento_model = self.db.query(PagamentoModel).filter_by(id=pagamento_id).first()
        if not pagamento_model:
            raise ValueError("Pagamento não encontrado")

        pagamento_model.status = status
        self.db.commit()

    def listar_por_status(self, status: str) -> list[Pagamento]:
        pagamentos_model = self.db.query(PagamentoModel).filter_by(status=status).all()
        return [self._converter_para_entidade(p) for p in pagamentos_model]

    def _converter_para_entidade(self, model: PagamentoModel) -> Pagamento:
        return Pagamento(
            id=model.id,
            pedido_id=model.pedido_id,
            status=StatusPagamento(model.status),
            qrcode_url=model.qrcode_url,
            qrcode_id=model.qrcode_id,
            external_reference=model.external_reference,
            payment_id=model.payment_id,
            data_criacao=model.data_criacao,
            data_processamento=model.data_confirmacao,
            valor=model.valor
        )
