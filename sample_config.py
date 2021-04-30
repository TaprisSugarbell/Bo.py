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
    # Obtener api en https://saucenao.com/user.php?page=search-api
    sauce_api = os.getenv('sauce_api')
