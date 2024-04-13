import json
from pydantic import BaseModel
import os

class PostgresDB(BaseModel):
    dbname: str
    user: str
    password: str
    host: str
    port: str

class RedisDB(BaseModel):
    host: str
    port: int
    ttl: int

class Config(BaseModel):
    bot_token: str
    psql: PostgresDB
    redis: RedisDB

def load_config() -> Config:
    with open(f'{os.path.abspath(os.curdir)}/bot/config/config.json', 'r') as config_json:
        config_json = json.load(config_json)
        config = Config(**config_json)
        return config