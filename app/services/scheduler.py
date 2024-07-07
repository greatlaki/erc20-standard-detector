import asyncio
import json
import logging

from pg.models import ContractStatus
from schemas.contract import UpdateContractStatus
from services.messages_sender import BaseMessageSenderClient
from settings import settings

logger = logging.getLogger('app')


async def run_scheduler(sender_client: BaseMessageSenderClient, manager, service):
    while True:
        try:
            contracts, contract_ids = await service.get_contracts(settings.ROWS_LIMIT)
            if contracts:
                message = json.dumps([contract.dict() for contract in contracts])
                await sender_client.send(message)
                await manager.bulk_update_contract(
                    contract_ids, UpdateContractStatus(status=ContractStatus.WAITS_PROCESSING)
                )
            else:
                logging.info("No contracts to publish.")
                await asyncio.sleep(100)
        except Exception as ex:
            logging.error(f"Publisher Error: {ex}")
            raise ex
