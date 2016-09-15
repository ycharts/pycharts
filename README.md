# pycharts
Python client for the YCharts API.

# Requirements

* Python (2.7, 3.0, 3.2, 3.3, 3.4, 3.5)
* Valid API key from YCharts Support.

# Installation

Install from github using `pip`.

```
pip install git+https://github.com/ycharts/pycharts.git
```

# Examples

```python
import datetime

# Other clients include MutualFundClient and IndicatorClient
from pycharts import CompanyClient 
# More exception classes in pycharts/exceptions.py
from pycharts import exceptions


ycharts_api_key = 'sample-api-key'
company_client = CompanyClient(ycharts_api_key)

# POINT QUERIES

# queries the latest price values for AAPL and MSFT
point_rsp = company_client.get_points(['AAPL', 'MSFT'], ['price'])

# queries the price values for AAPL and MSFT 21  days ago
previous_point_rsp = company_client.get_points(['MSFT'], ['price'], query_date=-21)

# SERIES QUERIES

now = datetime.datetime.now()
past = now - datetime.timedelta(days=100)
series_rsp = company_client.get_series(['AAPL', 'MSFT'], ['price'],
    query_start_date=past , query_end_date=now)

# INFO QUERIES

info_rsp = company_client.get_info(['AAPL'], ['description'])

# EXCEPTION EXAMPLE

try:
    bad_point_rsp = company_client.get_points(['AAPL'], ['price'], query_date=45)
except exceptions.PyChartsRequestException as pycharts_error:
    print(pycharts_error.error_message)

```

# Documentation and Support

Full api documentation can be found at https://www.ycharts.com/api.

For questions and information about api access, visit https://ycharts.com/support for more info.
