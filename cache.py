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


# Example usage
cache = Cache(ttl=3600)  # TTL of 1 hour

# Add a record to the cache
cache.add_record('example.com', '192.168.1.100')

# Get a record from the cache
ip = cache.get_record('example.com')
print(ip)  # Output: 192.168.1.100

# Remove a record from the cache
cache.remove_record('example.com')

# Clear the entire cache
cache.clear_cache()
