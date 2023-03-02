import os
from pathlib import Path

from dotenv import load_dotenv

# root
BASE_DIR = Path(__file__).resolve().parent.parent
# path to environment variables
PATH_TO_ENV = BASE_DIR / '.env.dev'
# load environment variables
load_dotenv(PATH_TO_ENV)


MONGO_TIMEOUT = int(os.getenv('MONGO_TIMEOUT'))
MONGO_INITDB_ROOT_USERNAME = os.getenv('MONGO_INITDB_ROOT_USERNAME')
MONGO_INITDB_ROOT_PASSWORD = os.getenv('MONGO_INITDB_ROOT_PASSWORD')
MONGO_INITDB_DATABASE = os.getenv('MONGO_INITDB_DATABASE')
MONGO_COLLECTION_SUCCESS = os.getenv('MONGO_COLLECTION_SUCCESS')
MONGO_COLLECTION_ERROR=os.getenv('MONGO_COLLECTION_ERROR')
MONGO_HOST_DOCKER = os.getenv('MONGO_HOST_DOCKER')
MONGO_PORT = os.getenv('MONGO_PORT')

REDIS_HOST_DOCKER = os.getenv('REDIS_HOST_DOCKER')
REDIS_PORT = os.getenv('REDIS_PORT')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')    

DIRNAME = os.getenv('DIRNAME')
SLEEP = float(os.getenv('SLEEP'))
CHUNK_SIZE = int(os.getenv('CHUNK_SIZE'))
