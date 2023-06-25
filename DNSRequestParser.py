class DNSHeader:
    def __init__(self, id, flags, questions_num, answers_num, auth_num, additional_num):
        self.id = id
        self.flags = flags
        self.questions_num = questions_num
        self.answers_num = answers_num
        self.auth_num = auth_num
        self.additional_num = additional_num

    def __repr__(self):
        return f'ID: {self.id}, Flags: {self.flags}, # Questions: {self.questions_num}' \
               f', # Answer RRs: {self.answers_num}, # Authority RRs: {self.auth_num}' \
               f', # AdditionalRRs : {self.additional_num}'


class DNSQuery:
    def __init__(self, name, type, class_):
        self.name = name
        self.type = type
        self.class_ = class_

    def __repr__(self):
        return f'Name: {self.name}, Type: {self.type}, Class: {self.class_}'


class DNSRequest:
    def __init__(self, message):
        self.message = message
        self.header = self.parse_header()
        self.queries = self.parse_questions()

    def parse_header(self):
        header_data = self.message[:12]
        id = (header_data[0] << 8) + header_data[1]
        flags = (header_data[2] << 8) + header_data[3]
        questions_num = (header_data[4] << 8) + header_data[5]
        answers_num = (header_data[6] << 8) + header_data[7]
        auth_num = (header_data[8] << 8) + header_data[9]
        additional_num = (header_data[10] << 8) + header_data[11]

        return DNSHeader(id, flags, questions_num, answers_num, auth_num, additional_num)

    def parse_questions(self):
        if self.header.questions_num == 0:
            return []
        queries = []
        cur_offset = 12

        for _ in range(self.header.questions_num):
            qname_parts = []
            while True:
                length = self.message[cur_offset]
                if length == 0:
                    break

                cur_offset += 1
                query_part = self.message[cur_offset:cur_offset + length].decode('utf-8')
                qname_parts.append(query_part)
                cur_offset += length
            query_name = '.'.join(qname_parts)
            cur_offset += 1
            query_type = (self.message[cur_offset] << 8) + self.message[cur_offset + 1]
            cur_offset += 2
            query_class = (self.message[cur_offset] << 8) + self.message[cur_offset + 1]
            dns_query = DNSQuery(query_name, query_type, query_class)
            queries.append(dns_query)
            cur_offset += 2

        return queries


if __name__ == '__main__':
    dns_message = '00028180000100010000000006676f6f676c6503636f6d0000010001c00c00010001000000b50004d8ef2678'
    dns_message = bytes.fromhex(dns_message)
    dns_request = DNSRequest(dns_message)

    print('Header:', dns_request.header)
    print('Queries:', dns_request.queries)
