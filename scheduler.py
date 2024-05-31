import asyncio
import logging
from database import check_thresholds
from utils import send_system_stats


async def scheduled_check_thresholds():
    while True:
        await check_thresholds()
        await asyncio.sleep(120)  # Ждать 2 минуты


async def scheduled_send_system_stats():
    while True:
        await send_system_stats()
        await asyncio.sleep(43200)  # Ждать 12 часов (2 раза в день)
