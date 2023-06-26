import time
import redis

class Cache:
    def __init__(self, ttl):
        self.redis = redis.Redis(host='localhost', port=6379, db=0)
        self.ttl = ttl

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
        return self.redis.exists(hostname)

# Example usage
cache = Cache(ttl=5)  # TTL of 5 seconds

# Add a record to the cache
cache.add_record('example.com', '192.168.1.100')

# Check if the record is cached immediately after adding
is_cached = cache.is_record_cached('example.com')
print(is_cached)  # Output: True

# Retrieve the record immediately after adding
ip = cache.get_record('example.com')
print(ip)  # Output: 192.168.1.100

# Wait for the TTL to expire
time.sleep(6)

# Check if the record is still cached after the TTL has expired
is_cached = cache.is_record_cached('example.com')
print(is_cached)  # Output: False

# Retrieve the record after the TTL has expired
ip = cache.get_record('example.com')
print(ip)  # Output: None
