import redis


class Storage():

    def __init__(self, host, port, db):
        self.connection = redis.StrictRedis(host, port, db, charset="utf-8", decode_responses=True)