import os
import logging
from pyrogram import Client, errors

try:
    from sample_config import Config
except:
    from config import Config

# Variables
Token = Config.TOKEN
api_id = Config.api_id
api_hash = Config.api_hash

LOGGER = logging.getLogger(__name__)
WEBHOOK = bool(os.environ.get("WEBHOOK", False))

logging.getLogger("pyrogram.syncer").setLevel(logging.WARNING)

app = Client("BoPyro", api_id=api_id, api_hash=api_hash, bot_token=Token)
apps = []
apps.append(app)


