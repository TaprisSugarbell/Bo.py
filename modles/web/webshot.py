import os
import time
from selenium import webdriver
from telegram import ChatAction
from telegram.ext import ConversationHandler

#Variables
input_webshot = 0

def webshot_callback(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text="Ingresa URL"
    )
    return input_webshot

def send_webshot(photo, chat):
    chat.send_action(
        action=ChatAction.UPLOAD_PHOTO,
        timeout=None
    )
    chat.send_document(
        document=open(photo, "rb")
    )

def input_webshot(update, context):
    chat = update.message.chat
    urll = context.args
    url = "".join(urll)
    options = webdriver.ChromeOptions()
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    options.add_argument('--window-size=1024,900')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument("--hide-scrollbars")

    browser = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=options)

    browser.get(url)
    time.sleep(2)
    photo = browser.save_screenshot('temp.png')
    browser.close()

    send_webshot(photo, chat)
    os.unlink(photo)
    return ConversationHandler.END


