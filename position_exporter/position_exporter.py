from prometheus_client import start_http_server, Summary, Gauge
import logging, requests, json, yaml
import os
import time
import sys

UPDATE_PERIOD = int(os.environ.get('UPDATE_INTERVAL'))

CURRENT_PRICE = Gauge('current_price',
                    'Current Position Price',
                    ['symbol', 'side', 'exchange', 'asset_class'])

LASTDAY_PRICE = Gauge('lastday_price',
                    'Last Closing Price',
                    ['symbol', 'side', 'exchange', 'asset_class'])

MARKET_VALUE = Gauge('market_value',
                    'Market Value of Securities',
                    ['symbol', 'side', 'exchange', 'asset_class'])

def main():
    start_http_server(int(os.environ.get('PORT')))

    while True:
        # call the alpaca API and get position data
        p = requests.get(POSITION_URL, headers=HEADERS)
        position_data = json.loads(p.content)
        for s in position_data:
            CURRENT_PRICE.labels(s['symbol'], s['side'], s['exchange'], s['asset_class']).set(s['current_price'])
            LASTDAY_PRICE.labels(s['symbol'], s['side'], s['exchange'], s['asset_class']).set(s['lastday_price'])
            MARKET_VALUE.labels(s['symbol'], s['side'], s['exchange'], s['asset_class']).set(s['market_value'])

        time.sleep(UPDATE_PERIOD)

if __name__ == '__main__':
    try:
        with open('config.yml') as f:
            config_data = yaml.safe_load(f)

            alpaca_data = config_data.get("alpaca", {})
            
            API_KEY = alpaca_data.get("API_KEY", "")
            SECRET_KEY = alpaca_data.get("SECRET_KEY", "")
            BASE_URL = alpaca_data.get("BASE_URL", "")

            ORDERS_URL = "{}/v2/orders".format(BASE_URL)
            ACCOUNT_URL = "{}/v2/account".format(BASE_URL)
            POSITION_URL = "{}/v2/positions".format(BASE_URL)
            HEADERS = {'APCA-API-KEY-ID': API_KEY, 'APCA-API-SECRET-KEY': SECRET_KEY}

            main()

    except Exception as e:
        print(e)
        sys.exit()