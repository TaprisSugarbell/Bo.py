import os
from modles.booru import *
from telegram.ext import ConversationHandler
try:
    from sample_config import Config
except:
    from config import Config

# Variables
Input = 0
IDuser = int(Config.chatuser)


def konachan_callback(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text="Ingresa URL"
    )
    return Input


def send_pic(post, files, chat, context):
    chatuser = chat["id"]
    caption = caption_kona(post)
    inline = inline_kona(post)
    if chatuser == IDuser:
        channel_kona(files, caption, inline, chat, context)
    elif chatuser != IDuser:
        chat_kona(files, caption, inline, chat)


def input_konachan(update, context):
    chat = update.message.chat
    post = kona_show(context.args[0])

    file = download_kona(post["id"])
    # Reduciendo Tamaño
    filejpg = filejpeg(file)
    # Datos/Envío
    files = file, filejpg
    send_pic(post, files, chat, context)
    os.unlink(file)
    os.unlink(filejpg)
    return ConversationHandler.END









