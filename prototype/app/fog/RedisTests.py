import redis


def main():
    rdb = redis.StrictRedis('localhost', 6379, 0, charset="utf-8", decode_responses=True)
    