from modles import varis
from modles.reverse import gis
from modles.web import webshot, danbooru, danboo
from modles.cmds import QR, aud, URL, downanime, Password, pytb
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler,  CallbackQueryHandler, ConversationHandler, MessageHandler, Filters

def start(update, context):
    update.message.reply_text(
        text='Hola bienvenido a Bopy\n/qr - Genera QR a partir de un texto\n/url - Acorta un link\n/pwd - Genera contraseña\n/pytb - Descarga video de Youtube\n/aud - Descarga música de Youtube\n/gis - Google Image Search\n/downanime - Descarga anime de Tio Anime',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text='Generar QR', callback_data='qr'), 
            InlineKeyboardButton(text='Acortar URL', callback_data='url')],
            [InlineKeyboardButton(text='Descargar Video', callback_data='pytb'),
            InlineKeyboardButton(text='Descargar Audio', callback_data='aud')],
            [InlineKeyboardButton(text='Generar Contraseña', callback_data='pwd'),
            InlineKeyboardButton(text='Google Image Search', callback_data='gis')],
            [InlineKeyboardButton(text='Descargar Anime', callback_data='downanime')],
            # [InlineKeyboardButton(
            #     text='Repositorio', url='https://github.com/TaprisSugarbell/Bo.py/tree/master')]
        ])
        )

if __name__ == '__main__':
    updater = Updater(token=varis.Token, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))

    # Generate QR
    dp.add_handler(ConversationHandler(
        entry_points=[CommandHandler('qr', QR.qrcommand),
        CallbackQueryHandler(pattern='qr', callback=QR.qr_callback_handler)],
        states={QR.INPUTEXT: [MessageHandler(Filters.text, QR.input_text)]},
        fallbacks=[],
        per_user=True
        ))

    # SHORT URL
    dp.add_handler(ConversationHandler(
        entry_points=[CommandHandler('url', URL.urlcommand),
        CallbackQueryHandler(pattern='url', callback=URL.url_callback_handler)],
            states={URL.INPUTURL: [MessageHandler(Filters.text, URL.input_url)]},
            fallbacks=[],
            per_user=True
            ))
    
    # Random Password
    dp.add_handler(ConversationHandler(
        entry_points=[CommandHandler('pwd', Password.input_password),
        CallbackQueryHandler(pattern='pwd', callback=Password.password_callback_handler)],
        states={Password.INPUTNUM: [MessageHandler(Filters.text, Password.input_password)]},
        fallbacks=[],
        per_user=True
            ))

    # Pytube
    dp.add_handler(ConversationHandler(
        entry_points=[CommandHandler('pytb', pytb.pytbcommand),
        CallbackQueryHandler(pattern='pytb', callback=pytb.pytb_callback_handler)],
        states={pytb.INPUTpy: [MessageHandler(Filters.text, pytb.input_pytb)]},
        fallbacks=[],
        per_user=True
            ))

    # Aud
    dp.add_handler(ConversationHandler(
        entry_points=[CommandHandler('aud', aud.audcommand),
                      CallbackQueryHandler(pattern='aud', callback=aud.aud_callback_handler)],
        states={aud.INPUTpy: [MessageHandler(Filters.text, aud.input_aud)]},
        fallbacks=[],
        per_user=True
            ))
    
    # Google IMG Search
    dp.add_handler(ConversationHandler(
        entry_points=[CommandHandler('gis', gis.input_gis),
                      CallbackQueryHandler(pattern='gis', callback=gis.gis_callback_handler)],
        states={gis.Inputt: [MessageHandler(Filters.photo, gis.input_gis)]},
        fallbacks=[],
        per_user=True
            ))

    # downanime
    dp.add_handler(ConversationHandler(
        entry_points=[CommandHandler('downanime', downanime.dacommand),
                      CallbackQueryHandler(pattern='downanime', callback=downanime.da_callback_handler)],
        states={downanime.INPUTpy: [MessageHandler(Filters.text, downanime.input_da)]},
        fallbacks=[]
    ))

    # Webshot
    dp.add_handler(ConversationHandler(
        entry_points=[CommandHandler("webshot", webshot.input_webshot),
                      CallbackQueryHandler(pattern="webshot", callback=webshot.webshot_callback)],
        states={webshot.input_webshot: [MessageHandler(Filters.text, webshot.input_webshot)]},
        fallbacks=[]
    ))

    # Danbooru Channel
    dp.add_handler(ConversationHandler(
        entry_points=[CommandHandler("d", danbooru.input_danbooru),
                      CallbackQueryHandler(pattern="d", callback=danbooru.danbooru_callback)],
        states={danbooru.Input: [MessageHandler(Filters.text, danbooru.input_danbooru)]},
        fallbacks=[]
    ))

    # Danbooru
    dp.add_handler(ConversationHandler(
        entry_points=[CommandHandler("danbooru", danboo.input_danbooru),
                      CallbackQueryHandler(pattern="danbooru", callback=danboo.danbooru_callback)],
        states={danboo.Input: [MessageHandler(Filters.text, danboo.input_danbooru)]},
        fallbacks=[]
    ))

    updater.start_polling()
    updater.idle()











































































