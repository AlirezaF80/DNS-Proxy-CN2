class cache:

    reqAddress = ""
    reqList = []

    def __init__(self, time_out, req):
        self.time_out = time_out
        self.req = req

    def check_req_in_list(self, reqList):
        if self.reqAddress in reqList:
            return self.reqAddress
        else:
            reqList.append(self.reqAddress)
            return False