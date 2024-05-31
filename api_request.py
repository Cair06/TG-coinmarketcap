"""
Not using in TG bot, just for test only request and type of data 
"""

import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ["CMC_API_KEY"]

# URL для запроса данных из CoinMarketCap API
url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

# Параметры запроса
parameters = {"start": "1", "limit": "5000", "convert": "USD"}

# Заголовки запроса, включая API ключ
headers = {
    "Accepts": "application/json",
    "X-CMC_PRO_API_KEY": api_key,
}

# Создание сессии и обновление заголовков
session = requests.Session()
session.headers.update(headers)

try:
    response = session.get(url, params=parameters)
    response.raise_for_status()
    data = response.json()

    # Условие для биткоина
    for crypto in data["data"]:
        if crypto["symbol"] == "BTC":
            price = crypto["quote"]["USD"]["price"]
            if price > 50000:
                print(f"Цена биткоина ({crypto['name']}) выше 50000 USD: {price}")
            elif price < 10000:
                print(f"Цена биткоина ({crypto['name']}) ниже 10000 USD: {price}")
            else:
                print(
                    f"Цена биткоина ({crypto['name']}) в диапазоне 10000-50000 USD: {price}"
                )

except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
except requests.exceptions.ConnectionError as conn_err:
    print(f"Connection error occurred: {conn_err}")
except requests.exceptions.Timeout as timeout_err:
    print(f"Timeout error occurred: {timeout_err}")
except requests.exceptions.RequestException as req_err:
    print(f"An error occurred: {req_err}")
