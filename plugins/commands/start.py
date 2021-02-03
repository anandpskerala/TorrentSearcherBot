from pyrogram import Client, filters
from pyrogram.types import Message

from config import START_MESSAGE


@Client.on_message(filters.command("start"))
async def start_message(c: Client, m: Message):
    await m.reply_text(START_MESSAGE, reply_to_message_id=m.message_id)
