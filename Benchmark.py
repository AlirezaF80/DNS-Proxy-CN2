import time

from Cache import Cache
from DNSMessageCreator import DNSMessageCreator
from DNSProxyServer import DNSProxyServer
import matplotlib.pyplot as plt
import numpy as np


def benchmark_dns_resolution(dns_proxy: DNSProxyServer, domain_list, num_requests_per_domain):
    num_requests = len(domain_list) * num_requests_per_domain
    dns_server_times = np.zeros(num_requests)
    proxy_times = np.zeros(num_requests)

    query_sizes = np.zeros(num_requests)
    dns_server_sizes = np.zeros(num_requests)
    proxy_sizes = np.zeros(num_requests)

    for i in range(num_requests_per_domain):
        for j in range(len(domain_list)):
            idx = i * len(domain_list) + j

            domain = domain_list[j]
            dns_query = DNSMessageCreator.create_dns_request(domain)
            query_sizes[idx] = len(bytes(dns_query))

            start = time.time()
            dns_server_answer = dns_proxy._answer_query_from_dns(dns_query)
            dns_server_time = time.time() - start
            dns_server_times[idx] = dns_server_time
            dns_server_sizes[idx] = len(bytes(dns_server_answer))

            start = time.time()
            proxy_answer = dns_proxy._answer_query(dns_query)
            proxy_time = time.time() - start
            proxy_times[idx] = proxy_time
            proxy_sizes[idx] = len(bytes(proxy_answer))

            print(f"Domain: {domain}")
            print(f"DNS Server Time: {dns_server_time} seconds")
            print(f"Proxy Time: {proxy_time} seconds")
            print(f"DNS Server Answer Size: {dns_server_sizes[idx]} bytes")
            print(f"Proxy Answer Size: {proxy_sizes[idx]} bytes")
            print("-" * 50)

    print(f"Average DNS Server Time: {np.average(dns_server_times)} seconds")
    print(f"Average Proxy Time: {np.average(proxy_times)} seconds")
    print("-" * 50)
    print(f"Average DNS Server Answer Size: {np.average(dns_server_sizes + query_sizes)} bytes")
    print(f"Average Proxy Answer Size: {np.average(proxy_sizes)} bytes")

    # plot the times
    plt.plot(dns_server_times, label="DNS Server")
    plt.plot(proxy_times, label="Proxy")
    plt.xlabel("Request Number")
    plt.ylabel("Time (s)")
    plt.title("DNS Server vs Proxy Time")
    plt.legend()
    plt.show()

    # plot the sizes
    plt.plot(dns_server_sizes + query_sizes, label="DNS Server")
    plt.plot(proxy_sizes, label="Proxy")
    plt.xlabel("Request Number")
    plt.ylabel("Size (bytes)")
    plt.title("DNS Server vs Proxy Size")
    plt.legend()
    plt.show()


if __name__ == '__main__':
    dns_server_ip = '8.8.8.8'
    proxy_host_address = '127.0.0.1'
    proxy_host_port = 53
    domain_list = open('domain_list.txt').read().splitlines()
    num_requests = 3

    cache = Cache(30, 'localhost', 6379)
    dns_proxy = DNSProxyServer(dns_server_ip, proxy_host_address, proxy_host_port, cache)

    benchmark_dns_resolution(dns_proxy, domain_list, num_requests)
