import socket

from DNSMessageParser import *


class DNSProxyServer:
    DNS_SERVER_PORT = 53

    def __init__(self, dns_server_ip, host_address, listen_port):
        self.dns_server_ip = dns_server_ip
        self.host_address = host_address
        self.listen_port = listen_port
        self.request_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

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
            dns_response = self._send_query(dns_query)
            print("Response from", requester_address, "processed")
            self.request_socket.sendto(bytes(dns_response), requester_address)
        except Exception as e:
            print("Error processing DNS request:", e)

    def _send_query(self, dns_query: DNSMessage):
        query_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        query_socket.sendto(bytes(dns_query), (self.dns_server_ip, self.DNS_SERVER_PORT))
        dns_answer, _ = query_socket.recvfrom(1024)
        query_socket.close()
        return DNSMessageParser.parse(dns_answer)
