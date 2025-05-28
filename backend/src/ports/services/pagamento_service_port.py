from abc import ABC, abstractmethod

from src.adapters.input.dto.pagamento_dto import PagamentoQRCodeResponse


class PagamentoServicePort(ABC):
    @abstractmethod
    def gerar_qrcode(self) -> PagamentoQRCodeResponse:
        pass
