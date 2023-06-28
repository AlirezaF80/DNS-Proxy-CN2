from DNSMessage import DNSMessage, DNSMessageHeader, DNSMessageQuery


class DNSMessageCreator:
    @staticmethod
    def create_dns_request(domain_name) -> DNSMessage:
        return DNSMessageCreator._create_dns_message(domain_name, 1, 1)

    @staticmethod
    def _create_dns_message(domain_name, query_type, query_class) -> DNSMessage:
        header = DNSMessageHeader(0, 0, 1, 0, 0, 0)
        query = DNSMessageQuery(domain_name, query_type, query_class)
        return DNSMessage(header, [query], [], [], [])
