from pyrogram import filters
from bot import LOG, app, advance_config, chats_data, from_chats, to_chats

LOG.info("Welcome, this is the telegram-message-forwarder-bot. main routine...")

@app.on_message(filters.chat(from_chats))
def work(client, message):
  if advance_config:
    try:
      for chat in chats_data[message.chat.id]:
        message.copy(chat)
    except Exception as e:
      LOG.error(e)
  else:
    try:
      for chat in to_chats:
        message.copy(chat)
    except Exception as e:
      LOG.error(e)
      
app.run()
