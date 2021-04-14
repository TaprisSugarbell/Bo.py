from modulos.QR import *
from modulos.gis import *
from modulos.aud import *
from modulos.URL import *
from modulos.pytb import *
from modulos.Password import *
from modulos.Modles import Token
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, replymarkup
from telegram.ext import Updater, CommandHandler,  CallbackQueryHandler,ConversationHandler, MessageHandler, Filters

def start(update, context):
    update.message.reply_text(
        text='Hola bienvenido a Bopy\n/qr - Genera QR a partir de un texto\n/url - Acorta un link\n/pwd - Genera contraseña\n/pytb - Descarga video de Youtube\n/aud - Descarga música de Youtube',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text='Generar QR', callback_data='qr'), 
            InlineKeyboardButton(text='Acortar URL', callback_data='url')],
            [InlineKeyboardButton(text='Descargar Video', callback_data='pytb'),
            InlineKeyboardButton(text='Descargar Audio', callback_data='aud')],
            [InlineKeyboardButton(text='Generar Contraseña', callback_data='pwd'),
            InlineKeyboardButton(text='Google Image Search', callback_data='gis')],
            [InlineKeyboardButton(
                text='Repositorio', url='https://github.com/TaprisSugarbell/Bo.py/tree/master')],
        ])
        )


if __name__ == '__main__':
    updater = Updater(token=Token, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))

    # Generate QR
    dp.add_handler(ConversationHandler(
        entry_points=[CommandHandler('qr', qrcommand),
        CallbackQueryHandler(pattern='qr', callback=qr_callback_handler)], 
        states={INPUTEXT: [MessageHandler(Filters.text, input_text)]}, 
        fallbacks=[]))

    # SHORT URL
    dp.add_handler(ConversationHandler(
        entry_points=[CommandHandler('url', urlcommand),
        CallbackQueryHandler(pattern='url', callback=url_callback_handler)], 
            states={INPUTURL: [MessageHandler(Filters.text, input_url)]}, 
            fallbacks=[]))
    
    # Random Password
    dp.add_handler(ConversationHandler(
        entry_points=[CommandHandler('pwd', input_password),
        CallbackQueryHandler(pattern='pwd', callback=password_callback_handler)],
        states={INPUTNUM: [MessageHandler(Filters.text, input_password)]},
        fallbacks=[]))

    # Pytube
    dp.add_handler(ConversationHandler(
        entry_points=[CommandHandler('pytb', pytbcommand),
        CallbackQueryHandler(pattern='pytb', callback=pytb_callback_handler)],
        states={INPUTpy: [MessageHandler(Filters.text, input_pytb)]},
        fallbacks=[]))

    # Aud
    dp.add_handler(ConversationHandler(
        entry_points=[CommandHandler('aud', audcommand),
        CallbackQueryHandler(pattern='aud', callback=aud_callback_handler)],
        states={INPUTpy: [MessageHandler(Filters.text, input_aud)]},
        fallbacks=[]))
    
    # Google IMG Search
    dp.add_handler(ConversationHandler(
        entry_points=[CommandHandler('gis', input_gis),
        CallbackQueryHandler(pattern='gis', callback=gis_callback_handler)],
        states={Inputt: [MessageHandler(Filters.photo, input_gis)]},
        fallbacks=[]
    ))

    # add handler
    updater.start_polling()
    updater.idle()












































































