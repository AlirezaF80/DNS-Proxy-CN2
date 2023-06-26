import socket

from DNSMessageParser import *


class DNSProxyServer:
    def __init__(self, DNSserverIP, host_address, port):
        self.DNSserverIP = DNSserverIP
        self.host_address = host_address
        self.port = port
        self.request_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def start(self):
        try:
            self.request_socket.bind((self.host_address, self.port))
            print("UDP DNS proxy server started. Listening on port", self.port)

            while True:
                data, requester_addr = self.request_socket.recvfrom(1024)
                dns_query = DNSMessageParser.parse(data)
                self._handle_request(dns_query, requester_addr)
        except Exception as e:
            print("Error starting DNS proxy server:", e)
        finally:
            self.request_socket.close()

    def _handle_request(self, dns_query, requester_address):
        try:
            response = self._send_query(dns_query)
            print("Response from", requester_address, "processed")
            self.request_socket.sendto(bytes(response), requester_address)
        except Exception as e:
            print("Error processing DNS request:", e)

    def _send_query(self, dns_query):
        server = (self.DNSserverIP, 53)
        query_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        query_socket.sendto(bytes(dns_query), server)
        dns_answer, _ = query_socket.recvfrom(1024)
        query_socket.close()
        return DNSMessageParser.parse(dns_answer)
