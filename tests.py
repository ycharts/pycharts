import datetime
import unittest
from unittest import mock, TestCase
import json
from pycharts.clients import CompanyClient
from pycharts import exceptions


#########################################
#####      MOCKING UTILITIES        #####
#########################################
class MockHttpResponse(object):

    URL_RESPONSE_INDEX = {
        'https://ycharts.com/api/v3/companies/AAPL/points/price': {
            'response': {
                'AAPL': {
                    'meta': {'status': 'ok'},
                    'results': {
                        'price': {
                            'meta': {'status': 'ok'},
                            'data': ['2016-09-15', 115.39],
                        },
                    },
                },
                'MSFT': {
                    'meta': {'status': 'ok'},
                    'results': {
                        'price': {
                            'meta': {'status': 'ok'},
                            'data': ['2016-09-15', 57.21],
                        },
                    },
                },
            },
            'meta': {'url': 'http://ycharts.com/api/v3/companies/AAPL,MSFT/points/price', 'status': 'ok'},
        },
        'https://ycharts.com/api/v3/companies/AAPL/series/price?start_date=2016-09-10': {
            'response': {
                'AAPL': {
                    'results': {
                        'price': {
                            'data': [['2016-09-12', 105.44], ['2016-09-13', 107.95], ['2016-09-14', 111.77], ['2016-09-15', 115.39]],
                            'meta': {'status': 'ok'},
                        },
                    },
                    'meta': {'status': 'ok'},
                },
            },
            'meta': {'url': 'http://ycharts.com/api/v3/companies/AAPL/series/price?start_date=2016-09-10', 'status': 'ok'},
        },
        'https://ycharts.com/api/v3/companies/AAPL/info/name': {
            'response': {
                'AAPL': {
                    'results': {
                        'name': {'data': 'Apple', 'meta': {'status': 'ok'}},
                    },
                    'meta': {'status': 'ok'},
                },
            },
            'meta': {'url': 'http://ycharts.com/api/v3/companies/AAPL/info/name', 'status': 'ok'},
        },
        'https://ycharts.com/api/v3/companies/TOOMANY/info/name': {
            'response': {},
            'meta': {
                'error_message': 'Too many identifiers. Ensure 100 or less.',
                'status': 'error',
                'error_code': 414,
                'url': 'http://ycharts.com/api/v3/companies/TOOMANY/info/name',
            },
        }
    }

    def __init__(self, request):
        self.request = request

    def read(self):
        return json.dumps(self.URL_RESPONSE_INDEX[self.request.get_full_url()]).encode('utf-8')


def mock_urlopen(request):
    return MockHttpResponse(request)

#########################################
#####           TEST CASES          #####
#########################################
class ClientTestCase(TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.client = CompanyClient('api_key')

    @mock.patch('pycharts.base.urlopen', mock_urlopen)
    def test_successful_point_request(self):
        point_rsp = self.client.get_points(['AAPL'], ['price'])
        status = point_rsp['meta']['status']
        security_response_data = point_rsp['response']['AAPL']
        securty_query_status = security_response_data['meta']['status']
        calculation_response_data = security_response_data['results']['price']
        calculation_query_status = calculation_response_data['meta']['status']
        calculation_query_data = calculation_response_data['data']
        # assertions
        self.assertEqual(status, 'ok')
        self.assertEqual(securty_query_status, 'ok')
        self.assertEqual(calculation_query_status, 'ok')
        self.assertEqual(calculation_query_data, ['2016-09-15', 115.39])

    @mock.patch('pycharts.base.urlopen', mock_urlopen)
    def test_successful_series_request(self):
        query_start_date = datetime.datetime(2016, 9, 10)
        series_rsp = self.client.get_series(['AAPL'], ['price'],query_start_date=query_start_date)
        status = series_rsp['meta']['status']
        security_response_data = series_rsp['response']['AAPL']
        securty_query_status = security_response_data['meta']['status']
        calculation_response_data = security_response_data['results']['price']
        calculation_query_status = calculation_response_data['meta']['status']
        calculation_query_data = calculation_response_data['data']
        # assertions
        self.assertEqual(status, 'ok')
        self.assertEqual(securty_query_status, 'ok')
        self.assertEqual(calculation_query_status, 'ok')
        expected_data = [['2016-09-12', 105.44], ['2016-09-13', 107.95],
            ['2016-09-14', 111.77], ['2016-09-15', 115.39]]
        self.assertEqual(calculation_query_data, expected_data)

    @mock.patch('pycharts.base.urlopen', mock_urlopen)
    def test_successful_info_request(self):
        info_rsp = self.client.get_info(['AAPL'], ['name'])
        status = info_rsp['meta']['status']
        security_response_data = info_rsp['response']['AAPL']
        securty_query_status = security_response_data['meta']['status']
        info_response_data = security_response_data['results']['name']
        info_query_status = info_response_data['meta']['status']
        info_query_data = info_response_data['data']
        # assertions
        self.assertEqual(status, 'ok')
        self.assertEqual(securty_query_status, 'ok')
        self.assertEqual(info_query_status, 'ok')
        self.assertEqual(info_query_data, 'Apple')

    # The 2 below methods test exceptions we raise as a result
    # of parsing a succesful rsp from the server. Though the request
    # themselves are 200, from a client application perspetive, they are
    # showstoppers so we want to make sure the exceptions are raised
    # appropriately.
    @mock.patch('pycharts.base.urlopen', mock_urlopen)
    def test_400_raise(self):

        with self.assertRaises(exceptions.PyChartsRequestException) as cm:
            self.client.get_points('AAPL', 'price', query_date=45)

        self.assertEqual(cm.exception.error_code, 400)

    @mock.patch('pycharts.base.urlopen', mock_urlopen)
    def test_414_raise(self):

        with self.assertRaises(exceptions.PyChartsRequestTooLongException) as cm:
            self.client.get_info(['TOOMANY'], ['name'])

        self.assertEqual(cm.exception.error_code, 414)


if __name__ == '__main__':
    unittest.main()
