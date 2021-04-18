import os
import re
import wget
import json
import requests
import youtube_dl

from index import app
from bs4 import BeautifulSoup
from datetime import datetime
from telegram import ChatAction, ParseMode
from telegram.ext import ConversationHandler
from requests_toolbelt.multipart.encoder import MultipartEncoder

# Variables
now = datetime.now()
dl = 2
INPUTpy = 0

def dacommand(update, context):
    update.message.reply_text('Enviame link para descargar capítulo de anime')
    return INPUTpy


def da_callback_handler(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text='Enviame link para descargar capítulo de anime'
    )
    return INPUTpy

def download(text):
    link = text
    r = requests.get(link)
    rs = str(r)
    if rs == '<Response [200]>':
        soup = BeautifulSoup(r.content, 'html.parser')
        lnk = []
        for script in soup.find_all(attrs={"class": "btn btn-success btn-download btn-sm rounded-pill"}):
            url = script['href']
            lnk.append(url)
        for l in lnk:
            ls = l.split('/')
            if ls[2] == 'www.mediafire.com':
                mediafire_ = l
            elif ls[2] == 'mega.nz':
                pass
            elif ls[3] == 'v':
                zippyshare = l

        try:
            r = requests.get(mediafire_)
            soup = BeautifulSoup(r.content, 'html.parser')
            dwnld = soup.find(id='downloadButton')
            w = dwnld.get('href')
            da = wget.download(w)
            if da[-4:] != '.mp4':
                os.rename(da, f'{da}.mp4')
                data = f'{da}.mp4'
        except:
            video_info = youtube_dl.YoutubeDL().extract_info(url=l, download=False)
            video_title = video_info['title']

            opciones = {
                'outtmpl': re.sub(r"[^a-zA-Z0-9.]", "", video_title),
            }

            da = re.sub(r"[^a-zA-Z0-9.]", "", video_title)

            with youtube_dl.YoutubeDL(opciones) as ydl:
                ydl.download([l])

            try:
                if da[-4:] != '.mp4':
                   os.rename(da, f'{da}.mp4')
                   data = f'{da}.mp4'
            except:
                pass

    else:
        print(r)
        print('Ese capítulo no existe :3')
    return data, da



def send_da(da, data, chat, chat_id, message_id):
    chat.send_action(
        action=ChatAction.TYPING,
        timeout=None
        )
    app.send_video(
        chat_id,
        video=f"{data}",
        caption=f'{da}',
        parse_mode="md",
        reply_to_message_id=message_id
    )



def input_da(update, context):
    text = update.message.text
    datos = download(text)
    # url, adminCode, data = datos
    message_id = update.message.id
    chat = update.message.chat
    chat_id = chat.id
    send_da(datos, chat)
    os.unlink(datos[2])
    return ConversationHandler.END




