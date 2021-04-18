import os
import qrcode
from telegram import ChatAction
from telegram.ext import ConversationHandler

# Variables
INPUTEXT = 0

# QR
def qrcommand(update, context):
    update.message.reply_text("Enviame texto para hacerlo QR")
    return INPUTEXT


def qr_callback_handler(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Enviame texto para hacerlo QR")
    return INPUTEXT


def generate_qr(text):
    filename = text + ".jpg"
    img = qrcode.make(text)
    img.save(filename)
    return filename


def send_qr(filename, chat):
    chat.send_action(action=ChatAction.UPLOAD_PHOTO, timeout=None)
    chat.send_photo(photo=open(filename, "rb"))
    os.unlink(filename)


def input_text(update, context):
    text = update.message.text
    filename = generate_qr(text)
    chat = update.message.chat
    send_qr(filename, chat)
    return ConversationHandler.END
