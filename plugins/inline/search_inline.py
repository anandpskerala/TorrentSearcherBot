from pyrogram import Client
from pyrogram.types import InlineQuery

from helpers.torrent import get_inline_torrents


@Client.on_inline_query()
async def torrent_via_inline(c: Client, m: InlineQuery):
    query = m.query
    results = await get_inline_torrents(query)
    await m.answer(
        results=results
    )
