from DNSProxyServer import DNSProxyServer

if __name__ == '__main__':
    DNSserverIP = '185.51.200.2'
    host_address = '127.0.0.1'
    port = 53

    dns_proxy = DNSProxyServer(DNSserverIP, host_address, port)
    dns_proxy.start()
