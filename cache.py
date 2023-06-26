import time
import redis


class Cache:
    def __init__(self, ttl):
        self.redis = redis.Redis(host='localhost', port=6379, db=0)
        self.ttl = ttl

    def add_record(self, hostname, ip_address):
        expiration_time = int(time.time()) + self.ttl
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
        return self.redis.exists(hostname)


# Example usage
cache = Cache(ttl=3600)  # TTL of 1 hour

# Add a record to the cache
cache.add_record('example.com', '192.168.1.100')

# Check if a record is already cached
is_cached = cache.is_record_cached('example.com')
print(is_cached)  # Output: True

# Check if a non-existing record is cached
is_cached = cache.is_record_cached('example.org')
print(is_cached)  # Output: False
