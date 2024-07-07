import json
import logging

from pg.models import ContractStatus
from schemas.contract import UpdateContractStatus

from run import broker, contract_manager, contract_service
from settings import settings

logger = logging.getLogger('app')


async def run_scheduler():
    while True:
        try:
            contracts, contract_ids = await contract_service.get_contracts(settings.ROWS_LIMIT)
            if contracts:
                message = json.dumps([contract.dict() for contract in contracts])
                await broker.publish(message, settings.CONTRACTS_QUEUE)
                await contract_manager.bulk_update_contract(
                    contract_ids, UpdateContractStatus(status=ContractStatus.WAITS_PROCESSING)
                )
            else:
                logging.info("No contracts to publish.")
        except Exception as ex:
            logging.error(f"Publisher Error: {ex}")
            raise ex
