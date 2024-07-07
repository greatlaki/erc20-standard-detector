import asyncio
import logging

from faststream import FastStream
from faststream.rabbit import RabbitBroker
from pydantic import json
from services.contract_detecor import ContractAnalyzeService
from services.contract_manager import ContractManager
from services.scheduler import run_scheduler

from settings import settings

broker: RabbitBroker = RabbitBroker(settings.BROKER_URL)
app: FastStream = FastStream(broker)

contract_manager = ContractManager()
contract_service = ContractAnalyzeService(contract_manager)

logger = logging.getLogger('app')


@broker.subscriber(settings.CONTRACTS_QUEUE)
async def agent_executor(message):
    contracts_data = json.loads(message.body.decode('utf-8'))
    await contract_service.analyze_contracts(contracts_data)


async def main():
    logger.info('run scheduler')
    await run_scheduler()


if __name__ == "__main__":
    asyncio.run(main())
