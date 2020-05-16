from bot import telegram_chatbot

update_id = None
bot = telegram_chatbot("config.cfg")

def make_reply(msg):
    reply = "Received."
    return reply

while True:
    print("...")
    updates = bot.get_updates(offset=update_id)
    updates = updates["result"]
    if updates:
        for item in updates:
            update_id = item["update_id"]
            try:
                message = str(item["message"]["text"])
            except:
                message = None
            #print(message)
            from_id = item["message"]["from"]["id"]
            reply = make_reply(message)
            bot.send_message(reply, from_id)