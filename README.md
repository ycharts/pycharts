# pycharts
Python client for the YCharts Market Data API.

# Requirements

* Python ( 3.x )
* Valid API key from YCharts.

# Installation

Install from github using `pip`.

```
pip install git+https://github.com/ycharts/pycharts.git
# or
pip install pycharts
```
# Documentation and Support

Full [API documentation](https://www.ycharts.com/api/docs/) can be found at https://www.ycharts.com/api/docs/.

For questions and information about API access, visit [YCharts](https://ycharts.com/api) or email us (sales@ycharts.com) for more info.

# Examples
Below are some examples to get started with using the Python Client.

- [Setup](#setup)
- [Discovery Queries](#discovery-queries)
- [Data Point Queries](#data-point-queries)
- [Data Series Queries](#data-series-queries)
- [Info Queries](#info-queries)
- [Dividend Queries](#dividend-queries)
- [Stock Split and Spinoff Queries](#stock-split-and-spinoff-queries)
- [Exceptions](#exceptions)

### Setup

```python
from pycharts import CompanyClient, IndicatorClient, MutualFundClient

ycharts_api_key = 'sample-api-key'

company_client = CompanyClient(ycharts_api_key)
mutual_fund_client = MutualFundClient(ycharts_api_key)
indicator_client = IndicatorClient(ycharts_api_key)

```

### Discovery Queries
Gets a paginated list of companies, mutual funds or indicators.
  - [Company Filters](http://ycharts.com/api/docs/companies/company_search.html)
  - [Mutual Fund Filters](http://ycharts.com/api/docs/mutual_funds/mutual_fund_search.html)
  - [Indicator Filters](http://ycharts.com/api/docs/indicators/indicator_search.html)
```python
companies = company_client.get_securities(exchange='NYSE')
mutual_funds = mutual_fund_client.get_securities(category='Technology')
indicators = indicator_client.get_securities(region='USA')
```

### Data Point Queries
Get a single date-value pair of data from one or more securities for one or more calculations. It takes an optional date parameter and will return the latest value before the requested date.
  - [Company Data Point](http://ycharts.com/api/docs/companies/company_data_point.html)
  - [Mutual Fund Data Point](http://ycharts.com/api/docs/mutual_funds/mutual_fund_data_point.html)
  - [Indicator Data Point](http://ycharts.com/api/docs/indicators/indicator_data_point.html)
```python
# Queries the latest price values for AAPL and MSFT
point_rsp = company_client.get_points(['AAPL', 'MSFT'], ['price'])
# Queries the latest net asset value for M:FCNTX
point_rsp = mutual_fund_client.get_points('M:FCNTX', ['net_asset_value'])
# Queries the latest value for I:USICUI
point_rsp = indicator_client.get_points('I:USICUI')

# Queries the price values for AAPL 21 days ago
previous_point_rsp = company_client.get_points('AAPL', 'price', query_date=-21)
# Queries the net asset value for M:FCNTXPL 21 days ago
twenty_one_days_ago = datetime.datetime.now() - datetime.timedelta(days=21)
previous_point_rsp = mutual_fund_client.get_points('M:FCNTX', ['net_asset_value'], 
    query_date=twenty_one_days_ago)
# Queries the value for I:USICUI 21 days ago
previous_point_rsp = indicator_client.get_points('I:USICUI', query_date=-31)
```

### Data Series Queries
Get a series of date-value pairs of data from one or more securities for one or more calculations. It takes optional start_date and end_date parameters and will return all values between the requested dates.
  - [Company Data Series](http://ycharts.com/api/docs/companies/company_data_series.html)
  - [Mutual Fund Data Series](http://ycharts.com/api/docs/mutual_funds/mutual_fund_data_series.html)
  - [Indicator Data Series](http://ycharts.com/api/docs/indicators/indicator_data_series.html)
```python
now = datetime.datetime.now()
past = now - datetime.timedelta(days=100)

series_rsp = company_client.get_series(['AAPL', 'MSFT'], ['price'],
    query_start_date=past , query_end_date=now)
    
series_rsp = mutual_fund_client.get_series('M:FCNTX', ['net_asset_value'], 
    query_start_date=past , query_end_date=now)
    
series_rsp = indicator_client.get_series('I:USICUI',
    query_start_date=past , query_end_date=now)

# example resampling request
series_rsp = company_client.get_series(['AAPL', 'MSFT'], ['price'], query_start_date=past, 
    query_end_date=now, resampling_frequency='daily', resampling_function='mean')
```

### Info Queries
Get information about one or more securities.
  - [Company Info](http://ycharts.com/api/docs/companies/company_info_fields.html)
  - [Mutual Fund Info](http://ycharts.com/api/docs/mutual_funds/mutual_fund_info_fields.html)
  - [Indicator Info](http://ycharts.com/api/docs/indicators/indicator_info_fields.html)
```python
info_rsp = company_client.get_info(['AAPL', 'MSFT'], ['description'])
info_rsp = mutual_fund_client.get_info('M:FCNTX', ['inception_date', 'broad_asset_class'])
info_rsp = indicator_client.get_info('I:USICUI', ['next_release'])
```

### Dividend Queries
Get dividends from one or more companies or mutual funds.
  - [Company Dividend](http://ycharts.com/api/docs/companies/company_dividends.html)
  - [Mutual Fund Dividend](http://ycharts.com/api/docs/mutual_funds/mutual_fund_dividends.html)
```python
start_date = datetime.datetime(2015, 1, 1)

dividend_rsp = company_client.get_dividends(['AAPL', 'MSFT'], ex_start_date=start_date, 
    dividend_type='special')
dividend_rsp = mutual_fund_client.get_dividends('M:FCNTX', ex_start_date=start_date)
```

### Stock Split and Spinoff Queries
Get a list of stock split/spinoff objects that within the date range specified by the optional start and end date parameters.
  - [Company Stock Split](http://ycharts.com/api/docs/companies/company_splits.html)
  - [Company Spinoffs](http://ycharts.com/api/docs/companies/company_spinoffs.html)
```python
split_spinoff_end_date = datetime.datetime(2014, 1, 1)
split_rsp = company_client.get_stock_splits(['AAPL'], split_end_date=split_spinoff_end_date)
spinoff_rsp = company_client.get_stock_spinoffs(['AAPL'], spinoff_end_date=split_spinoff_end_date)
```

### Exceptions
```python
# More exception classes in pycharts/exceptions.py
from pycharts import exceptions


try:
    bad_point_rsp = company_client.get_points(['AAPL'], ['price'], query_date=45)
except exceptions.PyChartsRequestException as pycharts_error:
    print(pycharts_error.error_message)

```
