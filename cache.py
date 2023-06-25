import time

class cache:

    def __init__(self):
        self.cache = {}

    def add_record(self, hostname, ip_address, ttl):
        expiration_time = time.time() + ttl
        self.cache[hostname] = (ip_address, expiration_time)

    def get_record(self, hostname):
        if hostname in self.cache:
            ip_address, expiration_time = self.cache[hostname]
            if expiration_time > time.time():
                return ip_address
            else:
                del self.cache[hostname]
        return None

    def remove_record(self, hostname):
        if hostname in self.cache:
            del self.cache[hostname]

    def clear_cache(self):
        self.cache = {}