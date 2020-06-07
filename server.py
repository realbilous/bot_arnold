from bot import telegram_chatbot
import csv
from reply import read_data, make_reply

countries_dict = read_data()

update_id = None
bot = telegram_chatbot("config.cfg")


starter = "Hello! I am Arnold Bot.\nI will help you find the facts on any coutry of your interest." +\
          "\nJust type its name! (e.g. United States)"

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
            if message == None:
                continue
            from_id = item["message"]["from"]["id"]
            if message == "/start":
                bot.send_message(starter, from_id)
                continue
            text, img_url = make_reply(message, countries_dict)
            bot.send_photo(img_url, from_id)
            bot.send_message(text, from_id)

