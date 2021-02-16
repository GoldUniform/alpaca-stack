from prometheus_client import start_http_server, Summary, Gauge
import alpaca_trade_api as tradeapi
import logging, requests, json, yaml
import os
import time
import sys

UPDATE_PERIOD = int(os.environ.get('UPDATE_INTERVAL'))

CURRENT_PRICE = Gauge('current_price',
                    'Current Position Price',
                    ['symbol', 'side', 'exchange', 'asset_class', 'sector'])

LASTDAY_PRICE = Gauge('lastday_price',
                    'Last Closing Price',
                    ['symbol', 'side', 'exchange', 'asset_class', 'sector'])

MARKET_VALUE = Gauge('market_value',
                    'Market Value of positions',
                    ['symbol', 'side', 'exchange', 'asset_class', 'sector'])

UNREALIZED_PL = Gauge('unrealized_pl',
                    'Unrealized Profit/Loss',
                    ['symbol', 'side', 'exchange', 'asset_class', 'sector'])

QTY = Gauge('qty',
                    'Quantity of this position',
                    ['symbol', 'side', 'exchange', 'asset_class', 'sector'])
        
AVG_ENTRY_PRICE = Gauge('avg_entry_price',
                    'Average Entry of this position',
                    ['symbol', 'side', 'exchange', 'asset_class', 'sector'])

CHANGE_TODAY = Gauge('change_today',
                    'Change of price since todays open',
                    ['symbol', 'side', 'exchange', 'asset_class', 'sector'])

def main():
    start_http_server(int(os.environ.get('PORT')))

    api = tradeapi.REST(API_KEY, SECRET_KEY, base_url=BASE_URL)
    
    while True:
        position_data = api.list_positions()
        for s in position_data:
            company_info = api.polygon.company(s.symbol)
            if hasattr(company_info, 'sector'):
                sector = company_info.sector
            else:
                sector = 'None'

            CURRENT_PRICE.labels(s.symbol, s.side, s.exchange, s.asset_class, sector).set(s.current_price)
            LASTDAY_PRICE.labels(s.symbol, s.side, s.exchange, s.asset_class, sector).set(s.lastday_price)
            MARKET_VALUE.labels(s.symbol, s.side, s.exchange, s.asset_class, sector).set(s.market_value)
            UNREALIZED_PL.labels(s.symbol, s.side, s.exchange, s.asset_class, sector).set(s.unrealized_pl)
            QTY.labels(s.symbol, s.side, s.exchange, s.asset_class, sector).set(s.qty)
            AVG_ENTRY_PRICE.labels(s.symbol, s.side, s.exchange, s.asset_class, sector).set(s.avg_entry_price)
            CHANGE_TODAY.labels(s.symbol, s.side, s.exchange, s.asset_class, sector).set(s.change_today)

        time.sleep(UPDATE_PERIOD)

if __name__ == '__main__':
    try:
        with open('config.yml') as f:
            config_data = yaml.safe_load(f)

            alpaca_data = config_data.get("alpaca", {})
            
            API_KEY = alpaca_data.get("API_KEY", "")
            SECRET_KEY = alpaca_data.get("SECRET_KEY", "")
            BASE_URL = alpaca_data.get("BASE_URL", "")

            main()

    except Exception as e:
        print(e)
        sys.exit()