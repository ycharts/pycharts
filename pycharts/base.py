import datetime
import json
from pycharts import exceptions
try:
    # Python 3
    from urllib.parse import urlencode
    from urllib.error import HTTPError
    from urllib.request import Request, urlopen
except ImportError:
    # Python2
    from urllib import urlencode
    from urllib2 import HTTPError, Request, urlopen


class BaseSecurityClient(object):
    """
    Base Class for all security api clients
    that provides shared functionality and enforces
    a common interface.
    """

    API_VERSION = 'v3'
    BASE_URL = 'https://ycharts.com/api'
    SECURITY_TYPE_PATH = None
    VALID_SECURITY_FILTERS = None

    def __init__(self, api_key):
        """
        Args:
            api_key (str): The API key that authorizes a client to query security data
        """
        self.header = {'X-YCHARTSAUTHORIZATION': api_key}

    def get_securities(self, page=1, **filter_param):
        """
        Queries /<security_type> endpoint to return a paged
        list of securities.
        """
        url_path = self._build_url_path(None, None)
        params = {'page': page}
        # the endpoints respond just fine to invaliid query params,
        # they just ignore them, but the the real value of the endpoints
        # is only revealed when using the filters, so let's not waste
        # requests on filters that don't do anything.
        if filter_param:
            query_filter = filter_param.popitem()
            if query_filter[0] in self.VALID_SECURITY_FILTERS:
                params[query_filter[0]] = query_filter[1]
            else:
                error_msg = 'Invalid filter param. Must be one of: {0}'.format(','.join(self.VALID_SECURITY_FILTERS))
                raise exceptions.PyChartsRequestException(error_msg)

        return self._get_data(url_path, params)

    def get_points(self, security_symbols, calculation_codes, query_date=None):
        """
        Queries data from a /<security_type>/points endpoint.

        Args:
            security_symbols (list): List of string symbols
            calculation_codes (list): List og string calculation codes
            query_date
                (datetime): datetime object on or before which the endpoint will query data for.
                (int): Negative integer representing relative periods(as it relates to each calc code) in the past.

        Returns:
            dict of the decoded json from server response.

        Notes:
            The max length of any list arg is 100
        """
        security_symbols = self._str_or_list(security_symbols)
        calculation_codes = self._str_or_list(calculation_codes)

        url_path = self._build_url_path(security_symbols,
            'points', calculation_codes)

        if query_date:
            params = {'date': self._format_query_date_for_url(query_date)}
        else:
            params = None

        return self._get_data(url_path, params)

    def get_series(self, security_symbols, calculation_codes, query_start_date=None, query_end_date=None,
        resample_frequency=None, resample_function=None, fill_method=None, aggregate_function=None):
        """
        Queries data from a /<security_type>/series endpoint.

        Args:
            security_symbols (list): List of string symbols
            calculation_codes (list): List og string calculation codes
            query_start_date
                (datetime): date after which the endpoint will query data for.
                (int): Negative integer representing relative periods(as it relates to each calc code) in the past.
            query_end_date
                (datetime): date on or before which the endpoint will query data for. 
                (int): Negative integer representing relative periods(as it relates to each calc code) in the past.

        Returns:
            dict of the decoded json from server response.

        Notes:
            The max length of any list arg is 100
        """
        security_symbols = self._str_or_list(security_symbols)
        calculation_codes = self._str_or_list(calculation_codes)

        url_path = self._build_url_path(security_symbols, 
            'series', calculation_codes)

        params = {}
        if query_start_date:
            params['start_date'] = self._format_query_date_for_url(query_start_date)
        if query_end_date:
            params['end_date'] = self._format_query_date_for_url(query_end_date)
        if resample_frequency:
            params['resample_frequency'] = resample_frequency
        if resample_function:
            params['resample_function'] = resample_function
        if fill_method:
            params['fill_method'] = fill_method
        if aggregate_function:
            params['aggregate_function'] = aggregate_function

        return self._get_data(url_path, params)  

    def get_info(self, security_symbols, info_field_codes):
        """
        Queries data from a /<security_type>/info endpoint.

        Args:
            security_symbols (list): List of string symbols
            info_field_codes (list): List of string info field codes

        Returns:
            dict of the decoded json from server response.

        Notes:
            The max length of any list arg is 100

        """
        security_symbols = self._str_or_list(security_symbols)
        info_field_codes = self._str_or_list(info_field_codes)

        url_path = self._build_url_path(security_symbols,
            'info', info_field_codes)

        return self._get_data(url_path, None)

    # Private Helper Methods
    def _get_data(self, url_path, params=None):
        url = '{0}/{1}/{2}'.format(self.BASE_URL, self.API_VERSION, url_path)
        if params:
            encoded_params = urlencode(params)
            url = '{0}?{1}'.format(url, encoded_params)

        url = url.replace(' ', '')
        req = Request(url, headers=self.header)
        response = self._parse_response(req)
        
        return response

    def _parse_response(self, req):
        try:
            response = urlopen(req).read().decode('utf-8')
        except HTTPError as http_error:
            if http_error.code == 404:
                raise exceptions.PyChartsRequestUrlNotFoundException()
            elif http_error.code == 401:
                raise exceptions.PyChartsRequestUnauthorizedException()
            elif http_error.code == 400:
                raise exceptions.PyChartsRequestException()
            else:
                raise

        parsed_rsp = json.loads(response)
        # raise any payload level errors
        if parsed_rsp['meta']['status'] == 'error':
            error_code = parsed_rsp['meta']['error_code']
            error_message = parsed_rsp['meta']['error_message']
            if error_code == 400:
                raise exceptions.PyChartsRequestException(error_message=error_message)
            elif error_code == 414:
                raise exceptions.PyChartsRequestTooLongException(error_message=error_message)

        return parsed_rsp
    
    def _build_url_path(self, security_symbols, query_type_path, query_keys=None):

        url_path = self.SECURITY_TYPE_PATH

        if security_symbols and query_type_path:
            security_symbol_params = self._format_list_for_url(security_symbols)
            url_path = '{0}/{1}/{2}'.format(url_path, security_symbol_params, query_type_path)

        if query_keys:
            query_key_params = self._format_list_for_url(query_keys)
            url_path = '{0}/{1}'.format(url_path, query_key_params)
        
        return url_path

    def _format_query_date_for_url(self, query_date):
        if isinstance(query_date, datetime.datetime):
            return query_date.isoformat().split('T')[0]
        elif isinstance(query_date, int) and query_date < 0:
            return query_date
        else:
            error_message = 'Invalid Date paramter. Date should be a datetime object or a negative integer.'
            raise exceptions.PyChartsRequestException(error_message=error_message)

    def _format_list_for_url(self, list_param):
        return ','.join(list_param)

    def _str_or_list(self, arg):
        if not isinstance(arg, (list, tuple)) and arg is not None:
            arg = [arg]
        return arg
