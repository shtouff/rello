import os

from redis.asyncio import ConnectionPool, Redis


# from .info import info_data


def create_redis_pool():
    host = os.environ.get("RELLO_REDIS_HOST", "127.0.0.1")
    port = int(os.environ.get("RELLO_REDIS_PORT", "6379"))
    db = int(os.environ.get("RELLO_REDIS_DB", 0))
    return ConnectionPool.from_url(f"redis://{host}:{port}", db=db)


redis_pool = create_redis_pool()


class PooledRedis(Redis):
    """
    This can be used as a Dependency, providing a new Redis connection, but always taken from the same pool, thus
    avoiding reaching the 'too many connections' error.
    """

    def __init__(self):
        super().__init__(connection_pool=redis_pool)
