import sys
import logging
from os import environ
from pyrogram import Client

log_level = environ.get("LOG_LEVEL", "INFO").upper()
logging.basicConfig(format='[%(asctime)s - %(pathname)s - %(levelname)s] %(message)s',
                    handlers=[logging.FileHandler('log.txt'), logging.StreamHandler()],
                    level=log_level)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
LOG = logging.getLogger(__name__)

chats_data = {}

LOG.info("Welcome, this is the telegram-message-forwarder-bot. initializing...")

api_id = int(environ["API_ID"])
api_hash = environ["API_HASH"]
bot_token = environ.get("BOT_TOKEN", None)
tg_session = environ.get("TELEGRAM_SESSION", None)
try:
  from_chats = list(set(int(x) for x in environ.get("FROM_CHATS").split()))
  to_chats = list(set(int(x) for x in environ.get("TO_CHATS").split()))
except:
  from_chats = []
  to_chats = []
advance_config = environ.get("ADVANCE_CONFIG", None)
if advance_config:
  from_chats = []

if tg_session:
  LOG.info("Session Mode - {tg_session}")
  app = Client(tg_session, api_id, api_hash)
elif bot_token:
  LOG.info("Bot Mode")
  app = Client(":memory:", api_id, api_hash, bot_token=bot_token)
  
with app:
  if advance_config:
    for chats in advance_config.split(";"):
      chat = chats.strip().split()
      f = int(chat[0])
      del chat[0]
      chat = [int(i) for i in chat]
      if f in chats_data:
        c = chats_data[f]
        c.extend(chat)
        chats_data[f] = c
      else:
        chats_data[f] = chat
      if not f in from_chats:
        from_chats.append(f)
    LOG.info(f"From Chats: {from_chats}")
    LOG.info(f"Advanced Config: {chats_data}")
  else:
    LOG.info(f"From Chats: {from_chats}")
    LOG.info(f"To Chats: {to_chats}")
