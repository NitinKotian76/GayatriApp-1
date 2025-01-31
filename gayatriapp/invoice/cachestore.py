from pymemcache.client.base import Client

class cachestore():
    def __init__(self):
        self.cache = Client(['localhost:11211'])
        self.ttl = 3600

    def set(self,sesionid,data):
        self.cache.set(sessionid,data,self.ttl)

    def get(self,sessionid):
        self.cache.get(sessionid)

    def delete(self,sessionid):
        self.cache.delete(sessionid)

