import os
from dotenv import load_dotenv

class Config(object):

    load_dotenv()
    # Obtener un token de bot de botfather
    TOKEN = os.getenv('TOKEN')
    # Crear app en https://api.imgur.com/oauth2/addclient Client ID
    imgur_id = os.getenv('imgur_id')
    # Crear app en https://api.imgur.com/oauth2/addclient Client secret
    imgur_secret = os.getenv('imgur_secret')
    # Obtener en my.telegram.org
    api_id = os.getenv('api_id')
    # Obtener en my.telegram.org
    api_hash = os.getenv('api_hash')

