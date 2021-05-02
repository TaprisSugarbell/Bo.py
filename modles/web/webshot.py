import os
import wget
import time
import requests
import urllib.parse
from telegram import ChatAction, ParseMode
from telegram.ext import ConversationHandler
try:
    from sample_config import Config
except:
    from config import Config

# Variables
input_webshot = 0

def webshot_callback(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text="Ingresa URL"
    )
    return input_webshot

def send_webshot(photo, urlp, chat):
    chat.send_action(
        action=ChatAction.UPLOAD_PHOTO,
        timeout=None
    )
    chat.send_document(
        caption=f"*WebShot Generada*\n*URL:* {urlp}",
        parse_mode=ParseMode.MARKDOWN_V2,
        document=open(photo, "rb")
    )

def input_webshot(update, context):
    chat = update.message.chat
    urll = context.args
    urlj = "".join(urll)

    screenshotapi = Config.screenshotapi
    url = urllib.parse.quote_plus(urlj)
    lnk = f"https://shot.screenshotapi.net/screenshot?token={screenshotapi}&url={url}"
    r = requests.get(lnk).json()
    photo = wget.download(r["screenshot"])
    urlp = r["url"]
    send_webshot(photo, urlp, chat)
    os.unlink(photo)
    return ConversationHandler.END


