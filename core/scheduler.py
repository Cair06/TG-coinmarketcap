import asyncio
import logging
from database import check_thresholds


async def scheduled_check_thresholds(bot):
    while True:
        await check_thresholds(bot)
        await asyncio.sleep(120)  # Ждать 2 минуты
