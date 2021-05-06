import re
import json
import requests
import html_to_json
from PIL import Image
from bs4 import BeautifulSoup
from telegram import ChatAction, ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
try:
    from sample_config import Config
except:
    from config import Config

# Variables
Input = 0
api_key = Config.api_key
channel = Config.channel
channel2 = Config.channel2
username = Config.username
IDuser = int(Config.chatuser)
# logging.basicConfig(filename="app.log", level="DEBUG")

def filter_post(postlink):
    try:
        post_link = int(postlink)
    except:
        post_link = postlink
    if isinstance(post_link, int):
        post_id = post_link
    elif isinstance(post_link, str):
        link_split = post_link.split("/")
        if link_split[2] == "konachan.com":
            post_id = link_split[5]
        elif link_split[2] == "danbooru.donmai.us":
            post_split = link_split[4].split("?")
            post_id = post_split[0]
        else:
            print("No se ingreso link o no es valido")
    return post_id


def danboo_show(link):
    post_id = filter_post(link)
    if api_key != None:
        base = f"https://danbooru.donmai.us/posts/{post_id}.json?login={username}&api_key={api_key}"
    elif isinstance(api_key, str):
        base = f"https://danbooru.donmai.us/posts/{post_id}.json"
    r = requests.get(base).content
    post_decode = r.decode("utf-8")
    post_info = json.loads(post_decode)
    return post_info


def download_booru(post_link):
    post = danboo_show(post_link)

    try:
        id = post["id"]
        artist = post["tag_string_artist"]
        character = post["tag_string_character"]
        ext = post["file_ext"]
        nimg = f"{id} {artist} {character}.{ext}"

    except:
        print("No se pudo descargar")
    rimg = requests.get(post["file_url"]).content
    with open(nimg, "wb") as img:
        img.write(rimg)
    return nimg


def soupBeauty(r):
    soup = BeautifulSoup(r.content, "html.parser")
    return soup


def kona_show(link):
    post_id = filter_post(link)
    base = requests.get(f"https://konachan.com/post/show/{post_id}")
    soup = soupBeauty(base)
    json_ = html_to_json.convert(base.text)
    infodic = {}
    infodic["id"] = post_id
    infodic["tags"] = json_["html"][0]["head"][0]["link"][2]["meta"][0]["meta"][0]["meta"][3]["_attributes"]["content"]
    infodic["tag_split"] = infodic["tags"].split(" ")
    try:
        prbl = json_["html"][0]["body"][0]["div"][6]["div"][0]["div"][2]["a"]
        listparent = []
        for pr in prbl[1:]:
            listparent.append(pr["_value"])
        infodic["parent_id"] = listparent
    except KeyError:
        pass
    except IndexError:
        pass
    try:
        url = soup.find_all(attrs={"class": "original-file-unchanged"})[0].get("href")
    except:
        url = soup.find_all(attrs={"class": "original-file-changed"})[0].get("href")
    infodic["file_ext"] = url[-3:]
    infodic["file_url"] = url
    return infodic


def download_kona(post_link):
    post = kona_show(post_link)
    try:
        id = post["id"]
        tags = " ".join(post["tag_split"][:6])
        ext = post["file_ext"]
        nimg = f"{id} {tags}.{ext}"
    except:
        print("No se pudo descargar")
    rimg = requests.get(post["file_url"]).content
    with open(nimg, "wb") as img:
        img.write(rimg)
    return nimg


def filter_text(text):
    filter2 = text.split("/")
    filter1 = filter2[4].split("?")
    filter0 = re.sub(r"[^0-9]", "", filter1[0])
    return filter0


def filejpeg(file):
    img = Image.open(file)
    fileconvert = img.convert("RGB")
    fileconvert.save('file.jpg', 'jpeg')
    filejpg = "file.jpg"
    return filejpg


def clean_tags(tags):
    tag_split = tags.split(" ")
    lista_tag = []
    for tag in tag_split:
        lista_tag.append(f"#{tag}")
    tag_string = " ".join(lista_tag)
    re_tag0 = tag_string.replace("/", "_")
    re_tag = re_tag0.replace("-", "_")
    clean_tag = re.sub(r"[^a-zA-Z0-9_# ]", "", re_tag)
    return clean_tag


def clean_one(tag):
    one_clean = re.sub(r"[^a-zA-Z0-9_# ]", "", tag)
    return one_clean


# def botones_filter():
#     urls = url.split("/")
#     pixiv_id, id, file_url = datoskey
#     danbo = InlineKeyboardButton(text="Danbooru", url=f"https://danbooru.donmai.us/posts/{id}")
#     dirdanbo = InlineKeyboardButton(text="Direct Link", url=file_url)
#     if urls[2] == "twitter.com":
#         source = InlineKeyboardButton(text="Twitter", url=url)
#         danboo_inline = InlineKeyboardMarkup([[danbo, dirdanbo], [source]])
#     elif urls[2] == "e-hentai.org":
#         source = InlineKeyboardButton(text="E-Hentai", url=url)
#         danboo_inline = InlineKeyboardMarkup([[danbo, dirdanbo], [source]])
#     elif pixiv_id != None:
#         source = InlineKeyboardButton(text="Pixiv", url=f"http://pixiv.net/i/{pixiv_id}")
#         danboo_inline = InlineKeyboardMarkup([[danbo, dirdanbo], [source]])
#     else:
#         danboo_inline = InlineKeyboardMarkup([[danbo, dirdanbo]])
#         return dan


def site_filter_danboo(post):
    pixiv_id, id, file_url, url = post["pixiv_id"], post["id"], post["file_url"], post["source"]
    urls = url.split("/")
    danbo = InlineKeyboardButton(text="Danbooru", url=f"https://danbooru.donmai.us/posts/{id}")
    dirdanbo = InlineKeyboardButton(text="Direct Link", url=file_url)
    if urls[2] == "twitter.com":
        source = InlineKeyboardButton(text="Twitter", url=url)
        danboo_inline = InlineKeyboardMarkup([[danbo, dirdanbo], [source]])
    elif urls[2] == "e-hentai.org":
        source = InlineKeyboardButton(text="E-Hentai", url=url)
        danboo_inline = InlineKeyboardMarkup([[danbo, dirdanbo], [source]])
    elif pixiv_id != None:
        source = InlineKeyboardButton(text="Pixiv", url=f"http://pixiv.net/i/{pixiv_id}")
        danboo_inline = InlineKeyboardMarkup([[danbo, dirdanbo], [source]])
    else:
        danboo_inline = InlineKeyboardMarkup([[danbo, dirdanbo]])
    return danboo_inline


def btn_url_gen(text="", url=""):
    btn = InlineKeyboardButton(text=text, url=url)
    return btn

def btn_markup_2(btn, btn2):
    btn_inline = InlineKeyboardMarkup([[btn, btn2]])
    return btn_inline


def btn_markup_3(btn, btn2, btn3):
    btn_inline = InlineKeyboardMarkup([[btn, btn2], [btn3]])
    return btn_inline


def inline_test(post):
    pixiv_id, post_id, file_url, url = post["pixiv_id"], post["id"], post["file_url"], post["source"]
    urls = url.split("/")
    danbo = btn_url_gen("Danbooru", f"https://danbooru.donmai.us/posts/{post_id}")
    dirdanbo = btn_url_gen("Direct Link", file_url)
    if urls[2] == "twitter.com":
        source = btn_url_gen("Twitter", url)
        inline = btn_markup_3(danbo, dirdanbo, source)
    elif urls[2] == "e-hentai.org":
        source = btn_url_gen("E-Hentai", url)
        inline = btn_markup_3(danbo, dirdanbo, source)
    elif urls[2] == "arca.live":
        source = btn_url_gen("Aka Live", url)
        inline = btn_markup_3(danbo, dirdanbo, source)
    elif pixiv_id != None:
        source = btn_url_gen("Pixiv", f"http://pixiv.net/i/{pixiv_id}")
        inline = btn_markup_3(danbo, dirdanbo, source)
    else:
        inline = btn_markup_2(danbo, dirdanbo)
    return inline


def chat_send(files, caption, inline, chat):
    file, filejpg = files
    chat.send_action(
        action=ChatAction.UPLOAD_PHOTO,
        timeout=20
    )
    chat.send_photo(
        caption=caption,
        parse_mode=ParseMode.HTML,
        photo=open(filejpg, "rb"),
        reply_markup=inline
    )
    chat.send_action(
        action=ChatAction.UPLOAD_DOCUMENT,
        timeout=20
    )
    chat.send_document(
        document=open(file, "rb"),
        timeout=20
    )


def channel_send(files, caption, inline, chat, context):
    file, filejpg = files
    chat.send_action(
        action=ChatAction.UPLOAD_PHOTO,
        timeout=20
    )
    context.bot.send_photo(
        caption=caption,
        parse_mode=ParseMode.HTML,
        photo=open(filejpg, "rb"),
        chat_id=channel,
        reply_markup=inline
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


def channel2_send(files, caption, inline, chat, context):
    file, filejpg = files
    chat.send_action(
        action=ChatAction.UPLOAD_PHOTO,
        timeout=20
    )
    context.bot.send_photo(
        caption=caption,
        parse_mode=ParseMode.HTML,
        photo=open(filejpg, "rb"),
        chat_id=channel2,
        reply_markup=inline
    )
    # logging.info("Se esta subiendo la foto como documento")
    chat.send_action(
        action=ChatAction.UPLOAD_DOCUMENT,
        timeout=20
    )
    context.bot.send_document(
        document=open(file, "rb"),
        chat_id=channel2,
        timeout=20
    )


def caption_text(post):
    post_id, source, tags, parent_id, \
        character, artist, sauce, file_url, ext = \
        post["id"], post["source"], post["tag_string_general"], post["parent_id"], \
        post["tag_string_character"], post["tag_string_artist"], post["tag_string_copyright"], \
        post["file_url"], post["file_ext"]
    # Esto agrega los tags
    tags_clean = clean_tags(tags)
    # Tag a el ---------------------------------- character
    clean_character = clean_tags(character)
    # Limpiando --------------------------------- Artista
    clean_artist = clean_one(artist)
    # Limpiando --------------------------------- Sauce
    clean_sauce = clean_tags(sauce)
    # Texto Caption
    caption = {}
    if isinstance(clean_artist, str):
        caption["Artist"] = f"<b>Artist: #{clean_artist}</b>\n"
    if sauce == "original":
        caption["Sauce"] = f"<b>Sauce: #original</b>\n"
        caption["Characters"] = f"<b>Characters: #original</b>\n"
    elif sauce != "original":
        caption["Sauce"] = f"<b>Sauce: {clean_sauce}</b>\n"
    try:
        isinstance(character[2], str)
        caption["Characters"] = f"<b>Characters: {clean_character}</b>\n"
    except:
        pass
    caption_clean = f"<b>PostID: </b><code>{post_id}</code>\n" \
                    f"<b>ParentID: </b><code>{parent_id}</code>\n" + \
                    caption["Artist"] + \
                    caption["Sauce"] + \
                    caption["Characters"] + \
                    f"<b>Tags:</b> <i>{tags_clean}</i>"
    return caption_clean

def caption_preview(post):
    post_id, source, tags, parent_id, \
        character, artist, sauce, ext = \
        post["id"], post["source"], post["tag_string_general"], post["parent_id"], \
        post["tag_string_character"], post["tag_string_artist"], post["tag_string_copyright"], post["file_ext"]
    lfu = post["large_file_url"]
    # Esto agrega los tags
    tags_clean = clean_tags(tags)
    # Tag a el ---------------------------------- character
    clean_character = clean_tags(character)
    # Limpiando --------------------------------- Artista
    clean_artist = clean_one(artist)
    # Limpiando --------------------------------- Sauce
    clean_sauce = clean_tags(sauce)
    # Texto Caption
    caption = {}
    if isinstance(clean_artist, str):
        caption["Artist"] = f"<b>Artist: #{clean_artist}</b>\n"
    if sauce == "original":
        caption["Sauce"] = f"<b>Sauce: #original</b>\n"
        caption["Characters"] = f"<b>Characters: #original</b>\n"
    elif sauce != "original":
        caption["Sauce"] = f"<b>Sauce: {clean_sauce}</b>\n"
    try:
        isinstance(character[2], str)
        caption["Characters"] = f"<b>Characters: {clean_character}</b>\n"
    except:
        pass
    preview = f"<b>PostID: </b><code>{post_id}</code>\n" \
                    f"<b>ParentID: </b><code>{parent_id}</code>\n" + \
                    caption["Artist"] + \
                    caption["Sauce"] + \
                    caption["Characters"] + \
                    f"<b>Tags:</b> <i>{tags_clean}</i>" \
                    f"<a href='{lfu}'>&#8205;</a>"
    return preview


def send_preview(caption, inline, chat):
    chat.send_action(
        action=ChatAction.UPLOAD_PHOTO,
        timeout=20
    )
    chat.send_message(
        text=caption,
        parse_mode=ParseMode.HTML,
        reply_markup=inline
    )


def kona_clean(tags):
    if tags == "None":
        tag_clean = "<code>None</code>"
    else:
        tag_list = []
        for tag in tags:
            tag_list.append(f"</code>{tag}</code>")
        tag_join = " ".join(tag_list)
        tag_clean = re.sub(r"[^a-zA-Z0-9_#</> ]", "", tag_join)
    return tag_clean


def caption_kona(post):
    try:
        tags, post_id, parent_id = post["tags"], post["id"], post["parent_id"]
    except:
        tags, post_id, parent_id = post["tags"], post["id"], "None"
    # Esto agrega los tags
    tags_clean = clean_tags(tags)
    # Parent Clean
    parent_clean = kona_clean(parent_id)
    # Texto Caption
    caption_clean = f"<b>PostID: </b><code>{post_id}</code>\n" \
                    f"<b>ParentID: </b>{parent_clean}\n" \
                    f"<b>Tags:</b> <i>{tags_clean}</i>"
    return caption_clean


def inline_kona(post):
    post_id, file_url = post["id"], post["file_url"]
    kona = btn_url_gen("Konachan", f"https://konachan.com/post/show/{post_id}")
    dirkona = btn_url_gen("Direct Link", file_url)
    inline = btn_markup_2(kona, dirkona)
    return inline


def chat_kona(files, caption, inline, chat):
    file, filejpg = files
    chat.send_action(
        action=ChatAction.UPLOAD_PHOTO,
        timeout=20
    )
    chat.send_photo(
        caption=caption,
        parse_mode=ParseMode.HTML,
        photo=open(filejpg, "rb"),
        reply_markup=inline
    )
    chat.send_action(
        action=ChatAction.UPLOAD_DOCUMENT,
        timeout=20
    )
    chat.send_document(
        document=open(file, "rb"),
        timeout=20
    )


def channel_kona(files, caption, inline, chat, context):
    file, filejpg = files
    chat.send_action(
        action=ChatAction.UPLOAD_PHOTO,
        timeout=20
    )
    context.bot.send_photo(
        caption=caption,
        parse_mode=ParseMode.HTML,
        photo=open(filejpg, "rb"),
        chat_id=channel,
        reply_markup=inline
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






