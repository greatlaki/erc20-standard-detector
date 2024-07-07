from enum import StrEnum

from pg.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_utils import ChoiceType


class ContractStatus(StrEnum):
    WAITS_PROCESSING = "WAITS_PROCESSING"
    PROCESSING = "PROCESSING"
    PROCESSED = "PROCESSED"
    FAILED = "FAILED"


class Contract(Base):

    __tablename__ = "contracts"

    contract_address: Mapped[str] = mapped_column(unique=True)
    source_code: Mapped[str] = mapped_column()
    is_erc_20: Mapped[bool] = mapped_column(server_default="f")
    erc20_version: Mapped[str] = mapped_column(server_default="")
    status: Mapped[str] = mapped_column(ChoiceType(ContractStatus), default=ContractStatus.WAITS_PROCESSING)
