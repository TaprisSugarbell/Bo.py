import os
import requests
from imgurpython import ImgurClient
from telegram import ChatAction, ParseMode
from telegram.ext import ConversationHandler
try:
    from sample_config import Config
except:
    from config import Config

#Variables
Inputt = 0
imgurid = Config.imgur_id
imgursecret = Config.imgur_secret
im = ImgurClient(client_id=imgurid,client_secret=imgursecret)

def gis_callback_handler(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text='Enviame imagen para buscar'
    )
    return Inputt

def send_url(links, chat):
    url, yandex, snao = links
    chat.send_action(
        action=ChatAction.TYPING,
        timeout=None
    )
    chat.send_message(
        text=f'Google: [Link]({url})\nYandex: [Link]({yandex})\nSauceNAO: [Link]({snao})',
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
    searchurl = 'http://www.google.com/searchbyimage/upload'
    multipart = {'encoded_image': (dimg, open(dimg, 'rb')), 'image_content': ''}
    response = requests.post(searchurl, files=multipart, allow_redirects=False)
    url = response.headers['Location']
    # Yandex
    # file = dimg
    # up = "https://yandex.ru/images/search"
    # fileup = {'upfile': ('blob', open(file, 'rb'), 'image/jpeg')}
    # params = {'rpt': 'imageview', 'format': 'json',
    #           'request': '{"blocks":[{"block":"b-page_type_search-by-image__link"}]}'}
    # response = requests.post(up, params=params, files=fileup)
    # print(response)
    # query_string = json.loads(response.content)['blocks'][0]['params']['url']
    # isu = up + '?' + query_string
    upload = im.upload_from_path(dimg)
    link = upload["link"]
    yandex = f'https://yandex.com/images/search?url={link}&rpt=imageview'
    snao = f'https://saucenao.com/search.php?db=999&numres=16&url={link}'

    links = url, yandex, snao
    send_url(links, chat)
    os.unlink(dimg)
    return ConversationHandler.END
