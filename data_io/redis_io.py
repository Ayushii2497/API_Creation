import redis
import json 

TTL = 10000

class Redis_IO:
    def __init__(self):
        self.r_client = redis.Redis(host='localhost', port=6379, db=0)

    def insert_info(self, channel_name, data):
        self.r_client.psetex(channel_name, TTL ,json.dumps(data))

    def get_info(self,channel_name):
        resp_info = self.r_client.get(channel_name)
        if resp_info:
            return json.loads(resp_info)
        else:
            return None