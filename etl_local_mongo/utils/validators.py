from datetime import date, datetime
from typing import Optional

import numpy as np
from dateutil.parser import parse
from pydantic import BaseModel, Field, conlist, validator

DEFAULT_STR = 'default' 
DEFAULT_DATE = '1777-07-07'


class MongoPydantic(BaseModel):
    serverSelectionTimeoutMS: str
    username: str
    password: str
    host: str
    port: str


class RedisPydantic(BaseModel):    
    host: str
    port: str


class TeamPydantic(BaseModel):
    id:int
    name: str
    location: Optional[str]

    class Config:
        validate_assignment = True

    @validator('location')
    def set_str(cls, value):
        return value or DEFAULT_STR


class PlayerPydantic(BaseModel):
    id: int
    name: str
    birthday: Optional[str]
    hometown: Optional[str]
    nationality: Optional[str]    

    class Config:
        validate_assignment = True

    @validator('birthday')
    def set_birthday(cls, value):
        return value or DEFAULT_DATE
    
    @validator('hometown', 'nationality')
    def set_str(cls, value):
        return value or DEFAULT_STR
    


class PlayerFullPydantic(BaseModel):
    adr: Optional[float] 
    assists: Optional[int] 
    deaths: Optional[int] 
    first_kills_diff: Optional[int] 
    flash_assists: Optional[int] 
    game_id: int
    headshots: Optional[int] 
    k_d_diff: Optional[int] 
    kast: Optional[float] 
    kills: Optional[int] 
    rating: Optional[float] 
    player: PlayerPydantic
    opponent: TeamPydantic
    team: TeamPydantic

    class Config:
        validate_assignment = True

    @validator('adr', 'kast', 'rating')
    def set_float(cls, value):
        return value or 0.0
    
    @validator('assists', 'deaths', 'first_kills_diff', 'flash_assists', 'headshots', 'k_d_diff', 'kills')
    def set_int(cls, value):
        return value or 0

class RoundPydantic(BaseModel):
    ct: int
    outcome: str
    round: int
    terrorists: int
    winner_team: int   


class MapPydantic(BaseModel):
    id: int
    name: str    


class LeaguePydantic(BaseModel):
    id: int
    name: str


class SeriePydantic(BaseModel):
    id: int
    name: str = Field(alias="full_name")
    tier: Optional[str]
    
    class Config:
        validate_assignment = True

    @validator('tier')
    def set_tier(cls, tier):
        return tier or 'default'
    

class TournamentPydantic(BaseModel):
    id: int
    name: str    
    prizepool: Optional[str] 

    class Config:
        validate_assignment = True

    @validator('prizepool')
    def set_prizepool(cls, prizepool):
        return prizepool or '0 United States Dollar'


class MatchPydantic(BaseModel):
    league: LeaguePydantic
    serie: SeriePydantic
    tournament: TournamentPydantic


class GamePydantic(BaseModel):
    id: int
    begin_at: str    
    match: MatchPydantic
    map: MapPydantic
    players: list[PlayerFullPydantic]
    rounds: list[RoundPydantic]

    class Config:
        validate_assignment = True

    @validator('players')
    def should_have_valid_players(cls, players):
        all_players = sorted([i.player.id for i in players])
        all_teams = np.unique([i.team.id for i in players])        
        if len(all_teams)!=2:
            raise ValueError("Number of teams should be 2.")
        elif len(all_players) != 10:
            raise ValueError("Number of players should be 10.")
        return players
    
    @validator('rounds')
    def should_have_valid_rounds(cls, rounds):
        all_rounds = sorted([i.round for i in rounds])
        diff = len(np.unique(np.diff(all_rounds)))
        if min(all_rounds)!=1:
            raise ValueError("Minimum round should be 1.")
        elif diff != 1:
            raise ValueError("Some rounds are missing.")
        return rounds


