class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message):
        Exception.__init__(self)
        self.message = message
