import os
import re
import wget
import logging
import requests
from PIL import Image
from modles.booru import *
from pybooru import Danbooru
from telegram.ext import ConversationHandler
from telegram import ChatAction, ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
try:
    from sample_config import Config
except:
    from config import Config

# Variables
Input = 0
# logging.basicConfig(filename="app.log", level="DEBUG")

def danbooru_callback(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text="Ingresa URL"
    )
    return Input


def send_pic(post, chat):
    inline = inline_test(post)
    caption = caption_preview(post)
    send_preview(caption, inline, chat)


def input_danbooru(update, context):
    chat = update.message.chat
    # Variables de booru
    post = danboo_show(context.args[0])
    # Datos Envío
    send_pic(post, chat)
    return ConversationHandler.END
