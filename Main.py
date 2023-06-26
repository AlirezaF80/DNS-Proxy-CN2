from DNSProxyServer import DNSProxyServer

if __name__ == '__main__':
    dns_server_ip = '185.51.200.2'  # Shecan DNS server
    server_host_address = '127.0.0.1'
    server_port = 53

    dns_proxy = DNSProxyServer(dns_server_ip, server_host_address, server_port)
    dns_proxy.start()
