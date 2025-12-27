import redis
from sqlalchemy.ext.asyncio import AsyncSession


class RedisServer():
    def __init__(self):
        self.redis_server = redis.Redis()
        print("\n Connecting to Redis Server: \n",self.redis_server.__repr__(),"\n")
    def intialize_server(self,
                         db:AsyncSession):
        pass
    def add(self,key,value,ex=None):
        self.redis_server.set(name=key,
                              value=value,
                              ex=ex)
    def delete(self,key):
        self.redis_server.delete(key)
    def get(self,key):
        return self.redis_server.get(key)
    def incr(self,key):
        self.redis_server.incr(name=key,amount=1)


