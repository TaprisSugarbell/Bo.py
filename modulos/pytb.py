import os
import wget
import requests
import youtube_dl
from config import Config
from mega import Mega
from pydeezer import Deezer
from bs4 import BeautifulSoup
from telegram import ChatAction
from telegram.ext import ConversationHandler
from pydeezer.constants import track_formats

# Variables
INPUTpy = 0
try:
    from sample_config import Config
except:
    from config import Config


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
    iurl = text.split('/')
    
    if iurl[2] == 'mega.nz':
        mega = Mega()
        m = mega.login()
        filename = m.download_url(url)

    elif iurl[2] == 'www.mediafire.com':
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        dwnld = soup.find(id='downloadButton')
        w = dwnld.get('href')
        filename = wget.download(w)

    elif iurl[2] == 'www.deezer.com':
        arl = Config.ARL
        url = url.split('/')
        deezer = Deezer(arl=arl)
        user_info = deezer.user

        download_dir = ''

        if url[3] == 'mx':
            track_id = url[4]
            if url[4] == 'track':
                track_id = url[5]
            elif url[3] == 'track':
                track_id = url[3]
            elif url[4] == 'album':
                album_id = url[5]
        elif url[3] == 'us':
            track_id = url[4]
        elif url[3] == 'es':
            track_id = url[4]
        try:
            track = deezer.get_track(track_id)
            track_info = track["info"]
            filename = '{}.flac'.format(track_info['DATA']['SNG_TITLE'])
            track["download"](download_dir, quality=track_formats.FLAC)
        except:
            # album = deezer.get_album_tracks(album_id)
            pass

    else:
        video_info = youtube_dl.YoutubeDL().extract_info(url=url, download=False)
        video_title = video_info['title']

        opciones = {
            'outtmpl': f'modulos/src/{video_title}.mp4',
        }
        filename = f'/modulos/src/{video_title}.mp4'
        with youtube_dl.YoutubeDL(opciones) as ydl:
            ydl.download([url])
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