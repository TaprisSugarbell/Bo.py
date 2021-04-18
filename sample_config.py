import os
from dotenv import load_dotenv


class Config(object):

    load_dotenv()
    # Obtener un token de bot de botfather
    TOKEN = os.getenv("TOKEN")
    # Obtener un token de deezer
    ARL = os.getenv("ARL")
    # Obtener en my.telegram.org
    api_id = os.getenv("api_id")
    # Obtener en my.telegram.org
    api_hash = os.getenv("api_hash")
