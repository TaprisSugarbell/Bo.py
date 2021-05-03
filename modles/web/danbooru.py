import os
import re
import wget
import logging
import requests
from PIL import Image
from pybooru import Danbooru
from telegram.ext import ConversationHandler
from telegram import ChatAction, ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
try:
    from sample_config import Config
except:
    from config import Config

# Variables
Input = 0
api_key = Config.api_key
channel = Config.channel
usermame = Config.usermame
IDuser = int(Config.chatuser)
# logging.basicConfig(filename="app.log", level="DEBUG")

def danbooru_callback(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text="Ingresa URL"
    )
    return Input

def inline_danboo(url, datoskey):
    urls = url.split("/")
    pixiv_id, id, file_url = datoskey
    danbo = InlineKeyboardButton(text="Danbooru", url=f"https://danbooru.donmai.us/posts/{id}")
    dirdanbo = InlineKeyboardButton(text="Direct Link", url=file_url)
    try:
        urls[2] == "twitter.com"
        source = InlineKeyboardButton(text="Twitter", url=url)
        danboo_inline = InlineKeyboardMarkup([[danbo, dirdanbo], [source]])
    except:
        if pixiv_id != None:
            source = InlineKeyboardButton(text="Pixiv", url=f"http://pixiv.net/i/{pixiv_id}")
            danboo_inline = InlineKeyboardMarkup([[danbo, dirdanbo], [source]])
        else:
            danboo_inline = InlineKeyboardMarkup([[danbo, dirdanbo]])
    return danboo_inline

def send_pic(file, filejpg, danboo_inline, varis, chat, context):
    chatuser = chat["id"]
    id, source, tags_string, tags_string_general, parent_id, \
        character, artist, sauce, file_url, ext = varis
    # Esto agrega los tags
    lst = tags_string_general.split(" ")
    lstg = []
    for tag in lst:
        lstg.append(f"#{tag}")
    strlst = " ".join(lstg)
    strlstr = strlst.replace("-", "_")
    strl = re.sub(r"[^a-zA-Z0-9_# ]", "", strlstr)
    # Tag a el ---------------------------------- character
    lstc = character.split(" ")
    lstcl = []
    for charact in lstc:
        lstcl.append(f"#{charact}")
    strlstc = " ".join(lstcl)
    strlc = re.sub(r"[^a-zA-Z0-9_# ]", "", strlstc)
    # Limpiando --------------------------------- Artista
    artistl = re.sub(r"[^a-zA-Z0-9_# ]", "", artist)
    # Limpiando --------------------------------- Sauce
    lsts = sauce.split(" ")
    lstsa = []
    for sau in lsts:
        lstsa.append(f"#{sau}")
    strlsau = " ".join(lstsa)
    strlsauc = re.sub(r"[^a-zA-Z0-9_# ]", "", strlsau)
    # Texto Caption
    caption = {}
    if isinstance(artistl, str):
        caption["Artist"] = f"<b>Artist: #{artistl}</b>\n"
    if sauce == "original":
        caption["Sauce"] = f"<b>Sauce: #original</b>\n"
        caption["Characters"] = f"<b>Characters: #original</b>\n"
    elif sauce != "original":
        caption["Sauce"] = f"<b>Sauce: {strlsauc}</b>\n"
    try:
        isinstance(character[2], str)
        caption["Characters"] = f"<b>Characters: {strlc}</b>\n"
    except:
        pass
    # logging.info("Se creo el diccionario %s y se esta enviando la imagen", caption)
    if chatuser == IDuser:
        chat.send_action(
            action=ChatAction.UPLOAD_PHOTO,
            timeout=20
        )
        context.bot.send_photo(
            caption=f"<b>PostID: </b><code>{id}</code>\n" +
                    f"<b>ParentID: </b><code>{parent_id}</code>\n" +
                    caption["Artist"] +
                    caption["Sauce"] +
                    caption["Characters"] +
                    f"<b>Tags:</b> <i>{strl}</i>",
            parse_mode=ParseMode.HTML,
            photo=open(filejpg, "rb"),
            chat_id=channel,
            reply_markup=danboo_inline
        )
        # logging.info("Se esta subiendo la foto como documento")
        chat.send_action(
            action=ChatAction.UPLOAD_DOCUMENT,
            timeout=20
        )
        context.bot.send_document(
            document=open(file, "rb"),
            chat_id=channel,
            timeout=20
        )
    elif chatuser != IDuser:
        chat.send_action(
            action=ChatAction.UPLOAD_PHOTO,
            timeout=20
        )
        chat.send_photo(
            caption=f"<b>PostID: </b><code>{id}</code>\n" +
                    f"<b>ParentID: </b><code>{parent_id}</code>\n" +
                    caption["Artist"] +
                    caption["Sauce"] +
                    caption["Characters"] +
                    f"<b>Tags:</b> <i>{strl}</i>",
            parse_mode=ParseMode.HTML,
            photo=open(filejpg, "rb"),
            reply_markup=danboo_inline
        )
        # logging.info("Se esta subiendo la foto como documento")
        chat.send_action(
            action=ChatAction.UPLOAD_DOCUMENT,
            timeout=20
        )
        chat.send_document(
            document=open(file, "rb"),
            timeout=20
        )


def input_danbooru(update, context):
    chat = update.message.chat
    idpost = context.args
    idpostj = "".join(idpost)
    idposts = idpostj.split("/")
    client = Danbooru("danbooru", username=usermame, api_key=api_key)
    try:
        filter1 = idposts[4].split("?")
        filter = re.sub(r"[^0-9]", "", filter1[0])
        post = client.post_show(filter)
    except:
        post = client.post_show(idpostj)
    # Variables de Pybooru
    id, source, tags_string, tags_string_general, parent_id, \
        character, artist, sauce, file_url, ext = \
        post["id"], post["source"], post["tag_string"], post["tag_string_general"], post["parent_id"], \
        post["tag_string_character"], post["tag_string_artist"], post["tag_string_copyright"], \
        post["file_url"], post["file_ext"]

    varis = \
        post["id"], post["source"], post["tag_string"], post["tag_string_general"], post["parent_id"], \
        post["tag_string_character"], post["tag_string_artist"], post["tag_string_copyright"], \
        post["file_url"], post["file_ext"]
    # logging.info("Obteniendo variables %s", varis)

    archname = f"{id} {artist} {character}.{ext}"
    file = wget.download(file_url, archname)
    # Reduciendo Tamaño
    img = Image.open(file)
    size = img.size
    fileresize = img.resize(size)
    fileconvert = fileresize.convert("RGB")
    fileconvert.save('file.jpg', 'jpeg')
    filejpg = "file.jpg"

    # Datos Botones
    datoskey = post["pixiv_id"], post["id"], post["file_url"]
    danboo_inline = inline_danboo(source, datoskey)
    send_pic(file, filejpg, danboo_inline, varis, chat, context)
    os.unlink(file)
    os.unlink(filejpg)
    return ConversationHandler.END


