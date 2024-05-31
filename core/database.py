import html
import aiosqlite
import logging
from utils import send_log_to_chat, get_crypto_data


async def init_db():
    async with aiosqlite.connect("thresholds.db") as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS thresholds (
                chat_id INTEGER,
                slug TEXT,
                min_value REAL,
                max_value REAL,
                PRIMARY KEY (chat_id, slug)
            )
            """
        )
        await db.commit()
    logging.info("Database initialized")


async def check_thresholds(bot):
    logging.info("Checking thresholds...")
    crypto_data = await get_crypto_data()
    async with aiosqlite.connect("thresholds.db") as db:
        async with db.execute(
            "SELECT chat_id, slug, min_value, max_value FROM thresholds"
        ) as cursor:
            async for row in cursor:
                chat_id, slug, min_value, max_value = row
                for crypto in crypto_data:
                    if crypto["slug"] == slug:
                        price = crypto["quote"]["USD"]["price"]
                        logging.info(
                            f"Checking {slug} price: {price} against min: {min_value}, max: {max_value}"
                        )

                        if max_value is not None and price >= max_value:
                            logging.info(
                                f"Price {price} is above max threshold {max_value}"
                            )
                            message = f"Цена {html.escape(crypto['name'])} ({html.escape(crypto['symbol'])}) достигла максимального порога {max_value} USD, цена на данный момент: {price:.2f}"
                            await bot.send_message(chat_id=chat_id, text=message)
                            await db.execute(
                                "DELETE FROM thresholds WHERE chat_id = ? AND slug = ? AND max_value = ?",
                                (chat_id, slug, max_value),
                            )
                            await db.commit()
                            logging.info(
                                f"Sent max threshold message for {slug} at {price}"
                            )
                        elif min_value is not None and price <= min_value:
                            logging.info(
                                f"Price {price} is below min threshold {min_value}"
                            )
                            message = f"Цена {html.escape(crypto['name'])} ({html.escape(crypto['symbol'])}) достигла минимального порога {min_value} USD, цена на данный момент: {price:.2f}"
                            await bot.send_message(chat_id=chat_id, text=message)
                            await db.execute(
                                "DELETE FROM thresholds WHERE chat_id = ? AND slug = ? AND min_value = ?",
                                (chat_id, slug, min_value),
                            )
                            await db.commit()
                            logging.info(
                                f"Sent min threshold message for {slug} at {price}"
                            )
                        else:
                            logging.info(
                                f"Price {price} is within the thresholds for {slug}"
                            )
