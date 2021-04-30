import os
import io
import requests
from PIL import Image
from bs4 import BeautifulSoup
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
    upload = im.upload_from_path(dimg) #Subir a Imgur
    link = upload["link"]
    yandex = f'https://yandex.com/images/search?url={link}&rpt=imageview'

    # SauceNAO
    minsim = '80!'
    api_key = Config.sauce_api
    thumbSize = (250, 250)

    # enable or disable indexes
    index_hmags = '0'
    index_reserved = '0'
    index_hcg = '0'
    index_ddbobjects = '0'
    index_ddbsamples = '0'
    index_pixiv = '1'
    index_pixivhistorical = '1'
    index_reserved = '0'
    index_seigaillust = '1'
    index_danbooru = '0'
    index_drawr = '1'
    index_nijie = '1'
    index_yandere = '0'
    index_animeop = '0'
    index_reserved = '0'
    index_shutterstock = '0'
    index_fakku = '0'
    index_hmisc = '0'
    index_2dmarket = '0'
    index_medibang = '0'
    index_anime = '0'
    index_hanime = '0'
    index_movies = '0'
    index_shows = '0'
    index_gelbooru = '0'
    index_konachan = '0'
    index_sankaku = '0'
    index_animepictures = '0'
    index_e621 = '0'
    index_idolcomplex = '0'
    index_bcyillust = '0'
    index_bcycosplay = '0'
    index_portalgraphics = '0'
    index_da = '1'
    index_pawoo = '0'
    index_madokami = '0'
    index_mangadex = '0'

    # generate appropriate bitmask
    db_bitmask = int(
        index_mangadex + index_madokami + index_pawoo + index_da + index_portalgraphics + index_bcycosplay + index_bcyillust + index_idolcomplex + index_e621 + index_animepictures + index_sankaku + index_konachan + index_gelbooru + index_shows + index_movies + index_hanime + index_anime + index_medibang + index_2dmarket + index_hmisc + index_fakku + index_shutterstock + index_reserved + index_animeop + index_yandere + index_nijie + index_drawr + index_danbooru + index_seigaillust + index_anime + index_pixivhistorical + index_pixiv + index_ddbsamples + index_ddbobjects + index_hcg + index_hanime + index_hmags,
        2)
    print("dbmask=" + str(db_bitmask))

    fname = "kurumi.jpg"
    print(fname)
    image = Image.open(fname)
    image = image.convert('RGB')
    image.thumbnail(thumbSize, resample=Image.ANTIALIAS)
    imagedata = io.BytesIO()
    image.save(imagedata, format='PNG')

    url = 'http://saucenao.com/search.php?output_type=0&numres=1&minsim=' + minsim + '&dbmask=' + str(
        db_bitmask) + '&api_key=' + api_key
    files = {'file': ("image.png", imagedata.getvalue())}
    imagedata.close()

    r = requests.post(url, files=files)
    soup = BeautifulSoup(r.content, "html.parser")
    listalink = []
    for link in soup.find_all(attrs={"class": "linkify"}):
        listalink.append(link)
    snao = listalink[0].get("href")

    links = url, yandex, snao
    send_url(links, chat)
    os.unlink(dimg)
    return ConversationHandler.END
