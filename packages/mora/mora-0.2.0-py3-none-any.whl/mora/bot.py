"""
Minimal Telegram Bot integration using only standard library.
Supports inline keyboard via reply_markup.
"""
import threading
import urllib.request
import urllib.parse
import json
import time

class TelegramBot:
    def __init__(self, token):
        self.token = token
        self.api_url = f'https://api.telegram.org/bot{token}/'
        self.offset = None
        self.running = False

    def get_updates(self, timeout=30):
        params = {'timeout': timeout}
        if self.offset:
            params['offset'] = self.offset + 1
        url = self.api_url + 'getUpdates?' + urllib.parse.urlencode(params)
        with urllib.request.urlopen(url, timeout=timeout+5) as resp:
            data = json.loads(resp.read().decode())
            return data.get('result', [])

    def send_message(self, chat_id, text, reply_markup=None):
        params = {'chat_id': chat_id, 'text': text}
        if reply_markup is not None:
            params['reply_markup'] = json.dumps(reply_markup)
        data = urllib.parse.urlencode(params).encode()
        url = self.api_url + 'sendMessage'
        req = urllib.request.Request(url, data=data)
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())

    def handle_update(self, update):
        # override this in handlers
        pass

    def _polling_loop(self):
        self.running = True
        while self.running:
            for u in self.get_updates():
                self.offset = u['update_id']
                try:
                    self.handle_update(u)
                except:
                    pass
            time.sleep(1)

    def start(self):
        t = threading.Thread(target=self._polling_loop, daemon=True)
        t.start()

    def stop(self):
        self.running = False