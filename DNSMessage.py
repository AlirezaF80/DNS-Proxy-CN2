class DNSMessageHeader:
    def __init__(self, transaction_id, flags, queries_num, answers_num, auth_num, additional_num):
        self.transaction_id = transaction_id
        self.flags = flags
        self.queries_num = queries_num
        self.answers_num = answers_num
        self.auth_num = auth_num
        self.additional_num = additional_num

    def __bytes__(self):
        transaction_id_bytes = self.transaction_id.to_bytes(2, 'big')
        flags_bytes = self.flags.to_bytes(2, 'big')
        queries_num_bytes = self.queries_num.to_bytes(2, 'big')
        answers_num_bytes = self.answers_num.to_bytes(2, 'big')
        auth_num_bytes = self.auth_num.to_bytes(2, 'big')
        additional_num_bytes = self.additional_num.to_bytes(2, 'big')
        return transaction_id_bytes + flags_bytes + queries_num_bytes + answers_num_bytes + auth_num_bytes + additional_num_bytes

    def __len__(self):
        return len(self.__bytes__())

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

    def __eq__(self, other):
        return self.query_name == other.query_name and self.query_type == other.query_type and self.query_class == other.query_class

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
        ttl_bytes = self.rr_ttl.to_bytes(4, 'big')
        rdlen_bytes = self.rdlength.to_bytes(2, 'big')
        rdata_bytes = self.rdata
        return name_bytes + type_bytes + class_bytes + ttl_bytes + rdlen_bytes + rdata_bytes

    def __len__(self):
        return len(self.__bytes__())

    def __repr__(self):
        return f'DNSMessageResourceRecord(Name: {self.rr_name}, Type: {self.rr_type}, Class: {self.rr_class}' \
               f', TTL: {self.rr_ttl}, RDLength: {self.rdlength}, RData: {self.rdata})'


class DNSMessage:
    def __init__(self, header, queries, answers, authority, additional):
        self.header: DNSMessageHeader = header
        self.queries: list[DNSMessageQuery] = queries
        self.answers: list[DNSMessageResourceRecord] = answers
        self.authority: list[DNSMessageResourceRecord] = authority
        self.additional: list[DNSMessageResourceRecord] = additional

    def __bytes__(self):
        header_bytes = bytes(self.header)
        queries_bytes = b''
        for query in self.queries:
            queries_bytes += bytes(query)
        answers_bytes = b''
        for answer in self.answers:
            answers_bytes += bytes(answer)
        authority_bytes = b''
        for auth in self.authority:
            authority_bytes += bytes(auth)
        additional_bytes = b''
        for add in self.additional:
            additional_bytes += bytes(add)
        return header_bytes + queries_bytes + answers_bytes + authority_bytes + additional_bytes

    def __len__(self):
        return len(self.__bytes__())

    def __repr__(self):
        return f'DNSMessage(Header: {self.header}, Queries: {self.queries}, Answers: {self.answers}' \
               f', Authority: {self.authority}, Additional: {self.additional})'
