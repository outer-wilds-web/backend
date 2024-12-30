from aiokafka import AIOKafkaConsumer
import asyncio
from contextlib import asynccontextmanager
from config.config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC_PLANETS
from datetime import datetime

from api.services import planet_service, position_service

from api.models.Message import Message
from api.models.Position import Position


@asynccontextmanager
async def kafka_lifespan(app):
    """
    Lifespan context manager for Kafka consumer lifecycle.
    """
    consumer = AIOKafkaConsumer(
        KAFKA_TOPIC_PLANETS,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id=None
    )
    await consumer.start()
    print(f"Kafka consumer started for topic: {KAFKA_TOPIC_PLANETS}")

    consumer_task = asyncio.create_task(consume_messages(consumer))

    try:
        yield
    finally:
        consumer_task.cancel()
        try:
            await consumer_task
        except asyncio.CancelledError:
            print("Consumer task cancelled.")
        await consumer.stop()
        print("Kafka consumer stopped.")


async def consume_messages(consumer):
    """
    Asynchronous function to consume messages from Kafka.
    """
    try:
        async for msg in consumer:

            # Décoder le message
            message_value = msg.value.decode('utf-8')

            # Convertir en instance de modèle Pydantic
            message: Message = Message.model_validate_json(message_value)
            id = None
            if message.type_object == "planet":
                planet = planet_service.get_planet_by_name(message.name)
                if not planet:
                    planet = planet_service.create(message.name)
                id = planet.id

            if message.type_object == "ship":
                pass
            if id:
                position_time = datetime.fromtimestamp(
                    message.timestamp / 1000.0)
                position = Position(
                    id=id,
                    x=message.x,
                    y=message.y,
                    z=message.z,
                    time=position_time
                )
                position_service.add_position(position)

    except asyncio.CancelledError:
        print("Message consumption cancelled.")
        raise
