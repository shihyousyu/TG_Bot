import telebot
import datetime
curriculum=[]
bot = telebot.TeleBot('6430764623:AAE06hxXPRqmKb180h7FRu3QWctRQHWZrjA')

@bot.message_handler(commands=['add'])
def add_food(message):
    bot.reply_to(message, "Okay")
    curriculum.append(message.text[4:])

@bot.message_handler(commands=['list'])
def list_food(message):
    bot.reply_to(message, f"now curriculum: {curriculum}")

@bot.message_handler(commands = ['class'])
def function_name(message):
    week=datetime.datetime.now()
    weekend=week.weekday()
    bot.reply_to(message,curriculum[weekend])

bot.infinity_polling()
