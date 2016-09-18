class ApiResponse(object):
    statusCode = 0
    body = {}
    #
    def __init__(self, statusCode, body):
        self.statusCode = statusCode
        self.body = body