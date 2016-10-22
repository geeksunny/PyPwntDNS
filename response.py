class ApiResponse(object):

    #####
    def __init__(self, status_code, body):
        self.statusCode = status_code
        self.body = body
