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


def danbooru_callback(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text="Ingresa URL"
    )
    return Input


def send_pic(post, files, chat, context):
    chatuser = chat["id"]
    caption = caption_text(post)
    inline = inline_test(post)
    if chatuser == IDuser:
        channel_send(files, caption, inline, chat, context)
    elif chatuser != IDuser:
        chat_send(files, caption, inline, chat)


def input_danbooru(update, context):
    chat = update.message.chat
    post = danboo_show(context.args[0])

    file = download_booru(post["id"])
    # Reduciendo Tamaño
    filejpg = filejpeg(file)
    # Datos/Envío
    files = file, filejpg
    send_pic(post, files, chat, context)
    os.unlink(file)
    os.unlink(filejpg)
    return ConversationHandler.END

