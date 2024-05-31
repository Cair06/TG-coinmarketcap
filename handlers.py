import html
from aiogram import Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import aiosqlite
import logging


async def command_start_handler(message: Message) -> None:
    user_name = html.escape(message.from_user.full_name)
    start_message = f"Hello, <b>{user_name}</b>!\nUse /set &lt;SYMBOL&gt; [min:&lt;MIN_VALUE&gt;] [max:&lt;MAX_VALUE&gt;] to set a price threshold."
    await message.answer(start_message)


async def set_threshold(message: Message):
    try:
        parts = message.text.split()
        if len(parts) < 2:
            raise ValueError

        symbol = parts[1].upper()
        min_value = None
        max_value = None

        for part in parts[2:]:
            if part.startswith("min:"):
                min_value = float(part.split(":")[1])
            elif part.startswith("max:"):
                max_value = float(part.split(":")[1])

        async with aiosqlite.connect("thresholds.db") as db:
            await db.execute(
                "INSERT OR REPLACE INTO thresholds (chat_id, symbol, min_value, max_value) VALUES (?, ?, ?, ?)",
                (message.chat.id, symbol, min_value, max_value),
            )
            await db.commit()
        await message.answer(
            f"Thresholds set for {html.escape(symbol)}: min {min_value if min_value is not None else 'None'} USD, max {max_value if max_value is not None else 'None'} USD"
        )
        logging.info(f"Thresholds set for {symbol}: min {min_value}, max {max_value}")
    except ValueError:
        await message.answer("Usage: /set <SYMBOL> [min:<MIN_VALUE>] [max:<MAX_VALUE>]")


def register_handlers(dp: Dispatcher):
    dp.message.register(command_start_handler, CommandStart())
    dp.message.register(set_threshold, Command(commands=["set"]))
