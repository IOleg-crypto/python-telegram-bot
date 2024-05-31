from library import *


class Function:
    def __init__(self) -> None:
        self.SPOTIFY_CLIENT_ID = "YOUR_SPOTIFY_CLIENT_ID"
        self.SPOTIFY_CLIENT_SECRET = "YOUR_SPOTIFY_CLIENT_SECRET"
        self.user_credentials = {}
        self.messages_to_clear = {}

    def on_button_click(message, self):
        self.bot.delete_message(message.chat.id, message.message_id - 1)

    def process_id_step(message, self):
        self.chat_id = message.chat.id
        self.client_id = message.text

        if self.chat_id not in self.user_credentials:
            self.user_credentials[self.chat_id] = {}

        self.user_cond[self.chat_id]["client_id"] = self.client_id
        self.bot.reply_to(self.message, "Spotify Client ID set successfully!")
