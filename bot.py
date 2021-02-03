import logging

from pyrogram import Client

from config import API_ID, API_HASH, TOKEN

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logging.getLogger(__name__)


client = Client(
    "TorrentSearcherBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=TOKEN,
    workers=200,
    parse_mode="html",
    plugins=dict(
        root="plugins"
    )
)

if __name__ == '__main__':
    client.run()
