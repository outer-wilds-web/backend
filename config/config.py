import yaml
import psycopg2

print("Chargement du fichier de configuration...")
# A ajouter au fichier de config


# Charger le fichier de configuration
config = yaml.load(open('config/config.yml', 'r'), Loader=yaml.SafeLoader)

# config kafka
KAFKA_BOOTSTRAP_SERVERS = config['kafka']['host'] + \
    ":" + str(config['kafka']['port'])
KAFKA_TOPIC_PLANETS = config['kafka']['topic']['planets']
KAFKA_TOPIC_SHIPS = config['kafka']['topic']['ships']

# Se connecter à la base de données


def connect_to_db():
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
        print("Connexion à la base de données réussie")
        return connection, cursor
    except Exception as e:
        print(f"Erreur lors de la connexion à la base de données: {e}")
        return None, None
