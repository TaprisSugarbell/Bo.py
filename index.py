from config import Config
from modulos.Modles import *
from telegram import ChatAction, InlineKeyboardMarkup, InlineKeyboardButton, replymarkup
from telegram.ext import Updater, CommandHandler,  CallbackQueryHandler,ConversationHandler, MessageHandler, Filters, commandhandler



def start(update, context):
    update.message.reply_text(
        text='Hola bienvenido a Bopy',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text='Generar QR', callback_data='qr'), 
            InlineKeyboardButton(text='Acortar URL', callback_data='url')],
            [InlineKeyboardButton(text='Generador de Contraseña', callback_data='psw')],
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
        entry_points=[CallbackQueryHandler(pattern='qr', callback=qr_callback_handler)], 
        states={INPUTEXT: [MessageHandler(Filters.text, input_text)]}, 
        fallbacks=[]))

    # SHORT URL
    dp.add_handler(ConversationHandler(
        entry_points=[CallbackQueryHandler(pattern='url', callback=url_callback_handler)], 
            states={INPUTURL: [MessageHandler(Filters.text, input_url)]}, 
            fallbacks=[]))
    
    # Random Password
    dp.add_handler(ConversationHandler(
        entry_points=[CallbackQueryHandler(pattern='psw', callback=password_callback_handler)],
        states={INPUTNUM: [MessageHandler(Filters.text, input_password)]},
        fallbacks=[]))
    
    # add handler
    updater.start_polling()
    updater.idle()












































































