import socket

from Cache import Cache
from DNSMessageParser import *


class DNSProxyServer:
    DNS_SERVER_PORT = 53

    def __init__(self, dns_server_ip, host_address, listen_port, cache: Cache):
        self.dns_server_ip = dns_server_ip
        self.host_address = host_address
        self.listen_port = listen_port
        self.request_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.cache: Cache = cache

    def start(self):
        try:
            self.request_socket.bind((self.host_address, self.listen_port))
            print("UDP DNS proxy server started. Listening on port", self.listen_port)

            while True:
                data, requester_addr = self.request_socket.recvfrom(1024)
                dns_query = DNSMessageParser.parse(data)
                self._handle_request(dns_query, requester_addr)
        except Exception as e:
            print("Error starting DNS proxy server:", e)
        finally:
            self.request_socket.close()

    def _handle_request(self, dns_query: DNSMessage, requester_address):
        try:
            if self.cache.is_record_cached(dns_query):
                print("Record for", dns_query.queries[0].query_name, "found in cache")
                cached_answer = self.cache.get_record(dns_query)
                cached_answer.header.transaction_id = dns_query.header.transaction_id
                dns_response = cached_answer
            else:
                dns_response = self._send_query(dns_query)
                print("Record for", dns_query.queries[0].query_name, "added to cache")
                self.cache.add_record(dns_query, dns_response)
            print(f"Request ({dns_query.queries[0].query_name}) from {requester_address} processed")
            print(dns_response)
            self.request_socket.sendto(bytes(dns_response), requester_address)
        except Exception as e:
            print("Error processing DNS request:", e)
        finally:
            print("\n")

    def _send_query(self, dns_query: DNSMessage):
        query_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        query_socket.sendto(bytes(dns_query), (self.dns_server_ip, self.DNS_SERVER_PORT))
        dns_answer, _ = query_socket.recvfrom(1024)
        query_socket.close()
        return DNSMessageParser.parse(dns_answer)
