from DNSProxyServer import DNSProxyServer
from ServerConfigLoader import ServerConfigLoader, ServerConfig

if __name__ == '__main__':
    server_config = ServerConfigLoader('ServerConfig.json').load()
    dns_server_ip = server_config.dns_servers_ips[0]
    host_address = server_config.host_listen_address
    host_port = server_config.host_listen_port

    dns_proxy = DNSProxyServer(dns_server_ip, host_address, host_port)
    dns_proxy.start()
