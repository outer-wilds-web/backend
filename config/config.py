import yaml
import psycopg2
import logging

print("Loading configuration file...")

# Load the configuration file
config = yaml.load(open('config/config.yml', 'r'), Loader=yaml.SafeLoader)

# Configure authification token
SECRET_KEY = config["token"]["secret_key"]
ALGORITHM = config["token"]["algorithm"]
ACCESS_TOKEN_EXPIRE_MINUTES = config["token"]["access_token_expire_minutes"]


# Kafka configuration
KAFKA_BOOTSTRAP_SERVERS = f"{
    config['kafka']['host']}:{config['kafka']['port']}"
KAFKA_TOPIC_PLANETS = config['kafka']['topic']['planets']
KAFKA_TOPIC_SHIPS = config['kafka']['topic']['ships']


# Configure logging
def get_logger():
    logging_level = config.get('logger', {}).get('level', 'INFO').upper()
    logging.basicConfig(
        level=logging_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    return logger


logger = get_logger()


# Connect to the database
def connect_to_db():
    """Connect to the database using configuration from the YAML file.

    Returns:
        tuple: A tuple containing the database connection and cursor, or (None, None) on failure.
    """
    host = config['db']['host']
    port = config['db']['port']
    user = config['db']['user']
    password = config['db']['password']
    dbname = config['db']['name']
    try:
        connection = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            dbname=dbname
        )
        cursor = connection.cursor()
        logger.info("Database connection successful.")
        return connection, cursor
    except Exception as e:
        logger.error(f"Error connecting to the database: {e}")
        return None, None
