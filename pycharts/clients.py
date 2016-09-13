from pycharts.base import BaseSecurityClient


class CompanyClient(BaseSecurityClient):
    
    SECURITY_TYPE_PATH = 'companies'


class MutualFundClient(BaseSecurityClient):
    
    SECURITY_TYPE_PATH = 'mutual_funds'


class IndicatorClient(BaseSecurityClient):
    
    SECURITY_TYPE_PATH = 'indicators'

    def get_points(self, security_symbols, query_date=None):
        return super().get_points(security_symbols, None, query_date)

    def get_series(self, security_symbols, query_start_date=None, query_end_date=None):
        return super().get_series(security_symbols, None, query_start_date, query_end_date)
