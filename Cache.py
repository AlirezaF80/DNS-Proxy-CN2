import redis
from DNSMessage import DNSMessage
from DNSMessageParser import DNSMessageParser
from threading import RLock

class Cache:
    def __init__(self, cache_ttl, redis_host, redis_port):
        self.redis = redis.Redis(host=redis_host, port=redis_port, db=0)
        self.ttl = cache_ttl
        self.lock = RLock()

    def add_record(self, dns_query: DNSMessage, dns_response: DNSMessage):
        with self.lock:
            if dns_query is None or dns_response is None:
                raise ValueError("DNS query and DNS response must not be None")
            if dns_query.queries[0].query_name != dns_response.queries[0].query_name:
                raise ValueError("DNS query and DNS response must have the same query name")
            key = self._get_key(dns_query)
            value = self._get_value(dns_response)
            self.redis.set(key, value, ex=self.ttl)

    def get_record(self, dns_query: DNSMessage):
        with self.lock:
            key = self._get_key(dns_query)
            value = self.redis.get(key)
            if value is not None:
                return DNSMessageParser.parse(value)
            return None

    @staticmethod
    def _get_key(dns_query: DNSMessage):
        if dns_query is None:
            raise ValueError("DNS query must not be None")
        key = b''
        for q in dns_query.queries:
            key += bytes(q)
        return key

    @staticmethod
    def _get_value(dns_response: DNSMessage):
        if dns_response is None:
            raise ValueError("DNS response must not be None")
        return bytes(dns_response)

    def remove_record(self, dns_query: DNSMessage):
        with self.lock:
            key = self._get_key(dns_query)
            self.redis.delete(key)

    def clear_cache(self):
        with self.lock:
            self.redis.flushdb()

    def is_record_cached(self, dns_query: DNSMessage):
        with self.lock:
            key = self._get_key(dns_query)
            return self.redis.exists(key) == 1
