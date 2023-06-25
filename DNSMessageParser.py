class DNSMessageHeader:
    def __init__(self, transaction_id, flags, queries_num, answers_num, auth_num, additional_num):
        self.transaction_id = transaction_id
        self.flags = flags
        self.queries_num = queries_num
        self.answers_num = answers_num
        self.auth_num = auth_num
        self.additional_num = additional_num

    def __repr__(self):
        return f'DNSHeader(ID: {self.transaction_id}, Flags: {self.flags}, # Queries: {self.queries_num}' \
               f', # Answer RRs: {self.answers_num}, # Authority RRs: {self.auth_num}' \
               f', # AdditionalRRs : {self.additional_num})'


class DNSMessageQuery:
    def __init__(self, query_name, query_type, query_class):
        self.query_name = query_name
        self.query_type = query_type
        self.query_class = query_class

    def __bytes__(self):
        name_parts = self.query_name.split('.')
        name_bytes = b''
        for part in name_parts:
            name_bytes += bytes([len(part)])
            name_bytes += part.encode('utf-8')
        name_bytes += b'\x00'
        type_bytes = self.query_type.to_bytes(2, 'big')
        class_bytes = self.query_class.to_bytes(2, 'big')
        return name_bytes + type_bytes + class_bytes

    def __len__(self):
        return len(self.__bytes__())

    def __repr__(self):
        return f'DNSQuery(Name: {self.query_name}, Type: {self.query_type}, Class: {self.query_class})'


class DNSMessageResourceRecord:
    def __init__(self, rr_name, rr_type, rr_class, rr_ttl, rdlength, rdata):
        self.rr_name = rr_name
        self.rr_type = rr_type
        self.rr_class = rr_class
        self.rr_ttl = rr_ttl
        self.rdlength = rdlength
        self.rdata = rdata

    def __bytes__(self):
        name_bytes = self.rr_name.to_bytes(2, 'big')
        type_bytes = self.rr_type.to_bytes(2, 'big')
        class_bytes = self.rr_class.to_bytes(2, 'big')
        ttl_bytes = self.rr_ttl.to_bytes(2, 'big')
        rdlen_bytes = self.rdlength.to_bytes(2, 'big')
        rdata_bytes = self.rdata
        return name_bytes + type_bytes + class_bytes + ttl_bytes + rdata_bytes + rdlen_bytes

    def __len__(self):
        return len(self.__bytes__())

    def __repr__(self):
        return f'DNSMessageResourceRecord(Name: {self.rr_name}, Type: {self.rr_type}, Class: {self.rr_class}' \
               f', TTL: {self.rr_ttl}, RDLength: {self.rdlength}, RData: {self.rdata})'


class DNSMessage:
    def __init__(self, header, queries, answers, authority, additional):
        self.header = header
        self.queries = queries
        self.answers = answers
        self.authority = authority
        self.additional = additional


class DNSMessageParser:
    @staticmethod
    def parse(message):
        message = message
        header = DNSMessageParser.parse_header(message)
        queries = DNSMessageParser.parse_queries(message, header.queries_num)
        answers_offset = 12 + sum(len(query) for query in queries)
        answers = DNSMessageParser.parse_resource_records(message, answers_offset, header.answers_num)
        authority_offset = answers_offset + sum(len(ans) for ans in answers)
        authority = DNSMessageParser.parse_resource_records(message, authority_offset, header.auth_num)
        additional_offset = authority_offset + sum(len(auth) for auth in authority)
        additional = DNSMessageParser.parse_resource_records(message, additional_offset, header.additional_num)
        return DNSMessage(header, queries, answers, authority, additional)

    @staticmethod
    def parse_header(message) -> DNSMessageHeader:
        header_data = message[:12]
        transaction_id = (header_data[0] << 8) + header_data[1]
        flags = (header_data[2] << 8) + header_data[3]
        queries_num = (header_data[4] << 8) + header_data[5]
        answers_num = (header_data[6] << 8) + header_data[7]
        auth_num = (header_data[8] << 8) + header_data[9]
        additional_num = (header_data[10] << 8) + header_data[11]

        return DNSMessageHeader(transaction_id, flags, queries_num, answers_num, auth_num, additional_num)

    @staticmethod
    def parse_queries(message, queries_num) -> list[DNSMessageQuery]:
        if queries_num == 0:
            return []

        cur_offset = 12
        queries = []
        for _ in range(queries_num):
            query_name_parts = []
            while True:
                length = message[cur_offset]
                if length == 0:
                    break

                cur_offset += 1
                query_part = message[cur_offset:cur_offset + length].decode('utf-8')
                query_name_parts.append(query_part)
                cur_offset += length
            query_name = '.'.join(query_name_parts)
            cur_offset += 1
            query_type = (message[cur_offset] << 8) + message[cur_offset + 1]
            cur_offset += 2
            query_class = (message[cur_offset] << 8) + message[cur_offset + 1]
            dns_query = DNSMessageQuery(query_name, query_type, query_class)
            queries.append(dns_query)
            cur_offset += 2

        return queries

    @staticmethod
    def parse_resource_records(message, offset, resource_records_num) -> list[DNSMessageResourceRecord]:
        if resource_records_num == 0:
            return []

        cur_offset = offset

        resource_records = []
        for _ in range(resource_records_num):
            rr_name = (message[offset] << 8) + message[offset + 1]
            cur_offset += 2
            rr_type = (message[cur_offset] << 8) + message[cur_offset + 1]
            cur_offset += 2
            rr_class = (message[cur_offset] << 8) + message[cur_offset + 1]
            cur_offset += 2
            rr_ttl = (message[cur_offset] << 24) + (message[cur_offset + 1] << 16) + (
                    message[cur_offset + 2] << 8) + message[cur_offset + 3]
            cur_offset += 4
            rdlength = (message[cur_offset] << 8) + message[cur_offset + 1]
            cur_offset += 2
            rdata = message[cur_offset:cur_offset + rdlength]
            cur_offset += rdlength
            resource_record = DNSMessageResourceRecord(rr_name, rr_type, rr_class, rr_ttl, rdlength, rdata)
            resource_records.append(resource_record)
        return resource_records


if __name__ == '__main__':
    dns_message_hex = '45fe818000010002000000000474696d65046e69737403676f760000010001c00c000500010000041b000b046e74703103676c62c011c02b00010001000000ed000484a36106'
    dns_message_hex = bytes.fromhex(dns_message_hex)
    dns_message = DNSMessageParser.parse(dns_message_hex)

    print('Header:', dns_message.header)
    print('Queries:', dns_message.queries)
    print('Answers:', dns_message.answers)
