import telebot
from telebot import types
import requests
import webbrowser
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import re
from googlesearch import search
#token to connect bot
bot = telebot.TeleBot('6895824327:AAEyCfrTRh-7wGuIjrAVSe9y2gXxx1Vpunk') 

class Functions:
      def get_spotify_client(chat_id):
       if chat_id in user_credentials and 'client_id' in user_credentials[chat_id] and 'client_secret' in user_credentials[chat_id]:
        client_id = user_credentials[chat_id]['client_id']
        client_secret = user_credentials[chat_id]['client_secret']
        return spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))
      else:
        return None       
        
SPOTIFY_CLIENT_ID = 'YOUR_SPOTIFY_CLIENT_ID'
SPOTIFY_CLIENT_SECRET = 'YOUR_SPOTIFY_CLIENT_SECRET'
user_credentials = {}

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET))
messages_to_clear = {}
@bot.message_handler(commands=['start'])

def start(message):
    local_name = f'Hello, <b>{message.from_user.first_name + message.from_user.last_name}</b>'
    say_hello = bot.send_message(message.chat.id , local_name , parse_mode = 'html')
    markup = types.ReplyKeyboardMarkup(row_width=1)
    itembtn1 = types.KeyboardButton('Clear chat')

    markup.add(itembtn1)
    bot.send_message(message.chat.id, say_hello, reply_markup=markup)
    bot.register_next_step_handler(message, on_button_click)
   
def on_button_click(message):
    bot.delete_message(message.chat.id, message.message_id - 1)
    
def log_message(message):
    chat_id = message.chat.id
    if chat_id not in messages_to_clear:
        messages_to_clear[chat_id] = []
    messages_to_clear[chat_id].append(message.message_id)   
   
def search_spotify(query):
    url = f"https://itunes.apple.com/search?term={query}&entity=song&limit=5"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('results', [])
    return []   
   
""""
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    sent_message = bot.reply_to(message, message.text)
    log_message(message)
    log_message(sent_message)    
"""""  

@bot.message_handler(commands=['findgoogle'])
def find_song(message):
    try:
        query = message.text.split(' ', 1)[1] + " song"
        results = search(query, num_results=5)
        if results:
            response = "Top search results:\n" + "\n".join(results)
            bot.reply_to(message, response)
        else:
            bot.reply_to(message, "No results found.")
    except IndexError:
        bot.reply_to(message, "Please provide a song name. For example: /findgoogle Imagine")
        
@bot.message_handler(commands=['clear'])
def clear_messages(message):
    chat_id = message.chat.id
    if chat_id in messages_to_clear:
        for msg_id in messages_to_clear[chat_id]:
            try:
                bot.delete_message(chat_id, msg_id)
            except Exception as e:
                print(f"Failed to delete message {msg_id}: {e}")
        messages_to_clear[chat_id] = []
    bot.reply_to(message, "Cleared all messages.")
    log_message(message)

                  
                  
@bot.message_handler(commands=['set_id'])
def set_id(message):
    msg = bot.reply_to(message, "Please send your Spotify Client ID")
    bot.register_next_step_handler(msg, process_id_step)

def process_id_step(message):
    chat_id = message.chat.id
    client_id = message.text
    if chat_id not in user_credentials:
        user_credentials[chat_id] = {}
    user_credentials[chat_id]['client_id'] = client_id
    bot.reply_to(message, "Spotify Client ID set successfully!")

@bot.message_handler(commands=['set_secret'])

def set_secret(message):
    msg = bot.reply_to(message, "Please send your Spotify Client Secret")
    bot.register_next_step_handler(msg, process_secret_step)

def process_secret_step(message):
    chat_id = message.chat.id
    client_secret = message.text
    if chat_id not in user_credentials:
        user_credentials[chat_id] = {}
    user_credentials[chat_id]['client_secret'] = client_secret
    bot.reply_to(message, "Spotify Client Secret set successfully!")                  
                  
@bot.message_handler(commands=['website'])         
def site(message):
    bot.send_message(message.chat.id, "That author`s website: {https://github.com/IOleg-crypto/python-telegram-bot}")
    markup = types.ReplyKeyboardMarkup(row_width=1)
    itembtn1 = types.KeyboardButton('Go to website')
    markup.add(itembtn1)
    bot.send_message(message.chat.id, "Go to website",  reply_markup=markup)
    
@bot.message_handler(commands=['finditunes'])
def find_song(message):
    try:
        query = message.text.split(' ', 1)[1]
        results = search_itunes(query)
        if results:
            response = '\n'.join([f"{song['trackName']} by {song['artistName']}\n{song['trackViewUrl']}" for song in results[:5]])
            bot.reply_to(message, response)
        else:
            bot.reply_to(message, "No results found.")
    except IndexError:
        bot.reply_to(message, "Please provide a song name. For example: /finditunes Imagine")

# Function to search iTunes for a song
def search_itunes(query):
    url = f"https://itunes.apple.com/search?term={query}&entity=song&limit=5"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('results', [])
    return []
    
@bot.message_handler(commands=['findspotify'])    
    
def find_song(message):
    try:
        url = message.text.split(' ', 1)[1]
        match = re.search(r"open.spotify.com/track/([a-zA-Z0-9]+)", url)
        if match:
            track_id = match.group(1)
            track = sp.track(track_id)
            response = f"{track['name']} by {', '.join([artist['name'] for artist in track['artists']])}\n{track['external_urls']['spotify']}"
            bot.reply_to(message, response)
        else:
            bot.reply_to(message, "Please provide a valid Spotify track URL. For example: /find https://open.spotify.com/track/xyz")
    except IndexError:
        bot.reply_to(message, "Please provide a Spotify track URL. For example: /findspotify https://open.spotify.com/track/xyz")


def main():
    bot.polling(none_stop = True)

if __name__ == '__main__':
    main()