import asyncio
import logging

from faststream import rabbit as fs
from settings import settings

logger = logging.getLogger('app')


class BaseMessageSenderClient:
    broker: fs.RabbitBroker
    queue: str
    _records: list[str]

    def __init__(self, broker: fs.RabbitBroker, queue: str):
        self.broker = broker
        self._queue = queue
        self._records = []

    async def send(self, data: str):
        logger.info(
            'Sending data. Dump record',
            extra={
                'record': data,
            },
        )
        self._records.append(data)

        if len(self._records) > settings.MQ.SCHEDULER_BATCH_RECORDS_SIZE:
            await self.await_all()

    async def await_all(self):
        if not self._records:
            return

        logger.debug(f'Sending {len(self._records)} {self.__class__.__name__} Record')

        for record in self._records:
            try:
                await self.broker.publish(message=record, queue=self._queue)

            except asyncio.CancelledError as ex:
                raise ex

            except BaseException as ex:
                logger.exception(
                    ex,
                    extra={
                        'data': record,
                    },
                )
                continue
            break

        self._records = []

    async def commit(self):
        await self.await_all()


class ContractSenderClient(BaseMessageSenderClient):
    pass
