from faststream.rabbit import RabbitBroker
from pydantic import AmqpDsn

from src.schemas import DataSchema, DataRow
from src.rabbitmq import exch, queue_create_data_schema, queue_save_row


class RabbitmqPersistence:
    def __init__(self, rabbitmq_dsn: AmqpDsn):
        self.broker = RabbitBroker(
            str(rabbitmq_dsn)
        )

    async def create_data_schema(self, data_schema: DataSchema):
        async with self.broker:
            await self.broker.publish(
                data_schema,
                queue_create_data_schema,
                exch,
            )

    async def save(self, rows: list[DataRow]) -> None:
        async with self.broker:
            for row in rows:
                await self.broker.publish(
                    row,
                    queue_save_row,
                    exch,
                )
