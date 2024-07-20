import telebot
import datetime
curriculum = []
bot = telebot.TeleBot('7157007495:AAEfts9nkfVzWQSYIytVZ-CsBl7Jp1loDcQ')

@bot.message_handler(commands=['add'])
def add_food(message):
    bot.reply_to(message, "Okay")
    del curriculum [int((message.text[5])-1)]
    curriculum.insert((int(message.text[5])) - 1, message.text[6:])

@bot.message_handler(commands=['delete'])
def add_food(message):
        bot.reply_to(message, "Okay")
        del curriculum [int((message.text[7:])-1)]
        curriculum.insert [int((message.text[7:])-1),int('no class')]

@bot.message_handler(commands=['list'])
def list_food(message):
    bot.reply_to(message, f"now curriculum: {curriculum}")

@bot.message_handler(commands = ['class'])
def function_name(message):
    week=datetime.datetime.now()
    weekend=week.weekday()
    bot.reply_to(message,curriculum[weekend])

bot.infinity_polling()
