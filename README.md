# DNS Proxy Server CN2
This is a DNS Proxy server written in Python for the Computer Networks 2 course at K.N.T.U. It serves as an intermediary between clients and external DNS servers, caching responses to improve performance.

## Features

- Acts as a DNS Proxy server, handling DNS requests and forwarding them to external DNS servers if not cached.
- Implements a cache using Redis to store and retrieve DNS responses.

## Usage

1. Install the required Python packages by running the following command: `pip install -r requirements.txt`

3. Modify the `ServerConfig.json` file to specify the desired server configuration.

4. Run the `Main.py` script to start the DNS proxy server:
`python Main.py`

5. The server will start listening for DNS requests on the specified host address and port. Clients can send DNS requests to the server, which will either serve the response from the cache or forward the request to the external DNS servers and cache the response.

## Contributors

- [Alireza Farzaneh](https://github.com/AlirezaF80)
- [Mohammad Salari](https://github.com/mohammadsalari-79)
