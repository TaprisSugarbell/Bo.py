import os
import youtube_dl
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
    video_info = youtube_dl.YoutubeDL().extract_info(url=url, download=False)
    video_title = video_info['title']

    opciones = {
        'outtmpl': f'{video_title}.mp4',
    }

    with youtube_dl.YoutubeDL(opciones) as ydl:
        filename = ydl.download([url])
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