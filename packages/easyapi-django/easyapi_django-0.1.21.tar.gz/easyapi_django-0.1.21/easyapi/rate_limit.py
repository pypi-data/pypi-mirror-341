import os
import time
from redis import StrictRedis

REDIS_DB = os.environ['REDIS_DB']
REDIS_SERVER = os.environ['REDIS_SERVER']
REDIS_PREFIX = os.environ.get('REDIS_PREFIX', '')


class RateLimit(StrictRedis):
    def __init__(self):
        super().__init__(host=REDIS_SERVER, db=REDIS_DB)

    def current_milli_time(self):
        return int(round(time.time() * 1000))

    def check_limits(self, identifier, limits, limit_type=None):
        now = self.current_milli_time()
        type_to_check = limit_type if limit_type else "api"
        key = f"{REDIS_PREFIX}:limits:{type_to_check}:{identifier}"
        abuse_key = f"{REDIS_PREFIX}:limits:abuse:{identifier}"

        limit = limits.get(type_to_check, limits["api"])
        limit_abuse = limits["abuse"]

        # Pipeline para operações do tipo específico e abuso
        p = self.pipeline()

        # Operações para o tipo específico
        p.zremrangebyscore(key, 0, now - limit["interval"])
        p.zcard(key)  # Conta antes de adicionar
        p.zadd(key, {f"req_{now}": now})
        p.expire(key, int(limit["interval"] / 1000) + 1)  # TTL em segundos

        # Operações para abuso
        p.zremrangebyscore(abuse_key, 0, now - limit_abuse["interval"])
        p.zcard(abuse_key)  # Conta antes de adicionar
        p.zadd(abuse_key, {f"req_{now}": now})
        p.expire(abuse_key, int(limit_abuse["interval"] / 1000) + 1)  # TTL em segundos

        pipeline_results = p.execute()

        # Resultados para o tipo específico
        count_type = pipeline_results[1]  # ZCARD antes de adicionar
        is_rate_limited = count_type >= limit["limit"]

        # Resultados para abuso
        count_abuse = pipeline_results[5]  # ZCARD antes de adicionar
        is_abuse = count_abuse >= limit_abuse["limit"]

        return {
            "rate_limited": is_rate_limited,
            "abuse": is_abuse
        }

    def api_limited(self, identifier, limits):
        return self.check_limits(identifier, limits, "api")

    def login_limited(self, identifier, limits):
        return self.check_limits(identifier, limits, "login")


RateLimiter = RateLimit()
