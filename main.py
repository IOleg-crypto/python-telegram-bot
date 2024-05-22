import telebot
from telebot import types

#token to connect bot
bot = telebot.TeleBot('6895824327:AAEyCfrTRh-7wGuIjrAVSe9y2gXxx1Vpunk') 

@bot.message_handler(commands=['start'])

def start(message):
    local_name = f'Hello, <b>{message.from_user.first_name + message.from_user.last_name}</b>'
    bot.send_message(message.chat.id , local_name , parse_mode = 'html')
    
@bot.message_handler()
def get_user_text(message):
    if message.text == "Hello":
        bot.send_message(message.chat.id, "Hello")
    elif message.text == "id":
         bot.send_message(message.chat.id,f'Your id : {message.from_user.id}')
    else:
        bot.send_message(message.chat.id, "I don`t understand you")
          
@bot.message_handler(commands=['website'])
def site(message):
    bot.send_message(message.chat.id, f"That author`s website: {https://github.com/IOleg-crypto/python-telegram-bot}")
   

bot.polling(none_stop = True)