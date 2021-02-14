from prometheus_client import start_http_server, Summary, Gauge
import logging, requests, json, yaml
import os
import time
import sys

UPDATE_PERIOD = int(os.environ.get('UPDATE_INTERVAL'))

BALANCE = Gauge('balance',
                    'Hold current account balances',
                    ['balance_type'])

def main():
    start_http_server(int(os.environ.get('PORT')))

    while True:
        # call the alpaca API and get account data
        a = requests.get(ACCOUNT_URL, headers=HEADERS)
        account_data = json.loads(a.content)

        equity = float(account_data['last_equity'])
        cash = float(account_data['buying_power'])

        BALANCE.labels('EQUITY').set(equity)
        BALANCE.labels('BUYING_POWER').set(cash)
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