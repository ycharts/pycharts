
class PyChartsRequestException(Exception):

    def __init__(self, error_message=''):
        self.error_message = error_message
        self.error_code = 400

    def __str__(self):
        return '{0} code:{1}'.format(self.error_message, self.error_code)


class PyChartsRequestUrlNotFoundException(PyChartsRequestException):
    
    def __init__(self):
        self.error_message = 'URL not found.'
        self.error_code = 404


class PyChartsRequestUnauthorizedException(PyChartsRequestException):

    def __init__(self):
        self.error_message = 'Invalid or Missing API Key.'
        self.error_code = 401


class PyChartsRequestTooLongException(PyChartsRequestException):

    def __init__(self, error_message=None):
        self.error_message = error_message
        self.error_code = 414
