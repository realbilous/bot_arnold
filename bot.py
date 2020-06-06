import requests
import json
import configparser as cfg

class telegram_chatbot():
    def __init__(self, config):
        self.token = self.read_token(config)
        self.base = f"https://api.telegram.org/bot{self.token}"

    def get_updates(self, offset=None, timeout=100):
        url = self.base + f"/getUpdates?timeout={timeout}"
        if offset:
            url = url + f"&offset={offset + 1}"
        r = requests.get(url)
        return r.json()

    def send_message(self, msg, chat_id):
        url = self.base + f"/sendMessage?chat_id={chat_id}&text={msg}"
        if msg is not None:
            requests.get(url)

    def send_photo(self, img_url, chat_id):
        url = self.base + f"/sendPhoto?chat_id={chat_id}&photo={img_url}"
        if img_url is not None:
            requests.get(url)

    def read_token(self, config):
        parser = cfg.ConfigParser()
        parser.read(config)
        return parser.get('creds', "token")