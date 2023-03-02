import backoff
import config
import pydantic
import redis
from pymongo import MongoClient, errors
from utils.logger import logger
from utils.validators import MongoPydantic, RedisPydantic


@backoff.on_exception(backoff.expo, errors.ServerSelectionTimeoutError, max_tries=5)
def get_mongo_client(MongoPydantic: pydantic.BaseModel) -> MongoClient:
    '''Get mongo params.'''
    d = {
        'serverSelectionTimeoutMS': config.MONGO_TIMEOUT,
        'username': config.MONGO_INITDB_ROOT_USERNAME,
        'password': config.MONGO_INITDB_ROOT_PASSWORD,        
        'host': config.MONGO_HOST_DOCKER,
        'port': config.MONGO_PORT,
    }
    d = MongoPydantic(**d).dict()
    try:
        return MongoClient(
            host=[d['host'] + ":" + d['port']],
            serverSelectionTimeoutMS=d['serverSelectionTimeoutMS'],
            username=d['username'],
            password=d['password'],
        )
    except errors.ServerSelectionTimeoutError as err:
        logger.error(err)


@backoff.on_exception(backoff.expo, redis.ConnectionError, max_tries=5)
def get_redis_client(RedisPydantic: pydantic.BaseModel) -> redis.Redis.client:
    '''Get redis instance.'''
    d = {'host': config.REDIS_HOST_DOCKER, 'port': config.REDIS_PORT}
    d = RedisPydantic(**d).dict()
    pool = redis.ConnectionPool(**d)
    try:        
        return redis.Redis(connection_pool=pool)
    except redis.ConnectionError as error:
        logger.error(error)