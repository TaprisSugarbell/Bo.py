import os
import pytube
import threading
from queue import Queue
from datetime import datetime
from telegram import ChatAction
from telegram.ext import ConversationHandler

# Variables
INPUTpy = 0

def pytbcommand(update, context):
    update.message.reply_text('Enviame link para descargar video')
    return INPUTpy

def pytb_callback_handler(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text='Enviame link para descargar video'
    )
    return INPUTpy

def generate_pytb(text):
    with open('cola.txt', 'a') as csf:
        csf.write(text + '\n')
    filename = pytube.YouTube(url).streams.first().download()


    q = Queue()
    num_threads = 2
    now = datetime.now()

    with open('cola.txt', 'r') as pyk:
        pyk = pyk.readlines()

    urls = [
        pyk
    ]

    def message(s):
        print('{}: {}'.format(threading.current_thread().name, s))

    def download(q):
        while True:
            message('Buscando en la próxima fila')
            url = q.get()
            data = pytube.YouTube(url).title
            message('Descargando {}'.format(data))
            filename = pytube.YouTube(url).streams.first().download()
            # Save the downloaded file to the current directory
            message('Escribiendo como: {}'.format(data))
            with open('logs.txt', 'a') as outfile:
                outfile.write('Se descargo: {} {}\n'.format(data, now))
            q.task_done()


    # Set up some threads
    for i in range(num_threads):
        worker = threading.Thread(
            target=download,
            args=(q,),
            name='\nworker-{}'.format(i),
        )
        worker.setDaemon(True)
        worker.start()

    for url in urls:
        stng = ''.join(url)
        lstng = stng.split()
        for msg in lstng:
            message('queuing {}'.format(
                msg))
            q.put(msg)


    # Se procesaron todas las descargas.
    message('*** Cola principal en espera')
    q.join()
    message('*** Hecho')
    return filename

def send_pytb(filename, chat):
    chat.send_action(
        action=ChatAction.UPLOAD_VIDEO,
        timeout=None
        )
    chat.send_video(
        video=open(filename, 'rb')
    )
    os.unlink(filename)
    os.remove('cola.txt')

def input_pytb(update, context):
    text = update.message.text
    filename = generate_pytb(text)
    chat = update.message.chat
    send_pytb(filename, chat)
    return ConversationHandler.END