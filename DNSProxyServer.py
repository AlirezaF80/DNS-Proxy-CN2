import socket
from threading import Thread

from Cache import Cache
from DNSMessage import DNSMessage
from DNSMessageParser import DNSMessageParser


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
            self._bind_socket()
            self._listen_for_requests()
        except Exception as e:
            print("Error starting DNS proxy server:", e)
        finally:
            self.request_socket.close()

    def _bind_socket(self):
        self.request_socket.bind((self.host_address, self.listen_port))
        print("UDP DNS proxy server started. Listening on port", self.listen_port)

    def _listen_for_requests(self):
        while True:
            data, requester_addr = self.request_socket.recvfrom(1024)
            dns_query = DNSMessageParser.parse(data)
            thread = Thread(target=self._handle_request, args=(dns_query, requester_addr))
            thread.start()

    def _handle_request(self, dns_query: DNSMessage, requester_address):
        try:
            if self.cache.is_record_cached(dns_query):
                self._handle_cached_record(dns_query, requester_address)
                print(f"DNS Request from {requester_address} handled using cached response.")
            else:
                self._handle_uncached_record(dns_query, requester_address)
                print(f"DNS Request from {requester_address} handled by requesting from DNS Server.")
        except Exception as e:
            print("Error processing DNS request:", e)

    def _handle_cached_record(self, dns_query: DNSMessage, requester_address):
        cached_response = self.cache.get_record(dns_query)
        cached_response.header.transaction_id = dns_query.header.transaction_id
        self._send_response(cached_response, requester_address)

    def _handle_uncached_record(self, dns_query: DNSMessage, requester_address):
        dns_response = self._send_query(dns_query)
        self.cache.add_record(dns_query, dns_response)
        self._send_response(dns_response, requester_address)

    def _send_query(self, dns_query: DNSMessage):
        query_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        query_socket.sendto(bytes(dns_query), (self.dns_server_ip, self.DNS_SERVER_PORT))
        dns_answer, _ = query_socket.recvfrom(1024)
        query_socket.close()
        return DNSMessageParser.parse(dns_answer)

    def _send_response(self, dns_response: DNSMessage, requester_address):
        self.request_socket.sendto(bytes(dns_response), requester_address)
