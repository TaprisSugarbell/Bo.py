import os
import ffmpeg
import youtube_dl
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
    # Obtenemos el titulo del video
    video_info = youtube_dl.YoutubeDL().extract_info(url=url, download=False)
    video_title = video_info['title']

    # Setear las opciones para la descarga del video
    opciones = {
        'format': 'bestaudio/best',
        'outtmpl': f'modulos/{video_title}.mp3',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    # Descargar el Video
    with youtube_dl.YoutubeDL(opciones) as ydl:
        ydl.download([url])

def send_aud(outtmpl, chat):
    chat.send_action(
        action=ChatAction.UPLOAD_AUDIO,
        timeout=None
    )
    chat.send_audio(
        audio=open(outtmpl, 'rb'),
        timeout=None
    )
    os.unlink(outtmpl)


def input_aud(update, context):
    text = update.message.text
    url = text
    video_info = youtube_dl.YoutubeDL().extract_info(url=url, download=False)
    video_title = video_info['title']
    outtmpl = f'modulos/{video_title}.mp3'
    generate_aud(text)
    chat = update.message.chat
    send_aud(outtmpl, chat)
    return ConversationHandler.END
