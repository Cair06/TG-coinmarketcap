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
                symbol TEXT,
                min_value REAL,
                max_value REAL,
                PRIMARY KEY (chat_id, symbol)
            )
            """
        )
        await db.commit()
    logging.info("Database initialized")


async def check_thresholds():
    logging.info("Checking thresholds...")
    crypto_data = await get_crypto_data()
    async with aiosqlite.connect("thresholds.db") as db:
        async with db.execute(
            "SELECT chat_id, symbol, min_value, max_value FROM thresholds"
        ) as cursor:
            async for row in cursor:
                chat_id, symbol, min_value, max_value = row
                for crypto in crypto_data:
                    if crypto["symbol"] == symbol:
                        price = crypto["quote"]["USD"]["price"]
                        logging.info(
                            f"Checking {symbol} price: {price} against min: {min_value}, max: {max_value}"
                        )
                        if max_value is not None and price >= max_value:
                            message = f"Цена {html.escape(crypto['name'])} ({html.escape(crypto['symbol'])}) достигла максимального порога {max_value} USD, цена на данный момент: {int(price)}"
                            await send_log_to_chat(message, chat_id)
                            await db.execute(
                                "DELETE FROM thresholds WHERE chat_id = ? AND symbol = ? AND max_value = ?",
                                (chat_id, symbol, max_value),
                            )
                            await db.commit()
                            logging.info(
                                f"Sent max threshold message for {symbol} at {price}"
                            )
                        elif min_value is not None and price <= min_value:
                            message = f"Цена {html.escape(crypto['name'])} ({html.escape(crypto['symbol'])}) достигла минимального порога {min_value} USD, цена на данный момент: {int(price)}"
                            await send_log_to_chat(message, chat_id)
                            await db.execute(
                                "DELETE FROM thresholds WHERE chat_id = ? AND symbol = ? AND min_value = ?",
                                (chat_id, symbol, min_value),
                            )
                            await db.commit()
                            logging.info(
                                f"Sent min threshold message for {symbol} at {price}"
                            )
