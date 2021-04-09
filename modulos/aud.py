import os
import pytube
from moviepy.editor import *
from telegram import ChatAction
from telegram.ext import ConversationHandler

# Variables
INPUTpy = 0

def audcommand(update, context):
    update.message.reply_text('Enviame link para descargar canción')
    return INPUTpy

def aud_callback_handler(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text='Enviame link para descargar canción'
    )
    return INPUTpy

def generate_aud(text):
    url = text
    nombrs = pytube.YouTube(url).title
    filename = pytube.YouTube(url).streams.first().download()
    song = VideoFileClip(filename).audio.write_audiofile(nombrs + '.mp3')
    os.unlink(filename)
    return song

def send_aud(song, chat):
    chat.send_action(
        action=ChatAction.UPLOAD_AUDIO,
        timeout=None
    )
    chat.send_audio(
        audio=ChatAction.UPLOAD_AUDIO,
        timeout=None
    )
    os.unlink(song)


def input_pytb(update, context):
    text = update.message.text
    song = generate_aud(text)
    chat = update.message.chat
    send_aud(song, chat)
    return ConversationHandler.END
