import json
import os
import time
from pathlib import Path
from pprint import pprint

import config
import numpy as np
import pandas as pd
import pydantic
from dotenv import load_dotenv
from pymongo import MongoClient, errors
from pymongo.collection import Collection
from utils.connections import get_mongo_client, get_redis_client
from utils.logger import logger
from utils.state import State
from utils.validators import (GamePydantic, LeaguePydantic, MongoPydantic,
                              PlayerFullPydantic, PlayerPydantic,
                              RedisPydantic, RoundPydantic, SeriePydantic,
                              TeamPydantic, TournamentPydantic)


def get_mongo_collection(mongo_client: MongoClient, collection: str) -> Collection:
    '''Get mongo collection.'''
    mydb = mongo_client[config.MONGO_INITDB_DATABASE]
    mycol = mydb[collection]
    return mycol


def get_new_games(state: State, DIRNAME: str) -> list:
    '''Get new games.'''
    try:
        s_success = set([i.decode('ascii') for i in state.get('mongo_success')])
    except Exception:
        s_success = set()
    try:
        s_error = set([i.decode('ascii') for i in state.get('mongo_error')])
    except Exception:
        s_error = set()
    s_all = set([g.split('.')[0] for g in os.listdir(DIRNAME)])
    return list(s_all - s_success - s_error)


def get_chunks(new_games: list, CHUNK_SIZE: int) -> list[list]:
    '''Get chunks of games.'''
    return np.array_split(new_games, np.int32(np.ceil(len(new_games) / CHUNK_SIZE)))


def validate_game(game_id: int, state: State) -> tuple[bool, dict]:
    '''Validate input game.'''
    pth = os.path.join(config.DIRNAME, f'{game_id}.json')
    try:
        with open(pth, 'r') as f:
            game = json.load(f)
    except Exception as exc:
        state.add('mongo_error', game_id)
        logger.error(f'GAME: {game_id}. {exc}')
        return False, {'id': game_id}
    try:
        d_game = GamePydantic(**game).dict()
        state.add('mongo_success', game_id)
        logger.info(f'GAME: {game_id}. SUCCESS')
        return True, d_game
    except pydantic.ValidationError as exc:
        state.add('mongo_error', game_id)
        logger.error(f'GAME: {game_id}. {exc}')
        return False, game


# size of insertion
CHUNK_SIZE = config.CHUNK_SIZE


def main():

    # root
    BASE_DIR = Path(__file__).resolve().parent.parent
    # path to environment variables
    PATH_TO_ENV = BASE_DIR / '.env'
    # load environment variables
    load_dotenv(PATH_TO_ENV)

    # set connections
    mongo_client = get_mongo_client(MongoPydantic)
    redis_client = get_redis_client(RedisPydantic)
    state = State(redis_client)
    new_games = get_new_games(state, config.DIRNAME)
    col_success = get_mongo_collection(mongo_client, config.MONGO_COLLECTION_SUCCESS)
    col_error = get_mongo_collection(mongo_client, config.MONGO_COLLECTION_ERROR)

    # no new games
    if len(new_games) == 0:
        logger.info('There is no new games')
        return False
    # new games
    else:
        logger.info(f'There is {len(new_games)} new games')   
        # split games into chunks for bulk insert      
        chuncks = get_chunks(new_games, CHUNK_SIZE)
        for chunk in chuncks:
            # valid and invalid games  
            L_success, L_error = [], []
            for game_id in chunk:
                is_success, d_game = validate_game(game_id, state)
                if is_success:
                    L_success.append(d_game)
                else:
                    L_error.append(d_game)
            # insert collections into Mongo
            if len(L_success) != 0:
                col_success.insert_many(L_success)
            if len(L_error) != 0:
                col_error.insert_many(L_error)
            del L_success, L_error

        return True

if __name__ =='__main__':

    while True:
        main()
        logger.info('FINISHED ...')
        time.sleep(config.SLEEP)
