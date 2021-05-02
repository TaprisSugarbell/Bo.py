import os
import re
import wget
import requests
from pybooru import Danbooru
from telegram import ChatAction, ParseMode
from telegram.ext import ConversationHandler
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


def send_pic(file, varis, chat):
    id, source, tags_string, tags_string_general, parent_id, \
        character, artist, sauce, file_url, ext = varis
    # Esto agrega los tags
    lst = tags_string_general.split(" ")
    lstg = []
    for tag in lst:
        lstg.append(f"#{tag}")
    strlst = " ".join(lstg)

    chat.send_action(
        action=ChatAction.UPLOAD_PHOTO,
        timeout=None
    )
    chat.send_photo(
        caption=f"<b>Artist:</b> {artist}\n<b>Tags:</b> {strlst}\n<b>Source:</b> {source}\n",
        parse_mode=ParseMode.HTML,
        photo=open(file, "rb")
    )
    chat.send_document(
        document=open(file, "rb")
    )


def input_danbooru(update, context):
    chat = update.message.chat
    idpost = context.args
    idpostj = "".join(idpost)
    idposts = idpostj.split("/")
    filter = re.sub(r"[^0-9]", "", idposts[4])
    client = Danbooru("danbooru", username=usermame, api_key=api_key)
    try:
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
    send_pic(file, varis, chat)
    return ConversationHandler.END


