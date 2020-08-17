from telegram.ext import (
    Updater, 
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackQueryHandler,
    InlineQueryHandler
)
from commands.commands import start, torrent
from inline.inline import button, inlinequery
from config import TOKEN


import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

logger = logging.getLogger(__name__)


#def _error(update, context):
    #logger.error('Update "%s" caused error "%s"', update, context.error)



def main():
    updater = Updater(token=TOKEN,use_context=True, workers=8)
    logger.info(f"SUCESSFULLY STARTED THE BOT IN {updater.bot.username}")
    start_handler = CommandHandler('start', start)
    torrent_handler = MessageHandler(Filters.text, torrent)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(torrent_handler)
    dispatcher.add_handler(CallbackQueryHandler(button))
    dispatcher.add_handler(InlineQueryHandler(inlinequery))
    #dispatcher.add_error_handler(_error)
    updater.start_polling()
    updater.idle()
    updater.stop()

if __name__ == "__main__":
    main()

