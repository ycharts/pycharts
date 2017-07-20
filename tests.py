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
        },
        'https://ycharts.com/api/v3/companies?page=1': {
            'response': [{'name': 'Apple', 'symbol': 'AAPL'}, {'name': 'Microsoft', 'symbol': 'MSFT'}],
            'meta': {
                'status': 'ok', 
                'url': 'https://ycharts.com/api/v3/companies?page=1', 
                'pagination_info': {
                    'end_index': 2, 'num_items': 2, 'start_index': 1, 
                    'num_pages': 1, 'current_page_num': 1
                }
            }
        },
        'https://ycharts.com/api/v3/companies/AAPL/dividends?start_date=2015-01-01': {
            'meta': {
                'status': 'ok',
                'url': 'http://ycharts.com/api/v3/companies/AAPL/dividends?start_date=2015-01-01'
            },
            'response': {
                'AAPL': {
                    'meta': {
                        'status': 'ok'
                    },
                    'results': [
                        {
                            'adjusted_dividend_amount': 0.47,
                            'currency_code': 'USD',
                            'declared_date': '2015-01-27',
                            'dividend_amount': 0.47,
                            'dividend_type': 'normal',
                            'ex_date': '2015-02-05',
                            'pay_date': '2015-02-12',
                            'record_date': '2015-02-09'
                        }
                    ]
                }
            }
        },
        'https://ycharts.com/api/v3/companies/AAPL/splits?end_date=2014-01-01': {
            'meta': {
                'status': 'ok',
                'url': 'https://ycharts.com/api/v3/companies/AAPL/splits?end_date=2014-01-01'
            },
            'response': {
                'AAPL': {
                    'meta': {
                        'status': 'ok'
                    },
                    'results': [
                        {
                            'day': '1987-06-16',
                            'is_stock_dividend': 'false',
                            'ratio': 2.0,
                            'status': 'executed'
                        }
                    ]
                }
            }
        },
        'https://ycharts.com/api/v3/companies/GGP/spinoffs?end_date=2014-01-01': {
            'meta': {
                'status': 'ok',
                'url': 'https://ycharts.com/api/v3/companies/GGP/spinoffs?end_date=2014-01-01'
            },
            'response': {
                'GGP': {
                    'meta': {
                        'status': 'ok'
                    },
                    'results': [
                        {
                            'child_company_exchange': 'null',
                            'child_company_symbol': 'NYU',
                            'day': '2010-11-10',
                            'ratio': 1.259958,
                            'status': 'executed'
                        }
                    ]
                }
            }
        },
        'https://ycharts.com/api/v3/companies/AAPL/series/price?aggregate_function=max': {
            'response': {
                'AAPL': {
                    'results': {
                        'price': {
                            'data': [['2016-09-12', 99999.00]],
                            'meta': {'status': 'ok'},
                        },
                    },
                    'meta': {'status': 'ok'},
                },
            },
            'meta': {'url': 'http://ycharts.com/api/v3/companies/AAPL/series/price?aggregate_function=max', 'status': 'ok'},
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

    @mock.patch('pycharts.base.urlopen', mock_urlopen)
    def test_successful_securities_request(self):
        securities_rsp = self.client.get_securities()
        meta = securities_rsp['meta']
        securities = securities_rsp['response']
        for security in securities:
            self.assertTrue(security['symbol'] in ['AAPL', 'MSFT'])
            self.assertTrue(security['name'] in ['Apple', 'Microsoft'])

        status = securities_rsp['meta']['status']
        self.assertEqual(status, 'ok')
        # test pagination info in the response
        pagination_info = meta['pagination_info']
        self.assertEqual(pagination_info['num_items'], 2)
        self.assertEqual(pagination_info['start_index'], 1)
        self.assertEqual(pagination_info['end_index'], 2)
        self.assertEqual(pagination_info['num_pages'], 1)
        self.assertEqual(pagination_info['current_page_num'], 1)

    def test_400_bad_filter_securities_request(self):
        with self.assertRaises(exceptions.PyChartsRequestException) as cm:
            self.client.get_securities(bad_filter='bad_value')

        self.assertEqual(cm.exception.error_code, 400)

    @mock.patch('pycharts.base.urlopen', mock_urlopen)
    def test_successful_dividend_request(self):
        start_date = datetime.datetime(2015, 1, 1)
        dividend_rsp = self.client.get_dividends('AAPL', ex_start_date=start_date)
        status = dividend_rsp['meta']['status']
        dividend_data = dividend_rsp['response']['AAPL']['results']
        # assertions
        self.assertEqual(status, 'ok')
        self.assertEqual(len(dividend_data), 1)
        self.assertEqual(dividend_data[0]['adjusted_dividend_amount'],  0.47)
        self.assertEqual(dividend_data[0]['currency_code'], 'USD')
        self.assertEqual(dividend_data[0]['declared_date'], '2015-01-27')
        self.assertEqual(dividend_data[0]['dividend_amount'], 0.47)
        self.assertEqual(dividend_data[0]['dividend_type'], 'normal')
        self.assertEqual(dividend_data[0]['ex_date'], '2015-02-05')
        self.assertEqual(dividend_data[0]['pay_date'], '2015-02-12')
        self.assertEqual(dividend_data[0]['record_date'], '2015-02-09')

    @mock.patch('pycharts.base.urlopen', mock_urlopen)
    def test_successful_stock_split_request(self):
        end_date = datetime.datetime(2014, 1, 1)
        split_rsp = self.client.get_stock_splits('AAPL', split_end_date=end_date)
        status = split_rsp['meta']['status']
        split_data = split_rsp['response']['AAPL']['results']
        # assertions
        self.assertEqual(status, 'ok')
        self.assertEqual(len(split_data), 1)
        self.assertEqual(split_data[0]['day'],  '1987-06-16')
        self.assertEqual(split_data[0]['is_stock_dividend'],  'false')
        self.assertEqual(split_data[0]['ratio'],  2.0)
        self.assertEqual(split_data[0]['status'],  'executed')

    @mock.patch('pycharts.base.urlopen', mock_urlopen)
    def test_successful_stock_spinoff_request(self):
        end_date = datetime.datetime(2014, 1, 1)
        spinoff_rsp = self.client.get_stock_spinoffs('GGP', spinoff_end_date=end_date)
        status = spinoff_rsp['meta']['status']
        spinoff_data = spinoff_rsp['response']['GGP']['results']
        # assertions
        self.assertEqual(status, 'ok')
        self.assertEqual(len(spinoff_data), 1)
        self.assertEqual(spinoff_data[0]['day'],  '2010-11-10')
        self.assertEqual(spinoff_data[0]['child_company_symbol'],  'NYU')
        self.assertEqual(spinoff_data[0]['child_company_exchange'],  'null')
        self.assertEqual(spinoff_data[0]['status'],  'executed')
        self.assertEqual(spinoff_data[0]['ratio'],  1.259958)

    @mock.patch('pycharts.base.urlopen', mock_urlopen)
    def test_successful_series_request_with_aggregation(self):
        series_rsp = self.client.get_series(['AAPL'], ['price'], aggregate_function='max')
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
        expected_data = [['2016-09-12', 99999.00]]
        self.assertEqual(calculation_query_data, expected_data)

if __name__ == '__main__':
    unittest.main()
