import os

TOKEN = os.environ.get("BOT_TOKEN")
START_MESSAGE = os.environ.get("START_MESSAGE", "*Hi ! I am a simple torrent searcher using @sjprojects's Torrent Searcher api.\n\n\nMade with 🐍 by @KeralasBots*")
FOOTER_TEXT = os.environ.get("FOOTER_TEXT", "*Made with ❤️ by @KeralasBots*")