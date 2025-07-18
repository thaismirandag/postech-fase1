from uuid import UUID, uuid4
from datetime import UTC, datetime
from typing import Optional
from enum import Enum


class StatusPagamento(str, Enum):
    PENDENTE = "pendente"
    APROVADO = "aprovado"
    REJEITADO = "rejeitado"
    CANCELADO = "cancelado"
    EXPIRADO = "expirado"


class Pagamento:
    def __init__(
        self,
        id: UUID,
        pedido_id: UUID,
        status: StatusPagamento = StatusPagamento.PENDENTE,
        qrcode_url: Optional[str] = None,
        qrcode_id: Optional[str] = None,
        external_reference: Optional[str] = None,
        payment_id: Optional[str] = None,
        data_criacao: datetime | None = None,
        data_processamento: datetime | None = None,
        valor: float = 0.0,
    ):
        self.id = id
        self.pedido_id = pedido_id
        self.status = status
        self.qrcode_url = qrcode_url
        self.qrcode_id = qrcode_id
        self.external_reference = external_reference
        self.payment_id = payment_id
        self.data_criacao = data_criacao or datetime.now(UTC)
        self.data_processamento = data_processamento
        self.valor = valor
        
        # Validações de domínio
        self._validar_pagamento()

    @classmethod
    def criar(
        cls,
        pedido_id: UUID,
        valor: float,
        qrcode_url: Optional[str] = None,
        qrcode_id: Optional[str] = None,
    ) -> "Pagamento":
        """Factory method para criar um novo pagamento com validações"""
        if valor <= 0:
            raise ValueError("Valor deve ser maior que zero")
        
        if valor > 10000:
            raise ValueError("Valor não pode ser maior que R$ 10.000,00")
        
        return cls(
            id=uuid4(),
            pedido_id=pedido_id,
            status=StatusPagamento.PENDENTE,
            qrcode_url=qrcode_url,
            qrcode_id=qrcode_id,
            data_criacao=datetime.now(UTC),
            valor=valor,
        )

    def confirmar_pagamento(
        self,
        payment_id: str,
        external_reference: str,
        data_processamento: Optional[datetime] = None,
    ) -> None:
        """Confirma o pagamento"""
        if self.status != StatusPagamento.PENDENTE:
            raise ValueError("Apenas pagamentos pendentes podem ser confirmados")
        
        if not payment_id:
            raise ValueError("Payment ID é obrigatório")
        
        if not external_reference:
            raise ValueError("External reference é obrigatória")
        
        self.status = StatusPagamento.APROVADO
        self.payment_id = payment_id
        self.external_reference = external_reference
        self.data_processamento = data_processamento or datetime.now(UTC)

    def rejeitar_pagamento(
        self,
        motivo: Optional[str] = None,
        data_processamento: Optional[datetime] = None,
    ) -> None:
        """Rejeita o pagamento"""
        if self.status != StatusPagamento.PENDENTE:
            raise ValueError("Apenas pagamentos pendentes podem ser rejeitados")
        
        self.status = StatusPagamento.REJEITADO
        self.data_processamento = data_processamento or datetime.now(UTC)

    def cancelar_pagamento(self) -> None:
        """Cancela o pagamento"""
        if self.status not in [StatusPagamento.PENDENTE, StatusPagamento.APROVADO]:
            raise ValueError("Pagamento não pode ser cancelado no status atual")
        
        self.status = StatusPagamento.CANCELADO
        self.data_processamento = datetime.now(UTC)

    def expirar_pagamento(self) -> None:
        """Expira o pagamento"""
        if self.status != StatusPagamento.PENDENTE:
            raise ValueError("Apenas pagamentos pendentes podem expirar")
        
        self.status = StatusPagamento.EXPIRADO
        self.data_processamento = datetime.now(UTC)

    def esta_aprovado(self) -> bool:
        """Verifica se o pagamento está aprovado"""
        return self.status == StatusPagamento.APROVADO

    def esta_pendente(self) -> bool:
        """Verifica se o pagamento está pendente"""
        return self.status == StatusPagamento.PENDENTE

    def pode_ser_processado(self) -> bool:
        """Verifica se o pagamento pode ser processado"""
        return self.status == StatusPagamento.PENDENTE

    def obter_tempo_expiracao(self) -> Optional[int]:
        """Retorna o tempo de expiração em segundos (se aplicável)"""
        if self.status != StatusPagamento.PENDENTE:
            return None
        
        # 30 minutos de expiração
        tempo_limite = self.data_criacao.replace(tzinfo=UTC) + datetime.timedelta(minutes=30)
        tempo_atual = datetime.now(UTC)
        
        if tempo_atual > tempo_limite:
            return 0
        
        return int((tempo_limite - tempo_atual).total_seconds())

    def _validar_pagamento(self) -> None:
        """Validações internas do pagamento"""
        if self.valor < 0:
            raise ValueError("Valor não pode ser negativo")
        
        if self.valor > 10000:
            raise ValueError("Valor não pode ser maior que R$ 10.000,00")

    def __str__(self) -> str:
        return f"Pagamento {self.id} - Status: {self.status} - Valor: R$ {self.valor:.2f}"

    def __repr__(self) -> str:
        return f"Pagamento(id={self.id}, status={self.status}, valor={self.valor})"