import telebot
from telebot import types

#token to connect bot
bot = telebot.TeleBot('6895824327:AAEyCfrTRh-7wGuIjrAVSe9y2gXxx1Vpunk') 

@bot.message_handler(commands=['start'])

def start(message):
    bot.send_message(message.chat.id, 'Hello, ' + message.from_user.first_name + message.from_user.last_name)
    markup = types.ReplyKeyboardMarkup()
    btn = types.KeyboardButton('Clear chat ')
    btn1 = types.KeyboardButton('Show author github')
    markup.add(btn) 
    markup.add(btn1)
    bot.send_message(message.chat.id, 'Chat cleared' , reply_markup=markup)
    bot.register_next_step_handler(message, on_click)
    
def on_click(message):
    if message.text == 'Clear chat':
       bot.delete_message(message.chat.id, message.message_id - 1)
    elif message.text == 'Show author github':
        bot.send_message(message.chat.id, 'That author`s website: https://github.com/IOleg-crypto/python-telegram-bot')
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
    bot.reply_to(message, "That author`s website", reply_markup=markup)
   
@bot.message_handler(commands=['clearChat'])
def clearChat(message):
    markup = types.InlineKeyboardMarkup()
    btn2 = types.InlineKeyboardButton('Clear chat', callback_data = 'delete')
    markup.add(btn2)
    #bot.reply_to(message, "Chat cleared", reply_markup=markup)

@bot.callback_query_handler(func= lambda callback: True)
def callback_message(callback):
    if callback.data == 'delete':
       bot.delete_message(callback.message.chat.id, callback.message.message_id - 2)

bot.infinity_polling()