import redis

from DNSMessage import DNSMessage
from DNSMessageParser import DNSMessageParser


class Cache:
    def __init__(self, cache_ttl, redis_host, redis_port):
        self.redis = redis.Redis(host=redis_host, port=redis_port, db=0)
        self.ttl = cache_ttl

    def add_record(self, dns_query: DNSMessage, dns_response: DNSMessage):
        if dns_query is None or dns_response is None:
            raise ValueError("DNS query and DNS response must not be None")
        if dns_query.queries[0].query_name != dns_response.queries[0].query_name:
            raise ValueError("DNS query and DNS response must have the same query name")
        key = self._get_key(dns_query)
        value = self._get_value(dns_response)
        self.redis.set(key, value, ex=self.ttl)

    def get_record(self, dns_query: DNSMessage):
        key = self._get_key(dns_query)
        value = self.redis.get(key)
        if value is not None:
            return DNSMessageParser.parse(value)
        return None

    @staticmethod
    def _get_key(dns_query: DNSMessage):
        if dns_query is None:
            raise ValueError("DNS query must not be None")
        if dns_query.header.queries_num != 1:
            raise ValueError("DNS query must have exactly one query")
        return dns_query.queries[0].query_name

    @staticmethod
    def _get_value(dns_response: DNSMessage):
        if dns_response is None:
            raise ValueError("DNS response must not be None")
        if dns_response.header.answers_num != 1:
            raise ValueError("DNS response must have exactly one answer")
        return bytes(dns_response)

    def remove_record(self, dns_query: DNSMessage):
        key = self._get_key(dns_query)
        self.redis.delete(key)

    def clear_cache(self):
        self.redis.flushdb()

    def is_record_cached(self, dns_query: DNSMessage):
        key = self._get_key(dns_query)
        return self.redis.exists(key) == 1


if __name__ == '__main__':
    c = Cache(5, 'localhost', 6379)
    c.clear_cache()
