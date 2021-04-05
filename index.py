import os
import qrcode
import pyshorteners
from modulos.SauceNAO import *
from telegram import ChatAction, InlineKeyboardMarkup, InlineKeyboardButton, replymarkup
from telegram.ext import Updater, CommandHandler,  CallbackQueryHandler,ConversationHandler, MessageHandler, Filters, commandhandler


INPUTEXT = 0
INPUTURL = 0

def start(update, context):
    update.message.reply_text(
        text='Hola bienvenido a Bopy',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text='Generar QR', callback_data='qr'), InlineKeyboardButton(text='Acortar URL', callback_data='url')],
            [InlineKeyboardButton(text='Repositorio', url='https://github.com/TaprisSugarbell/Bo.py/tree/master')],
        ])
        )

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

def url_callback_handler(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text='Enviame url para acortarlo'
    )
    return INPUTURL

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
    pass

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

def input_text(update, context):
    text = update.message.text
    filename = generate_qr(text)
    chat = update.message.chat
    send_qr(filename, chat)
    return ConversationHandler.END

if __name__ == '__main__':
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))

    dp.add_handler(ConversationHandler(entry_points=[CommandHandler('qr', qrcommand), CallbackQueryHandler(pattern='qr', callback=qr_callback_handler)], states={INPUTEXT: [MessageHandler(Filters.text, input_text)]}, fallbacks=[]))
    dp.add_handler(ConversationHandler(entry_points=[CallbackQueryHandler(pattern='url', callback=url_callback_handler)], states={INPUTURL: [MessageHandler(Filters.text, input_url)]}, fallbacks=[]))
    # add handler
    updater.start_polling()
    updater.idle()












































































