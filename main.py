import telebot
from telebot import types
import requests
import webbrowser
#token to connect bot
bot = telebot.TeleBot('6895824327:AAEyCfrTRh-7wGuIjrAVSe9y2gXxx1Vpunk') 


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
    bot.delete_message(message.chat.id, message.message_id - 100)
@bot.message_handler(сommands=['text'])
def text(message):
    bot.delete_message(message.chat.id, message.message_id - 100)
                  
@bot.message_handler(commands=['website'])         
def site(message):
    bot.send_message(message.chat.id, "That author`s website: {https://github.com/IOleg-crypto/python-telegram-bot}")
    markup = types.ReplyKeyboardMarkup(row_width=1)
    itembtn1 = types.KeyboardButton('Go to website')
    markup.add(itembtn1)
    bot.send_message(message.chat.id, "Go to website",  reply_markup=markup)
    if message.text == "Go to website":
       webbrowser.open("https://github.com/IOleg-crypto/python-telegram-bot")
    
@bot.message_handler(commands=['song'])  
def find_song(message):
    bot.reply_to(message.chat.id, "Welcome! Send me a song name and I'll find it for you.")
    song_name = message.text
    try:
        itunes_url = f"https://itunes.apple.com/search?term={song_name}&limit=1"
        response = requests.get(itunes_url)
        data = response.json()
        
        if data['resultCount'] > 0:
            result = data['results'][0]
            song_info = f"Song: {result['trackName']}\nArtist: {result['artistName']}\nAlbum: {result['collectionName']}\nLink: {result['trackViewUrl']}"
            bot.reply_to(message, song_info)
        else:
            bot.reply_to(message, "Sorry, I couldn't find that song.")
    except Exception as e:
        bot.reply_to(message, "An error occurred. Please try again later.")
        print(f"Error: {e}") 
''''
@bot.message_handler()
def get_user_text(message):
    if message.text == "Hello":
        bot.send_message(message.chat.id, "Hello")
    elif message.text == "id":
         bot.send_message(message.chat.id,f'Your id : {message.from_user.id}')
'''''
bot.polling(none_stop = True)