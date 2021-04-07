import os
import pytube
import threading
from queue import Queue
from datetime import datetime
from telegram import ChatAction
from telegram.ext import ConversationHandler

# Variables
INPUTpy = 0

def pytbcommand(update, context):
    update.message.reply_text('Enviame link para descargar video')
    return INPUTpy

def pytb_callback_handler(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text='Enviame link para descargar video'
    )
    return INPUTpy

def generate_pytb(text):
    url = text
    filename = pytube.YouTube(url).streams.first().download()
    return filename

def send_pytb(filename, chat):
    chat.send_action(
        action=ChatAction.UPLOAD_VIDEO,
        timeout=None
        )
    chat.send_video(
        video=open(filename, 'rb')
    )
    os.unlink(filename)

def input_pytb(update, context):
    text = update.message.text
    filename = generate_pytb(text)
    chat = update.message.chat
    send_pytb(filename, chat)
    return ConversationHandler.END