import socket


class DNSProxyServer:
    def __init__(self, DNSserverIP, host_address, port):
        self.DNSserverIP = DNSserverIP
        self.host_address = host_address
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def start(self):
        try:
            self.socket.bind((self.host_address, self.port))
            print("UDP DNS proxy server started. Listening on port", self.port)

            while True:
                data, addr = self.socket.recvfrom(1024)
                self._handle_request(data, addr)
                print("Request from", addr, "processed")
                print(data.hex())
                print("\n")
        except Exception as e:
            print("Error starting DNS proxy server:", e)
        finally:
            self.socket.close()

    def _handle_request(self, data, addr):
        try:
            response = self._send_query(data)
            self.socket.sendto(response, addr)
        except Exception as e:
            print("Error processing DNS request:", e)

    def _send_query(self, query):
        server = (self.DNSserverIP, 53)
        query_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        query_socket.sendto(query, server)
        response, _ = query_socket.recvfrom(1024)
        query_socket.close()
        return response
