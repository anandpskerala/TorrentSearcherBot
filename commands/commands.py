from telegram.ext import CallbackContext

from telegram import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    Update
)

from config import START_MESSAGE

from helpers.torrent import torrent_search

def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=START_MESSAGE, parse_mode="Markdown")

def torrent(update: Update, content: CallbackContext):
    if update.message.via_bot != None:
        return
    search_message = content.bot.send_message(chat_id=update.effective_chat.id, text="Searching your torrent file")
    torrent_name = update.effective_message.text
    response = torrent_search(torrent_name)
    if len(response) == 0:
        content.bot.edit_message_text(chat_id=update.effective_chat.id, message_id=search_message.message_id, text="No results found")
        return


    half_list = response[:15]
    inline_keyboard = []
    for split_list in half_list:
        single_torrent_name = split_list.get("name")
        inline_keyboard.append([InlineKeyboardButton(single_torrent_name, callback_data=f"{single_torrent_name}")])
    
    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    content.bot.edit_message_text(chat_id=update.effective_chat.id, message_id=search_message.message_id, text=f"Got the following results for your query *{torrent_name}*. Select the preffered type from the below options", parse_mode="Markdown", reply_markup=reply_markup)
