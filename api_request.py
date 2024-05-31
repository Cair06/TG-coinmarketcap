"""
Not using in TG bot, just for test only request and type of data 
"""

import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Укажите ваш API ключ здесь
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
    # Выполнение запроса
    response = session.get(url, params=parameters)
    # Проверка на успешный ответ
    response.raise_for_status()
    # Обработка данных
    data = response.json()
    print(json.dumps(data, indent=4))
except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
except requests.exceptions.ConnectionError as conn_err:
    print(f"Connection error occurred: {conn_err}")
except requests.exceptions.Timeout as timeout_err:
    print(f"Timeout error occurred: {timeout_err}")
except requests.exceptions.RequestException as req_err:
    print(f"An error occurred: {req_err}")
