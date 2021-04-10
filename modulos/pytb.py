import os
import wget
import requests
import youtube_dl
# from mega import Mega
from config import Config
# from pydeezer import Deezer
from bs4 import BeautifulSoup
from telegram import ChatAction
from telegram.ext import ConversationHandler
# from pydeezer.constants import track_formats

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
    
    if url[2] == 'mega.nz':
        # mega = Mega()
        # m = mega.login()
        # filename = m.download_url(url)
        pass

    elif url[2] == 'www.mediafire.com':
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        dwnld = soup.find(id='downloadButton')
        w = dwnld.get('href')
        filename = wget.download(w)

    elif url[2] == 'www.deezer.com':
        # arl = Config.ARL
        # deezer = Deezer(arl=arl)
        # user_info = deezer.user

        # download_dir = ''

        # track_id = url[4]
        # track = deezer.get_track(track_id)

        # track_info = track["info"]
        # filename = track["download"](download_dir, quality=track_formats.MP3_320)
        pass

    else:
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