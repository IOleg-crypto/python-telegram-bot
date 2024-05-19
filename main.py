import telebot
import webbrowser
from telebot import types

#token to connect bot
bot = telebot.TeleBot('6895824327:AAEyCfrTRh-7wGuIjrAVSe9y2gXxx1Vpunk') 

@bot.message_handler(commands=['start'])

def main(message):
    bot.send_message(message.chat.id, 'Hello, ' + message.from_user.first_name + message.from_user.last_name)
    markup = types.ReplyKeyboardMarkup()
    btn = types.KeyboardButton("Clear chat " , callback_data = 'clearchat')
    markup.add(btn) 
    bot.send_message(message.chat.id, 'Chat cleared')
    bot.register_next_step_handler(message, setnumber)
   
@bot.message_handler(commands=['setnumber'])

def setnumber(message):
    bot.send_message(message.chat.id, 5)
   
@bot.message_handler(commands=['website'])

def site(message):
    bot.send_message(message.chat.id, "That author`s website: https://github.com/IOleg-crypto/python-telegram-bot")
   
@bot.message_handler(commands=['getbutton'])
def getbutton(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('GitHub', url='https://github.com/IOleg-crypto/python-telegram-bot')
    #params : use only '' because you don`t see button`
    markup.row(btn1)
    bot.reply_to(message, "That author`s website: https://github.com/IOleg-crypto/python-telegram-bot", reply_markup=markup)
   
    
#@bot.callback_query_handler(func= lambda callback: True)
#def callback_inline(callback):
   # if callback.data == 'clearchat':
    #   bot.delete_message(callback.message.chat.id, callback.message.message_id - 1000)

bot.polling(none_stop=True)