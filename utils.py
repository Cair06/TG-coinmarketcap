import os
import requests
import psutil
import logging
from aiogram import Bot

TOKEN = os.environ["BOT_TOKEN"]
LOG_CHAT_ID = os.environ["LOG_CHAT_ID"]
bot = Bot(token=TOKEN)

# Настройки CoinMarketCap API
url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
headers = {
    "Accepts": "application/json",
    "X-CMC_PRO_API_KEY": os.environ["CMC_API_KEY"],
}


async def send_log_to_chat(log_message, chat_id=LOG_CHAT_ID):
    await bot.send_message(chat_id=chat_id, text=log_message)


def get_system_stats():
    cpu_usage = psutil.cpu_percent()
    memory_info = psutil.virtual_memory()
    disk_info = psutil.disk_usage("/")

    return f"CPU Usage: {cpu_usage}%\nMemory: {memory_info.percent}% used\nDisk: {disk_info.percent}% used"


async def send_system_stats():
    stats = get_system_stats()
    await send_log_to_chat(stats)


async def get_crypto_data():
    parameters = {"start": "1", "limit": "5000", "convert": "USD"}
    session = requests.Session()
    session.headers.update(headers)
    try:
        response = session.get(url, params=parameters)
        response.raise_for_status()
        data = response.json()
        logging.info("Fetched crypto data")
        return data["data"]
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching data: {e}")
        return []
