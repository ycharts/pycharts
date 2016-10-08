from pycharts.base import BaseSecurityClient


class CompanyClient(BaseSecurityClient):
    
    SECURITY_TYPE_PATH = 'companies'
    VALID_SECURITY_FILTERS = ['benchmark_index', 'exchange', 'hq_region', 'incorporation_region',
    	'industry', 'naics_industry', 'naics_sector', 'sector']


class MutualFundClient(BaseSecurityClient):
    
    SECURITY_TYPE_PATH = 'mutual_funds'
    VALID_SECURITY_FILTERS = ['attribute', 'benchmark_index', 'broad_asset_class', 'broad_category',
    	'category', 'domicile', 'fund_manager', 'fund_family', 'fund_style', 'legal_structure',
    	'prospectus_objective', 'share_class']


class IndicatorClient(BaseSecurityClient):
    
    SECURITY_TYPE_PATH = 'indicators'
    VALID_SECURITY_FILTERS = ['category', 'region', 'report', 'source']

    def get_points(self, security_symbols, query_date=None):
        return super(IndicatorClient, self).get_points(security_symbols, None, query_date)

    def get_series(self, security_symbols, query_start_date=None, query_end_date=None):
        return super(IndicatorClient, self).get_series(security_symbols, None, query_start_date, query_end_date)
