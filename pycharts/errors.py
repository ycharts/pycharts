
class PyChartsRequestError(Exception):

	def __init__(self, error_message=None):
		self.error_message = error_message
		self.error_code = 400

	def __str__(self):
		return '{0}: {1}'.format(self.error_message, self.error_code)


class PyChartsRequestUrlNotFoundError(PyChartsRequestError):
	
	def __init__(self):
		self.error_message = 'URL not found'
		self.error_code = 404


class PyChartsRequestUnauthorizedError(PyChartsRequestError):

	def __init__(self):
		self.error_message = 'Invalid or Missing API Key'
		self.error_code = 401


class PyChartsRequestTooLongError(PyChartsRequestError):

	def __init__(self, error_message=None):
		self.error_message = error_message
		self.error_code = 414