import redis
from redis.asyncio import ConnectionPool

class ConnectorRedis:
    def __init__(self, conn):
        self.conn = redis.Redis(host="localhost", port=6379, decode_responses=True, encoding="utf-8")
    
    def getterConnector(self):
        return self.conn