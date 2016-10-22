class ApiResponse(object):

    #####
    def __init__(self, status_code, body):
        self.status_code = status_code
        self.body = body
