from pycharts.base import BaseSecurityClient


class CompanyClient(BaseSecurityClient):
    
    SECURITY_TYPE_PATH = 'companies'
    VALID_SECURITY_FILTERS = ['exchange', 'benchmark_index', 'sector', 'industry',
    	'naics_sector', 'naics_industry', 'hq_region', 'incorporation_region']


class MutualFundClient(BaseSecurityClient):
    
    SECURITY_TYPE_PATH = 'mutual_funds'
    VALID_SECURITY_FILTERS = ['fund_style', 'broad_asset_class', 'broad_category', 'category',
    	'prospectus_objective', 'domicile', 'benchmark_index', 'fund_manager', 'fund_family',
    	'brokerage_availability', 'attribute', 'legal_structure', 'share_class']


class IndicatorClient(BaseSecurityClient):
    
    SECURITY_TYPE_PATH = 'indicators'
    VALID_SECURITY_FILTERS = ['region', 'category', 'source', 'report']

    def get_points(self, security_symbols, query_date=None):
        return super(IndicatorClient, self).get_points(security_symbols, None, query_date)

    def get_series(self, security_symbols, query_start_date=None, query_end_date=None):
        return super(IndicatorClient, self).get_series(security_symbols, None, query_start_date, query_end_date)
