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


class DNSRequest:
    def __init__(self, message):
        self.message = message
        self.header = self.header = self.parse_header()

    def parse_header(self):
        header_data = self.message[:12]
        id = (header_data[0] << 8) + header_data[1]
        flags = (header_data[2] << 8) + header_data[3]
        questions_num = (header_data[4] << 8) + header_data[5]
        answers_num = (header_data[6] << 8) + header_data[7]
        auth_num = (header_data[8] << 8) + header_data[9]
        additional_num = (header_data[10] << 8) + header_data[11]

        return DNSHeader(id, flags, questions_num, answers_num, auth_num, additional_num)


if __name__ == '__main__':
    dns_message = '00028180000100010000000006676f6f676c6503636f6d0000010001c00c00010001000000b50004d8ef2678'
    dns_message = bytes.fromhex(dns_message)
    dns_request = DNSRequest(dns_message)

    print('Header:', dns_request.header)
