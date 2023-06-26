import time
import redis
import json
import logging


class Cache:
    def __init__(self, cache_ttl, redis_host, redis_port):
        self.redis = redis.Redis(host=redis_host, port=redis_port, db=0)
        self.ttl = cache_ttl

    def add_record(self, hostname, ip_address):
        self.redis.set(hostname, ip_address, ex=self.ttl)

    def get_record(self, hostname):
        ip_address = self.redis.get(hostname)
        if ip_address:
            return ip_address.decode()
        return None

    def remove_record(self, hostname):
        self.redis.delete(hostname)

    def clear_cache(self):
        self.redis.flushdb()

    def is_record_cached(self, hostname):
        return self.redis.exists(hostname) == 1
