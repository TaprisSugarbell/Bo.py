import os

try:
    from sample_config import Config
except:
    from config import Config

# Variables
Token = Config.TOKEN
WEBHOOK = bool(os.environ.get("WEBHOOK", False))



