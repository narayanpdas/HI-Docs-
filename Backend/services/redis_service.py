import redis
from sqlalchemy.ext.asyncio import AsyncSession
from models.guys import Guys
from sqlalchemy import select

class RedisManager():
    def __init__(self):
        self.redis_server = redis.Redis(decode_responses=True)
        self.setname_task = "processing_tasks"
        self.setname_freetiercount = "freetier:"
        self.setname_requestcount = "request:"
        self.setname_creditcount = "credits:"
        try:
            self.redis_server.ping()
            print(f"\n Connecting to Redis Server: \n Details:\n {self.redis_server.__repr__()}\n")
        except redis.exceptions.ConnectionError:
            print("Redis Error : Could Not Connect to Server.")
        self.intialize_server()
    
    def intialize_server(self,db:AsyncSession=None):
        self.redis_server.sadd(self.setname_task,"default")
    
    # Set Values , Values under the name of a particular set.
    def check_set(self,set_name:str,
                  user_id:str):
        return self.redis_server.sismember(name=set_name,
                                           value=user_id)
    
    def add_set(self,set_name:str,
                user_id:str):
        self.redis_server.sadd(set_name,user_id)

    def remove_set(self,set_name:str,
                   user_id:str):
        self.redis_server.srem(set_name,user_id)

    # Direct Key-Value, Objects. Use Prefix for better segregation.
    def add(self,key,
            value,
            prefix="",ex=None):
        self.redis_server.set(name=prefix+key,
                              value=value,
                              ex=ex)
    
    def delete(self,key,
               prefix=""):
        self.redis_server.delete(prefix+key)
    
    def get(self,key,
            prefix=""):
        return self.redis_server.get(prefix+key)
    
    def decr(self,key,
             prefix="",
             amnt=1):
        return self.redis_server.decr(name=prefix+key,
                               amount=amnt)

    def incr(self,key,
             prefix="",
             amnt=1):
        return self.redis_server.incr(name=prefix+key,
                               amount=amnt)
    
    # Actual Utility Functions Used in the Application.

    def add_task(self,user_id:str):
        setname = self.setname_task
        self.add_set(set_name=setname,user_id=user_id)
    
    def delete_task(self,user_id:str):
        setname = self.setname_task
        self.remove_set(set_name=setname,user_id=user_id)

    def check_task(self,user_id:str)->bool:
        setname = self.setname_task
        return self.check_set(set_name=setname,user_id=user_id)

    def check_request_count(self,user_id:str):
        setname = self.setname_requestcount
        return self.get(key=user_id,prefix=setname)

    def reset_credits(self,user_id:str,amnt:int):
        setname = self.setname_creditcount
        self.incr(prefix=setname,key=user_id,amount=amnt)

    def decr_credits(self,user_id:str,amnt:int):
        setname = self.setname_creditcount
        self.decr(prefix=setname,key=user_id,amnt=amnt)

    def check_credits(self,user_id:str):
        setname = self.setname_creditcount
        return self.get(key=user_id,prefix=setname)

    async def sync_credits_to_db(self,
                                user_id:str,
                                db:AsyncSession):
        
        current_credits = self.check_credits(user_id=user_id)
        guy = await db.scalar(select(Guys).where(Guys.id==user_id))
        guy.free_credits = current_credits
        db.commit()
        db.close()

