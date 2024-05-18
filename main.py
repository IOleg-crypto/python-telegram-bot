import telebot

#token to connect bot
bot = telebot.TeleBot('6895824327:AAEyCfrTRh-7wGuIjrAVSe9y2gXxx1Vpunk') 

@bot.message_handler(commands=['start' , 'hello'])

def main(message):
    bot.send_message(message.chat.id, 'Hello, ' + message.from_user.first_name)
   
@bot.message_handler(commands=['setnumber'])

def setnumber(message):
    bot.send_message(message.chat.id, 5)
   
bot.polling(none_stop=True)