import redis, json
from redis.asyncio import ConnectionPool
from redis.commands.json.path import Path
from fastapi import Request, HTTPException
from redis.exceptions import ConnectionError
from config.connections.databases.redis.index import ConnectorRedis
from datetime import timedelta, datetime


class ServiceRedis:
    def __init__(self):
        self.connector = ConnectorRedis(conn=None)

    def get_connection_health(self):
        return self.connector.getterConnector().ping()

    async def setData(self, data):
        print(data)

    async def getData(self, data):
        return redis.exists(data)

    async def deleteData(self, data):
        pass

    async def getToken(self, key):
        result = self.connector.getterConnector().get(name=key)
        if(result):
            return json.loads(result)
        else:
            return None

    async def storeToken(self, key, value):
        # print(key, value)
        return self.connector.getterConnector().set(
            name=key, value=json.dumps(value), ex=30
        )
