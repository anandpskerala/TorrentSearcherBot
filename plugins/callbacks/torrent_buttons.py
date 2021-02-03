import html

from pyrogram import Client
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiohttp.client_exceptions import ContentTypeError

from config import TORRENTS, FOOTER_TEXT
from helpers.torrent import torrent_search


@Client.on_callback_query()
async def torrent_buttons(c: Client, m: CallbackQuery):
    query = m.data
    if query is None or len(query) == 0:
        return
    try:
        await m.message.edit("Fetching torrent Info")
        torrents = TORRENTS[m.message.message_id]
        torrent_name = None
        for torrent in torrents:
            name = torrent.get(query)
            if name is not None:
                torrent_name = name
        response = await torrent_search(torrent_name)
        name = html.escape(response[0].get("name"))
        age = html.escape(response[0].get("age"))
        leechers = response[0].get("leecher")
        magnet_link = html.escape(response[0].get("magnet"))
        seeders = response[0].get("seeder")
        size = html.escape(response[0].get("size"))
        type_of_file = html.escape(response[0].get("type"))
        site = html.escape(response[0].get("site"))
        torrent_url = html.escape(response[0].get("url"))
        text = f"<b>Name : {name}\nSize : {size}\nAge : {age}\nLeechers : {leechers}\nNo: of seeds : {seeders}"\
               f"\nType of File : {type_of_file}\nTorrent Url : {torrent_url}</b>\n\n<b>Magnet Link :</b> <code>{magnet_link}</code>" \
               f"\n\n<b>Powered by {site} website</b>\n\n{FOOTER_TEXT}"
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Try InlineQuery", switch_inline_query_current_chat=""),
                    InlineKeyboardButton("Search in another chat", switch_inline_query="")
                ]
            ]
        )
        await m.message.edit(
            text=text,
            reply_markup=keyboard
        )
    except KeyError:
        await m.answer("Request Timeout. Try again", show_alert=True)

    except IndexError:
        await m.answer("Something went Wrong", show_alert=True)

    except ContentTypeError:
        await m.answer("Cannot fetch the content of the torrent", show_alert=True)
