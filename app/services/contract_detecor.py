import json
import logging
from typing import Any

from core.constants import REGEX_PATTERN
from pg.models import ContractStatus
from schemas.contract import ContractDataToAnalyze, UpdateContractData
from services.contract_manager import ContractManager

logger = logging.getLogger('app')


class ContractAnalyzeService:

    def __init__(self, contract_storage: ContractManager) -> None:
        self._contract_manager = contract_storage

    async def get_contracts(self, limit: int) -> tuple[list[ContractDataToAnalyze], list[int]]:
        contracts = await self._contract_manager.analyze_contracts(limit)
        contract_ids = [contract.id for contract in contracts]
        return contracts, contract_ids

    async def receive_contracts(self, message: Any) -> None:
        try:
            contracts_data = json.loads(message.body.decode('utf-8'))
            await self.analyze_contracts(contracts_data)
            await message.ack()
        except json.JSONDecodeError as ex:
            logging.error(f"JSON decoding error handling message: {ex}")
        except Exception as ex:
            logging.error(f"Error handling message: {ex}")

    async def analyze_contracts(self, contracts_data: list[dict[str, Any]]) -> None:
        logging.info('Analyzing contracts')
        erc20_contracts, non_erc20_contracts = self.classify_contracts(contracts_data)

        if erc20_contracts:
            logging.info(f"Updating {len(erc20_contracts)} contracts as ERC20.")
            await self._contract_manager.bulk_update_contracts(
                erc20_contracts, UpdateContractData(status=ContractStatus.PROCESSED, is_erc_20=True)
            )

        if non_erc20_contracts:
            logging.info(f"Updating {len(non_erc20_contracts)} contracts as non-ERC20.")
            await self._contract_manager.bulk_update_contracts(
                non_erc20_contracts, UpdateContractData(status=ContractStatus.PROCESSED, is_erc_20=False)
            )

    @staticmethod
    def find_allowed_imports(source_code: str) -> list[str]:
        lines = source_code.split('\n')
        non_comment_lines = [line for line in lines if not line.strip().startswith("//")]
        return [line for line in non_comment_lines if REGEX_PATTERN.search(line)]

    def classify_contracts(self, contracts_data: list[dict[str, Any]]) -> tuple[list[int], list[int]]:
        erc20_contracts = []
        non_erc20_contracts = []

        for contract in contracts_data:
            source_code = contract['source_code']
            matches = self.find_allowed_imports(source_code)
            if matches:
                erc20_contracts.append(contract['id'])
            else:
                non_erc20_contracts.append(contract['id'])

        return erc20_contracts, non_erc20_contracts
