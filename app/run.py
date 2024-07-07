import asyncio
import logging

from faststream import FastStream
from faststream.rabbit import RabbitBroker
from pydantic import json
from services.messages_sender import ContractSenderClient
from settings import settings

from app.services.contract_detecor import ContractAnalyzeService
from app.services.contract_manager import ContractManager
from app.services.scheduler import run_scheduler

broker: RabbitBroker = RabbitBroker(settings.MQ.BROKER_URL)
app: FastStream = FastStream(broker)
contract_client: ContractSenderClient = ContractSenderClient(broker, settings.MQ.CONTRACTS_QUEUE)

contract_manager = ContractManager()
contract_service = ContractAnalyzeService(contract_manager)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('app')


@broker.subscriber(settings.MQ.CONTRACTS_QUEUE)
async def agent_executor(message):
    contracts_data = json.loads(message.body.decode('utf-8'))
    await contract_service.analyze_contracts(contracts_data)


async def main():
    logger.info('starting broker')
    await broker.start()

    logger.info('running scheduler')
    await run_scheduler(contract_client, contract_manager, contract_service)


if __name__ == "__main__":
    asyncio.run(main())
