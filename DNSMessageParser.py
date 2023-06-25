class DNSMessageHeader:
    def __init__(self, transaction_id, flags, questions_num, answers_num, auth_num, additional_num):
        self.transaction_id = transaction_id
        self.flags = flags
        self.questions_num = questions_num
        self.answers_num = answers_num
        self.auth_num = auth_num
        self.additional_num = additional_num

    def __repr__(self):
        return f'DNSHeader(ID: {self.transaction_id}, Flags: {self.flags}, # Questions: {self.questions_num}' \
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

    def __repr__(self):
        return f'DNSQuery(Name: {self.query_name}, Type: {self.query_type}, Class: {self.query_class})'


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
        queries = DNSMessageParser.parse_questions(message, header.questions_num)
        answers = []
        authority = []
        additional = []
        return DNSMessage(header, queries, answers, authority, additional)

    @staticmethod
    def parse_header(message) -> DNSMessageHeader:
        header_data = message[:12]
        transaction_id = (header_data[0] << 8) + header_data[1]
        flags = (header_data[2] << 8) + header_data[3]
        questions_num = (header_data[4] << 8) + header_data[5]
        answers_num = (header_data[6] << 8) + header_data[7]
        auth_num = (header_data[8] << 8) + header_data[9]
        additional_num = (header_data[10] << 8) + header_data[11]

        return DNSMessageHeader(transaction_id, flags, questions_num, answers_num, auth_num, additional_num)

    @staticmethod
    def parse_questions(message, question_num) -> list[DNSMessageQuery]:
        if question_num == 0:
            return []

        cur_offset = 12
        queries = []
        for _ in range(question_num):
            qname_parts = []
            while True:
                length = message[cur_offset]
                if length == 0:
                    break

                cur_offset += 1
                query_part = message[cur_offset:cur_offset + length].decode('utf-8')
                qname_parts.append(query_part)
                cur_offset += length
            query_name = '.'.join(qname_parts)
            cur_offset += 1
            query_type = (message[cur_offset] << 8) + message[cur_offset + 1]
            cur_offset += 2
            query_class = (message[cur_offset] << 8) + message[cur_offset + 1]
            dns_query = DNSMessageQuery(query_name, query_type, query_class)
            queries.append(dns_query)
            cur_offset += 2

        return queries


if __name__ == '__main__':
    dns_message_hex = '00028180000100010000000006676f6f676c6503636f6d0000010001c00c00010001000000b50004d8ef2678'
    dns_message_hex = bytes.fromhex(dns_message_hex)
    dns_message = DNSMessageParser.parse(dns_message_hex)

    print('Header:', dns_message.header)
    print('Queries:', dns_message.queries)
