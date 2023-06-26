import time
import redis
import json
import logging


class Cache:
    def __init__(self, settings_file):
        self.redis = redis.Redis(host='localhost', port=6379, db=0)
        self.load_settings(settings_file)

    def setup_logger(self):
        logger = logging.getLogger('Cache')
        logger.setLevel(logging.DEBUG)

        log_filename = 'cache.log'
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        file_handler = logging.FileHandler(log_filename)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

        return logger

    def load_settings(self, settings_file):
        with open(settings_file, 'r') as file:
            settings = json.load(file)
        self.ttl = settings.get('cache-expiration-time', 3600)
        self.external_dns_servers = settings.get('external-dns-servers', [])

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
