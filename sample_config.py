import os
from dotenv import load_dotenv

class Config(object):

    load_dotenv()
    # Obtener un token de bot de botfather
    TOKEN = os.getenv('TOKEN')
    # Obtener un token de deezer
    ARL = os.getenv('arl')


