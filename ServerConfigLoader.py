import json


class ServerConfig:
    def __init__(self, dns_servers_ips, host_listen_address, host_listen_port, cache_ttl, redis_host, redis_port):
        self.dns_servers_ips = dns_servers_ips
        self.host_listen_address = host_listen_address
        self.host_listen_port = host_listen_port
        self.cache_ttl = cache_ttl
        self.redis_host = redis_host
        self.redis_port = redis_port


class ServerConfigLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def load(self, default_ttl=3600, default_host_address='127.0.0.1', default_host_port=53,
             default_redis_host='localhost', default_redis_port=6379):
        with open(self.file_path, 'r') as file:
            settings = json.load(file)
        dns_servers_ips = settings.get('external-dns-servers', [])
        host_address = settings.get('host-address', default_host_address)
        host_listen_port = settings.get('host-port', default_host_port)
        cache_ttl = settings.get('cache-expiration-time', default_ttl)
        redis_host = settings.get('redis-host', default_redis_host)
        redis_port = settings.get('redis-port', default_redis_port)
        return ServerConfig(dns_servers_ips, host_address, host_listen_port, cache_ttl, redis_host, redis_port)
