import socket
from threading import Thread

from Cache import Cache
from DNSMessage import DNSMessage
from DNSMessageParser import DNSMessageParser


class DNSProxyServer:
    DNS_SERVER_PORT = 53

    def __init__(self, dns_server_ip: list, host_address, listen_port, cache: Cache):
        self.dns_server_ip = dns_server_ip
        self.host_address = host_address
        self.listen_port = listen_port
        self.cache: Cache = cache
        self.request_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

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
            dns_response = self._answer_query(dns_query)
            self._send_response_to_requester(dns_response, requester_address)
        except Exception as e:
            print("Error processing DNS request:", e)

    def _send_response_to_requester(self, dns_response: DNSMessage, requester_address):
        self.request_socket.sendto(bytes(dns_response), requester_address)

    def _answer_query(self, dns_query):
        if self.cache.is_record_cached(dns_query):
            dns_response = self._answer_query_from_cache(dns_query)
            print(f"a DNS Request answered using cached response.")
        else:
            dns_response = self._answer_query_from_dns(dns_query)
            self.cache.add_record(dns_query, dns_response)
            print(f"a DNS Request answered by requesting from DNS Server.")
        return dns_response

    def _answer_query_from_cache(self, dns_query: DNSMessage):
        cached_response = self.cache.get_record(dns_query)
        cached_response.header.transaction_id = dns_query.header.transaction_id
        return cached_response

    def _answer_query_from_dns(self, dns_query: DNSMessage):
        query_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        query_socket.sendto(bytes(dns_query), (self.dns_server_ip, self.DNS_SERVER_PORT))
        dns_answer, _ = query_socket.recvfrom(1024)
        query_socket.close()
        return DNSMessageParser.parse(dns_answer)
