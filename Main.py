from Cache import Cache
from DNSProxyServer import DNSProxyServer
from ServerConfigLoader import ServerConfigLoader

if __name__ == '__main__':
    server_config = ServerConfigLoader('ServerConfig.json').load()

    cache_ttl = server_config.cache_ttl
    redis_host = server_config.redis_host
    redis_port = server_config.redis_port
    cache = Cache(cache_ttl, redis_host, redis_port)

    dns_server_ip = server_config.dns_servers_ips[0]
    host_address = server_config.host_listen_address
    host_port = server_config.host_listen_port
    dns_proxy = DNSProxyServer(dns_server_ip, host_address, host_port, cache)
    dns_proxy.start()
