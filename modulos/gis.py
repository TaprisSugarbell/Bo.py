import os
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

def send_url(url, chat):
    chat.send_action(
        action=ChatAction.TYPING,
        timeout=None
    )
    chat.send_message(
        text=f'Google: [Link]({url})',
        parse_mode=ParseMode.MARKDOWN_V2
    )


def input_gis(update, context):
    bot = context.bot
    chat = update.message.chat
    try:
        img = update.message.reply_to_message.photo[2].file_id
    except:
        img = update.message.photo[2].file_id
    file = bot.getFile(img)
    print("file_id: " + str(img))
    dimg = file.download('modulos/src/temp.png')

    searchUrl = 'http://www.google.com/searchbyimage/upload'
    multipart = {'encoded_image': (dimg, open(dimg, 'rb')), 'image_content': ''}
    response = requests.post(searchUrl, files=multipart, allow_redirects=False)
    url = response.headers['Location']
    send_url(url, chat)
    os.unlink(dimg)
    return ConversationHandler.END