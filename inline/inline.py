from uuid import uuid4
from telegram import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    InlineQueryResultArticle,
    InputTextMessageContent
)
from config import FOOTER_TEXT

from helpers.torrent import torrent_search

def inlinequery(update, context):
    """Handles the inline query."""
    query = update.inline_query.query
    buttons = [[InlineKeyboardButton(text="Search Again", switch_inline_query_current_chat="")]]
    if len(query) == 0:
        results = [InlineQueryResultArticle(
            id=uuid4(),
            title="Search any keyword",
            input_message_content=InputTextMessageContent(
                f"*Search any torrent\nExample : *`Avengers`\n\n{FOOTER_TEXT}", 
                parse_mode="Markdown"
                ),
            reply_markup=InlineKeyboardMarkup(buttons)
            )
        ]

        context.bot.answer_inline_query(update.inline_query.id, results=results)
        return 
    print(len(query))
    torrent = torrent_search(query)
    results = []
    
    if torrent == None:
        results.append(InlineQueryResultArticle(
            id=uuid4(),
            title="Search any keyword",
            input_message_content=InputTextMessageContent(
                f"*Search any torrent\nExample : *`Avengers`\n\n{FOOTER_TEXT}", 
                parse_mode="Markdown"
                ),
            reply_markup=InlineKeyboardMarkup(buttons)
            )
        )
        context.bot.answer_inline_query(update.inline_query.id, results=results)
        return

    if len(torrent) == 0:
        results.append(InlineQueryResultArticle(
            id=uuid4(),
            title="404 Not Found",
            input_message_content=InputTextMessageContent(
                f"*Sorry there is no results for your query {query}*\n\n{FOOTER_TEXT}", 
                parse_mode="Markdown"
                ),
            reply_markup=InlineKeyboardMarkup(buttons)
            )
        )
        context.bot.answer_inline_query(update.inline_query.id, results=results)
        return


    for response in torrent[:15]:
        name = response.get("name")
        age = response.get("age")
        leechers = response.get("leecher")
        magnet_link = response.get("magnet")
        seeders = response.get("seeder")
        size = response.get("size")
        type_of_file = response.get("type")
        site = response.get("site")
        torrent_url = response.get("url")
        results.append(InlineQueryResultArticle(
            id=uuid4(),
            title=name,
            input_message_content=InputTextMessageContent(
                f"*Name : {name}\nSize : {size}\nAge : {age}\nLeechers : {leechers}\nNo: of seeds : {seeders}\nType of File : {type_of_file}\nTorrent Url : {torrent_url}*\n\n*Magnet Link : *`{magnet_link}`\n\n*Powered by {site} website*\n\n{FOOTER_TEXT}", 
                parse_mode="Markdown"
                ),
            reply_markup=InlineKeyboardMarkup(buttons)
            )
        )

    context.bot.answer_inline_query(update.inline_query.id, results=results)

def button(update, context):
    query = update.callback_query
    query.answer()
    torrent_name = query.data
    query.edit_message_text(text="Just a moment adding some final touch")
    if torrent_name == None:
        query.edit_message_text(text="Something went wrong")
        return
    response = torrent_search(torrent_name)
    if response == None:
        query.edit_message_text(text="Something went wrong")
        return
    if len(response) == 0:
        query.edit_message_text(text="Something went wrong")
        return

    
    
    
    name = response[0].get("name")
    age = response[0].get("age")
    leechers = response[0].get("leecher")
    magnet_link = response[0].get("magnet")
    seeders = response[0].get("seeder")
    size = response[0].get("size")
    type_of_file = response[0].get("type")
    site = response[0].get("site")
    torrent_url = response[0].get("url")
    buttons = [[InlineKeyboardButton(text="Try InlineQuery", switch_inline_query="")]]

    query.edit_message_text(text=f"*Name : {name}\nSize : {size}\nAge : {age}\nLeechers : {leechers}\nNo: of seeds : {seeders}\nType of File : {type_of_file}\nTorrent Url : {torrent_url}*\n\n*Magnet Link : *`{magnet_link}`\n\n*Powered by {site} website*\n\n{FOOTER_TEXT}", parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(buttons))


