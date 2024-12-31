import asyncio
import logging
from datetime import datetime
from aiokafka import AIOKafkaConsumer
from contextlib import asynccontextmanager
from config.config import KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC_PLANETS, KAFKA_TOPIC_SHIPS
from pydantic import ValidationError
from config.config import get_logger

from api.services import planet_service, ship_service, position_service

from api.models.Message import Message
from api.models.Position import Position

logger = get_logger()


@asynccontextmanager
async def kafka_lifespan(app):
    """Lifespan context manager for Kafka consumer lifecycle.

    This context manager initializes a Kafka consumer, starts it, and ensures
    proper cleanup of resources when exiting the context.

    Args:
        app: The FastAPI application instance (not used in this example).

    Yields:
        None: The context does not pass any specific object.
    """
    consumer = AIOKafkaConsumer(
        *[KAFKA_TOPIC_PLANETS, KAFKA_TOPIC_SHIPS],
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id=None
    )
    await consumer.start()
    logger.info(f"Kafka consumer started for topics: {KAFKA_TOPIC_PLANETS}, {KAFKA_TOPIC_SHIPS}")

    # Create a task to consume messages
    consumer_task = asyncio.create_task(consume_messages(consumer))

    try:
        yield
    finally:
        # Cancel the consumer task and ensure proper cleanup
        consumer_task.cancel()
        try:
            await asyncio.shield(consumer_task)
        except asyncio.CancelledError:
            logger.info("Consumer task cancelled.")
        await consumer.stop()
        logger.info("Kafka consumer stopped.")


async def consume_messages(consumer):
    """Consume messages from Kafka topics asynchronously.

    This function processes messages received from Kafka topics and performs
    necessary operations, including data validation and service calls.

    Args:
        consumer: An instance of AIOKafkaConsumer initialized with topics to consume.

    Raises:
        asyncio.CancelledError: When the task is cancelled, this exception is propagated.
    """
    try:
        async for msg in consumer:
            try:
                # Decode the message
                message_value = msg.value.decode('utf-8')

                # Validate and parse the message using a Pydantic model
                message: Message = Message.model_validate_json(message_value)

                id = None
                if message.type_object == "planet":
                    # Retrieve or create a planet by its name
                    planet = planet_service.get_planet_by_name(message.name)
                    if not planet:
                        planet = planet_service.create(message.name)
                    id = planet.id

                elif message.type_object == "ship":
                    # Retrieve a ship by its name, raising an error if not found
                    ship = ship_service.get_ship_by_name(message.name)
                    if not ship:
                        logger.error(f"Ship not found for name: {message.name}")
                        raise ValueError(f"Ship not found: {message.name}")
                    id = ship.id

                if id:
                    # Convert the timestamp to a datetime object and create a position
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

            except ValidationError as ve:
                # Log validation errors for invalid messages
                logger.error(f"Validation error for message: {msg.value}, error: {ve}")
            except ValueError as ve:
                # Log value errors for missing or invalid entities
                logger.error(f"Value error: {ve}")
            except Exception as e:
                # Log unexpected errors during message processing
                logger.exception(f"Unexpected error processing message: {msg.value}, error: {e}")

    except asyncio.CancelledError:
        # Log when the task is cancelled
        logger.info("Message consumption cancelled.")
        raise
