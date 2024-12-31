import os
import yaml
import psycopg2
import logging

print("Loading configuration file...")

# Load the configuration file with environment variable resolution


def load_config_with_env(file_path):
    with open(file_path, 'r') as file:
        raw_config = yaml.load(file, Loader=yaml.SafeLoader)

    # Resolve environment variables in the config
    def resolve_env(value):
        if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
            env_var = value[2:-1]
            return os.getenv(env_var.split(':-')[0], env_var.split(':-')[1])
        return value

    def traverse(obj):
        if isinstance(obj, dict):
            return {key: traverse(resolve_env(value)) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [traverse(resolve_env(item)) for item in obj]
        else:
            return resolve_env(obj)

    return traverse(raw_config)

# Load configuration


def load_config():
    config_path = 'config/config.yml'
    return load_config_with_env(config_path)


config = load_config()

# Configure authentication token
SECRET_KEY = config["token"]["secret_key"]
ALGORITHM = config["token"]["algorithm"]
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    config["token"]["access_token_expire_minutes"])

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
    port = int(config['db']['port'])
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
