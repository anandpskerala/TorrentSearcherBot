import html
import uuid
import aiohttp
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, \
    InlineQueryResultArticle, InputTextMessageContent
from config import TORRENTS, FOOTER_TEXT
from aiohttp.client_exceptions import ContentTypeError


async def torrent_search(torrent_name):
    base_url = f"https://api.sumanjay.cf/torrent/?query={torrent_name}"
    response = None
    try:
        async with aiohttp.ClientSession() as request:
            async with request.get(base_url) as result:
                if result.status == 200:
                    response = await result.json()
    except ContentTypeError:
        response = None
    return response


async def get_torrent_buttons(m: Message, status: Message):
    torrent_name = m.text
    message_id = status.message_id
    torrents = await torrent_search(torrent_name)
    if torrents is None or len(torrents) == 0:
        await status.edit("No results found")
        return None
    half_torrent = torrents[:8]
    keyboard = []
    torrent_list = []
    for torrent in half_torrent:
        torrent_id = str(uuid.uuid4())[:6]
        single_torrent = torrent.get("name")
        keyboard.append([InlineKeyboardButton(single_torrent, callback_data=f"{torrent_id}")])
        torrent_list.append({torrent_id: single_torrent})
    TORRENTS[message_id] = torrent_list

    return InlineKeyboardMarkup(keyboard)


async def get_inline_torrents(query):
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Search Again", switch_inline_query_current_chat="")
            ]
        ]
    )
    if len(query) == 0:
        result = [
            InlineQueryResultArticle(
                "Search any keyword",
                input_message_content=InputTextMessageContent(
                    message_text=f"<b>Search any torrent\nExample :</b> <code>Avengers</code>\n\n{FOOTER_TEXT}"
                ),
                reply_markup=keyboard,
                thumb_url="https://previews.123rf.com/images/fokaspokas/fokaspokas1808/fokaspokas180801753/111837514-loupe-search-or-magnifying-linear-icon-thin-outline-neon-style-light-decoration-icon-bright-electric.jpg"
            )
        ]
    else:
        result = []
        get_torrent = await torrent_search(query)
        if get_torrent is None or len(get_torrent) == 0:
            result.append(
                InlineQueryResultArticle(
                    title="404 Not Found",
                    input_message_content=InputTextMessageContent(
                        message_text=f"<b>Sorry there is no results for your query {query}</b>\n\n{FOOTER_TEXT}"
                    ),
                    reply_markup=keyboard,
                    thumb_url="https://cdn4.iconfinder.com/data/icons/web-design-and-development-8-2/128/390-512.png"
                )
            )
        else:
            for response in get_torrent[:8]:
                name = html.escape(response.get("name"))
                age = html.escape(response.get("age"))
                leechers = response.get("leecher")
                magnet_link = html.escape(response.get("magnet"))
                seeders = response.get("seeder")
                size = html.escape(response.get("size"))
                type_of_file = html.escape(response.get("type"))
                site = html.escape(response.get("site"))
                torrent_url = html.escape(response.get("url"))
                last_txt = f"<b>Name : {name}\nSize : {size}\nAge : {age}\nLeechers : {leechers}\n" \
                           f"No: of seeds : {seeders}\nType of File : {type_of_file}\nTorrent Url : {torrent_url}</b>" \
                           f"\n\n<b>Magnet Link :</b> <code>{magnet_link}</code>\n\n<b>Powered by {site} website</b>" \
                           f"\n\n{FOOTER_TEXT}"

                result.append(
                    InlineQueryResultArticle(
                        title=name,
                        input_message_content=InputTextMessageContent(
                            message_text=last_txt,
                            disable_web_page_preview=True
                        ),
                        reply_markup=keyboard,
                        thumb_url="https://telegra.ph/file/ea46b9708660e11a62513.jpg"
                    )
                )
    return result
