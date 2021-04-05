import os
import random
import string
import qrcode
import telegram
import pyshorteners
from dotenv import load_dotenv
from telegram import parsemode
from telegram.utils.helpers import escape_markdown, mention_html, mention_markdown
from telegram import ChatAction, InlineKeyboardMarkup, InlineKeyboardButton, replymarkup
from telegram.ext import Updater, CommandHandler,  CallbackQueryHandler,ConversationHandler, MessageHandler, Filters, commandhandler


# VARIABLES
load_dotenv()
key = os.getenv('key')
TOKEN = os.getenv('TOKEN')
INPUTEXT = 0
INPUTURL = 0
INPUTNUM = 0

# QR
def qrcommand(update, context):
    update.message.reply_text('Enviame texto para hacerlo qr')
    return INPUTEXT

def qr_callback_handler(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text='Enviame texto para hacerlo QR'
    )
    return INPUTEXT

def generate_qr(text):
    filename = text + '.jpg'
    img = qrcode.make(text)
    img.save(filename)
    return filename

def send_qr(filename, chat):
    chat.send_action(
        action=ChatAction.UPLOAD_PHOTO,
        timeout=None
        )
    chat.send_photo(
        photo=open(filename, 'rb')
    )
    os.unlink(filename)

def input_text(update, context):
    text = update.message.text
    filename = generate_qr(text)
    chat = update.message.chat
    send_qr(filename, chat)
    return ConversationHandler.END



# URL
def url_callback_handler(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text='Enviame url para acortarlo'
    )
    return INPUTURL


def input_url(update, context):
    url = update.message.text
    chat = update.message.chat

    #acortar url
    s = pyshorteners.Shortener()
    short = s.chilpit.short(url)
    
    chat.send_action(
        action=ChatAction.TYPING,
        timeout=None
        )
    chat.send_message(
        text=short
    )
    return ConversationHandler.END







def password_callback_handler(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text='Parámetros\n1. Alfabeto\n2. Mayúsculas\n3. Minúsculas\n4. Números\n5. Alfanumérico\n6. Alfanumérico y Símbolos\nIngresa el número de tu elección y/o la longitud,\npor defecto "8"')
    return INPUTNUM

def input_password(update, context):
    password = update.message.text
    chat = update.message.chat
    s = ''
    afn = password.split()
    m = int(afn[0])
    try:
        n = int(afn[1])
    except IndexError:
        n = 8

    if m == 1:
        c = list(string.ascii_letters)
    elif m == 2:
        c = list(string.ascii_uppercase)
    elif m == 3:
        c = list(string.ascii_lowercase)
    elif m == 4:
        c = list(string.digits)
    elif m == 5:
        c = list(string.hexdigits)
    elif m == 6:   
        c = list(string.printable)
        c = c[:-6]

    for i in range(n):
        s += random.choice(c)

    #asdfghjk = s.format(parsemode=parsemode.ParseMode.MARKDOWN)
    #print(asdfghjk)
    chat.send_action(
        action=ChatAction.TYPING,
        timeout=None
        )
    chat.send_message(
        text=f"Tu contraseña es: `{s}`",
    )
    return ConversationHandler.END
