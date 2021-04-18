import pyshorteners
from telegram import ChatAction
from telegram.ext import ConversationHandler

# Variables
INPUTURL = 0

# URL
def urlcommand(update, context):
    update.message.reply_text("Enviame url para acortarlo")
    return INPUTURL


def url_callback_handler(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Enviame url para acortarlo")
    return INPUTURL


def input_url(update, context):
    url = update.message.text
    chat = update.message.chat

    # acortar url
    s = pyshorteners.Shortener()
    short = s.chilpit.short(url)

    chat.send_action(action=ChatAction.TYPING, timeout=None)
    chat.send_message(text=short)
    return ConversationHandler.END
