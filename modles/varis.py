import os

try:
    from sample_config import Config
except:
    from config import Config

# Variables
Token = Config.TOKEN
api_id = Config.api_id
api_hash = Config.api_hash

WEBHOOK = bool(os.environ.get("WEBHOOK", False))



