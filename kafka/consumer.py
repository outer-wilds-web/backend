from aiokafka import AIOKafkaConsumer
import asyncio
import os

# Définition des variables d'environnement
KAFKA_TOPIC_PLANETS = "planet-positions"  # Remplacez si vous l'avez dans un .env
KAFKA_TOPIC_SHIPS = "ship-positions"
KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"  # Remplacez selon votre configuration Kafka


# Fonction asynchrone pour démarrer le consumer Kafka
async def consume():
    # Créez un consumer Kafka
    consumer = AIOKafkaConsumer(
        KAFKA_TOPIC_PLANETS,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id=None  # Pas de group_id si vous voulez consommer indépendamment
    )

    # Démarre le consumer
    await consumer.start()
    try:
        print(f"Consuming messages from topic: {KAFKA_TOPIC_PLANETS}")
        # Consommer les messages en boucle
        async for msg in consumer:
            print(f"Message reçu: {msg.value.decode('utf-8')}")  # Decodez si nécessaire
    finally:
        # Arrêtez le consumer proprement
        await consumer.stop()


# Création de la boucle d'événements asyncio et exécution du consumer
loop = asyncio.get_event_loop()
loop.run_until_complete(consume())
