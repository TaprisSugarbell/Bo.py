import os
import json
import requests
from telegram import ChatAction, ParseMode
from telegram.ext import ConversationHandler

#Variables
Inputt = 0

def gis_callback_handler(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text='Enviame imagen para buscar'
    )
    return Inputt

def send_url(links, chat):
    url, isu = links
    chat.send_action(
        action=ChatAction.TYPING,
        timeout=None
    )
    chat.send_message(
        text=f'Google: [Link]({url})\nYandex: [Link]({isu})',
        parse_mode=ParseMode.MARKDOWN_V2
    )


def input_gis(update, context):
    bot = context.bot
    chat = update.message.chat
    try:
        img = update.message.reply_to_message.photo[1].file_id
    except:
        img = update.message.photo[1].file_id
    
    file = bot.getFile(img)
    print("file_id: " + str(img))
    dimg = file.download('temp.png')

    # GIS
    searchUrl = 'http://www.google.com/searchbyimage/upload'
    multipart = {'encoded_image': (dimg, open(dimg, 'rb')), 'image_content': ''}
    response = requests.post(searchUrl, files=multipart, allow_redirects=False)
    url = response.headers['Location']
    # Yandex
    file = dimg
    up = "https://yandex.ru/images/search"
    fileup = {'upfile': ('blob', open(file, 'rb'), 'image/jpeg')}
    params = {'rpt': 'imageview', 'format': 'json',
              'request': '{"blocks":[{"block":"b-page_type_search-by-image__link"}]}'}
    response = requests.post(up, params=params, files=fileup)
    query_string = json.loads(response.content)['blocks'][0]['params']['url']
    isu = up + '?' + query_string

    links = url, isu
    send_url(links, chat)
    os.unlink(dimg)
    return ConversationHandler.END