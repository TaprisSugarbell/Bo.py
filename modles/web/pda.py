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
usermame = Config.usermame
# logging.basicConfig(filename="app.log", level="DEBUG")

def danbooru_callback(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text="Ingresa URL"
    )
    return Input

def send_pic(lfu, varis, chat, context):
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
    strlsac = strlsau.replace("/", "_")
    strlsauc = re.sub(r"[^a-zA-Z0-9_# ]", "", strlsac)
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
    chat.send_action(
        action=ChatAction.UPLOAD_PHOTO,
        timeout=20
    )
    chat.send_message(
        text=f"<b>PostID: </b><code>{id}</code>\n" +
                f"<b>ParentID: </b><code>{parent_id}</code>\n" +
                caption["Artist"] +
                caption["Sauce"] +
                caption["Characters"] +
                f"<b>Tags:</b> <i>{strl}</i>"
                f"<a href='{lfu}'>&#8205;</a>",
        parse_mode=ParseMode.HTML
    )


def input_danbooru(update, context):
    chat = update.message.chat
    chat1 = update.effective_chat
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
    lfu = post["large_file_url"]
    # Datos Botones
    send_pic(lfu, varis, chat, context)
    return ConversationHandler.END
