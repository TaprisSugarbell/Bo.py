from modulos.QR import *
from modulos.gis import *
from modulos.aud import *
from modulos.URL import *
from modulos.pytb import *
from modulos.Modles import *
from modulos.Password import *
from modulos.downanime import *
from pyrogram import Client, idle
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, replymarkup
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    Filters,
)


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)

LOGGER = logging.getLogger(__name__)

logging.getLogger("pyrogram.syncer").setLevel(logging.WARNING)


def start(update, context):
    update.message.reply_text(
        text="Hola bienvenido a Bopy\n/qr - Genera QR a partir de un texto\n/url - Acorta un link\n/pwd - Genera contraseña\n/pytb - Descarga video de Youtube\n/aud - Descarga música de Youtube\n/gis - Google Image Search\n/downanime - Descarga anime de Tio Anime",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(text="Generar QR", callback_data="qr"),
                    InlineKeyboardButton(text="Acortar URL", callback_data="url"),
                ],
                [
                    InlineKeyboardButton(text="Descargar Video", callback_data="pytb"),
                    InlineKeyboardButton(text="Descargar Audio", callback_data="aud"),
                ],
                [
                    InlineKeyboardButton(
                        text="Generar Contraseña", callback_data="pwd"
                    ),
                    InlineKeyboardButton(
                        text="Google Image Search", callback_data="gis"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="Descargar Anime", callback_data="downanime"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Repositorio",
                        url="https://github.com/TaprisSugarbell/Bo.py/tree/master",
                    )
                ],
            ]
        ),
    )


if __name__ == "__main__":
    updater = Updater(token=Token, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))

    # Generate QR
    dp.add_handler(
        ConversationHandler(
            entry_points=[
                CommandHandler("qr", qrcommand),
                CallbackQueryHandler(pattern="qr", callback=qr_callback_handler),
            ],
            states={INPUTEXT: [MessageHandler(Filters.text, input_text)]},
            fallbacks=[],
            per_user=True,
        )
    )

    # SHORT URL
    dp.add_handler(
        ConversationHandler(
            entry_points=[
                CommandHandler("url", urlcommand),
                CallbackQueryHandler(pattern="url", callback=url_callback_handler),
            ],
            states={INPUTURL: [MessageHandler(Filters.text, input_url)]},
            fallbacks=[],
            per_user=True,
        )
    )

    # Random Password
    dp.add_handler(
        ConversationHandler(
            entry_points=[
                CommandHandler("pwd", input_password),
                CallbackQueryHandler(pattern="pwd", callback=password_callback_handler),
            ],
            states={INPUTNUM: [MessageHandler(Filters.text, input_password)]},
            fallbacks=[],
            per_user=True,
        )
    )

    # Pytube
    dp.add_handler(
        ConversationHandler(
            entry_points=[
                CommandHandler("pytb", pytbcommand),
                CallbackQueryHandler(pattern="pytb", callback=pytb_callback_handler),
            ],
            states={INPUTpy: [MessageHandler(Filters.text, input_pytb)]},
            fallbacks=[],
            per_user=True,
        )
    )

    # Aud
    dp.add_handler(
        ConversationHandler(
            entry_points=[
                CommandHandler("aud", audcommand),
                CallbackQueryHandler(pattern="aud", callback=aud_callback_handler),
            ],
            states={INPUTpy: [MessageHandler(Filters.text, input_aud)]},
            fallbacks=[],
            per_user=True,
        )
    )

    # Google IMG Search
    dp.add_handler(
        ConversationHandler(
            entry_points=[
                CommandHandler("gis", input_gis),
                CallbackQueryHandler(pattern="gis", callback=gis_callback_handler),
            ],
            states={Inputt: [MessageHandler(Filters.photo, input_gis)]},
            fallbacks=[],
            per_user=True,
        )
    )

    # downanime
    dp.add_handler(
        ConversationHandler(
            entry_points=[
                CommandHandler("downanime", dacommand),
                CallbackQueryHandler(pattern="downanime", callback=da_callback_handler),
            ],
            states={INPUTpy: [MessageHandler(Filters.text, input_da)]},
            fallbacks=[],
        )
    )

    updater.start_polling()
    updater.idle()
    app.start()
    idle()
