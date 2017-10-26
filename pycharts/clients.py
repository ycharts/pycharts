from pycharts.base import BaseSecurityClient


class CompanyClient(BaseSecurityClient):
    
    SECURITY_TYPE_PATH = 'companies'
    VALID_SECURITY_FILTERS = ['benchmark_index', 'exchange', 'hq_region', 'incorporation_region',
    	'industry',  'is_lp', 'is_reit', 'is_shell', 'naics_industry', 'naics_sector', 'sector']

    def get_dividends(self, security_symbols, ex_start_date=None, ex_end_date=None, dividend_type=None):
        security_symbols = self._str_or_list(security_symbols)

        url_path = self._build_url_path(security_symbols, 'dividends')

        params = {}
        if ex_start_date:
            params['start_date'] = self._format_query_date_for_url(ex_start_date)
        if ex_end_date:
            params['end_date'] = self._format_query_date_for_url(ex_end_date)
        if dividend_type:
            params['dividend_type'] = dividend_type

        return self._get_data(url_path, params)

    def get_stock_splits(self, security_symbols, split_start_date=None, split_end_date=None):
        security_symbols = self._str_or_list(security_symbols)

        url_path = self._build_url_path(security_symbols, 'splits')

        params = {}
        if split_start_date:
            params['start_date'] = self._format_query_date_for_url(split_start_date)
        if split_end_date:
            params['end_date'] = self._format_query_date_for_url(split_end_date)

        return self._get_data(url_path, params)

    def get_stock_spinoffs(self, security_symbols, spinoff_start_date=None, spinoff_end_date=None):
        security_symbols = self._str_or_list(security_symbols)

        url_path = self._build_url_path(security_symbols, 'spinoffs')

        params = {}
        if spinoff_start_date:
            params['start_date'] = self._format_query_date_for_url(spinoff_start_date)
        if spinoff_end_date:
            params['end_date'] = self._format_query_date_for_url(spinoff_end_date)

        return self._get_data(url_path, params)   

class MutualFundClient(BaseSecurityClient):
    
    SECURITY_TYPE_PATH = 'mutual_funds'
    VALID_SECURITY_FILTERS = ['attribute', 'benchmark_index', 'broad_asset_class', 'broad_category',
    	'category', 'domicile', 'fund_manager', 'fund_family', 'fund_style', 'legal_structure',
    	'prospectus_objective', 'share_class']

    def get_dividends(self, security_symbols, ex_start_date=None, ex_end_date=None, dividend_type=None):
        security_symbols = self._str_or_list(security_symbols)

        url_path = self._build_url_path(security_symbols, 'dividends')

        params = {}
        if ex_start_date:
            params['start_date'] = self._format_query_date_for_url(ex_start_date)
        if ex_end_date:
            params['end_date'] = self._format_query_date_for_url(ex_end_date)
        if dividend_type:
            params['dividend_type'] = dividend_type

        return self._get_data(url_path, params)  


class IndicatorClient(BaseSecurityClient):
    
    SECURITY_TYPE_PATH = 'indicators'
    VALID_SECURITY_FILTERS = ['category', 'region', 'report', 'source']

    def get_points(self, security_symbols, query_date=None):
        return super(IndicatorClient, self).get_points(security_symbols, None, query_date)

    def get_series(self, security_symbols, query_start_date=None, query_end_date=None,
        resample_frequency=None, resample_function=None, fill_method=None, aggregate_function=None):
        return super(IndicatorClient, self).get_series(security_symbols, None, query_start_date, query_end_date,
            resample_frequency, resample_function, fill_method, aggregate_function)
