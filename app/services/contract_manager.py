from database.engines import engine
from pg.models import Contract, ContractStatus
from schemas.contract import ContractDataToAnalyze, UpdateContractData, UpdateContractStatus
from sqlalchemy import select, update


class ContractManager:

    _table = Contract

    @classmethod
    async def analyze_contracts(cls, limit: int) -> list[ContractDataToAnalyze]:
        async with engine.session() as session:
            query = (
                select(cls._table)
                .where(cls._table.status.in_([ContractStatus.PROCESSING, ContractStatus.FAILED]))
                .limit(limit)
            )
            result = await session.execute(query)
            contracts = result.scalars().all()

        return [ContractDataToAnalyze(id=contract.id, source_code=contract.source_code) for contract in contracts]

    @classmethod
    async def bulk_update_contracts(
        cls,
        contract_ids: list[int],
        to_update: UpdateContractData | UpdateContractStatus,
    ):
        async with engine.session() as session:
            await session.execute(update(cls._table).where(cls._table.id.in_(contract_ids)).values(**to_update))
            await session.commit()
