import os
import re
import wget
import requests
from PIL import Image
from pybooru import Danbooru
from telegram.ext import ConversationHandler
from telegram import ChatAction, ParseMode, PhotoSize
try:
    from sample_config import Config
except:
    from config import Config

# Variables
Input = 0
api_key = Config.api_key
usermame = Config.usermame

def danbooru_callback(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text="Ingresa URL"
    )
    return Input


def send_pic(file, filejpg, varis, chat):
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

    chat.send_action(
        action=ChatAction.UPLOAD_PHOTO,
        timeout=None
    )
    chat.send_photo(
        caption=f"<b>PostID:</b> <a href='https://danbooru.donmai.us/posts/{id}'>{id}</a>\n"
                f"<b>ParentID:</b> <a href='https://danbooru.donmai.us/posts/{parent_id}'>{parent_id}</a>\n<b>Artist:</b> "
                f"{artist}\n<b>Sauce:</b> {sauce}\n<b>Characters:</b> {character}\n"
                f"<b>Tags:</b> {strl}\n<b>Source:</b> {source}",
        parse_mode=ParseMode.HTML,
        photo=open(filejpg, "rb")
    )
    chat.send_action(
        action=ChatAction.UPLOAD_DOCUMENT,
        timeout=None
    )
    chat.send_document(
        document=open(file, "rb"),
        timeout=None
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
    id, source, tags_string, tags_string_general, parent_id, \
        character, artist, sauce, file_url, ext = \
        post["id"], post["source"], post["tag_string"], post["tag_string_general"], post["parent_id"], \
        post["tag_string_character"], post["tag_string_artist"], post["tag_string_copyright"], \
        post["file_url"], post["file_ext"]

    varis = \
        post["id"], post["source"], post["tag_string"], post["tag_string_general"], post["parent_id"], \
        post["tag_string_character"], post["tag_string_artist"], post["tag_string_copyright"], \
        post["file_url"], post["file_ext"]

    archname = f"{id} {artist} {character}.{ext}"
    file = wget.download(file_url, archname)
    # Reduciendo Tamaño
    img = Image.open(file)
    size = img.size
    fileresize = img.resize(size)
    fileresize.save('file.jpg', 'jpeg')
    filejpg = "file.jpg"

    send_pic(file, filejpg, varis, chat)
    os.unlink(file)
    os.unlink(filejpg)
    return ConversationHandler.END


