import os
import re
import wget
import json
import requests
import youtube_dl
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
        mp_encoder = MultipartEncoder(
            fields={
                'filesUploaded': (data, open(data, 'rb'))
            }
        )
        r = requests.post(
            'https://srv-store5.gofile.io/uploadFile',
            data=mp_encoder,
            headers={'Content-Type': mp_encoder.content_type}
        )
        scrap = r.json()
        url = scrap['data']['downloadPage']
        admincode = scrap['data']['adminCode']
        datos = (url, admincode,data)
        ncap = re.sub(r"[^0-9]", "", link)
        print(f'El capítulo {ncap} se ha descargado correctamente :3')
    else:
        print(r)
        print('Ese capítulo no existe :3')
    return datos



def send_da(datos, chat):
    chat.send_action(
        action=ChatAction.TYPING,
        timeout=None
        )
    chat.send_message(
        text=f'Aqui esta tu link:\n{datos[0]}\nY aqui tu código para editarlo:\n`{datos[1]}`',
        parse_mode=ParseMode.MARKDOWN
    )



def input_da(update, context):
    text = update.message.text
    datos = download(text)
    # url, adminCode, data = datos
    chat = update.message.chat
    send_da(datos, chat)
    os.unlink(datos[2])
    return ConversationHandler.END




