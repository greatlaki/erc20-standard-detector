from pydantic import BaseModel


class ContractDataToAnalyze(BaseModel):
    id: int
    source_code: str


class UpdateContractData(BaseModel):
    status: str
    is_erc_20: bool


class UpdateContractStatus(BaseModel):
    status: str
