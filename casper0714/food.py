import telebot
from datetime import datetime
import json

TOKEN = "7404236278:AAFMNq6TCG9nQekXO2r_nmoN2BSAkUqkc9Y"
bot = telebot.TeleBot(TOKEN, parse_mode= None)

number=0
number2=0
lists= []
@bot.message_handler(commands = ["lists"])
def send_welcome(message):
    bot.reply_to(message, f"Hello, do you need a list? \
                            \nUse /add to tell me add a objecct in list\
                            \nUse /print to see the whole list\
                            \nUse /del to delete a object\
                            \nUse /don to completion a list\
                            \nUse /rate to look your completion rate")

    
@bot.message_handler(commands = ["add"])
def add_list(message):
    bot.reply_to(message, "OK")
    lists.append(message.text[5:])
number+=1
print(number)    
    
@bot.message_handler(commands = ["del"])
def del_list(message):
    bot.reply_to(message, "Got it")
    lists.remove(message.text[5:])

    
@bot.message_handler(commands = ["don"])
def done_list(message):
    bot.reply_to(message, "OKay")
    lists.remove(message.text[5:])    
number2+=1
print(number2)

@bot.message_handler(commands = ["print"])
def lists_list(message):
    bot.reply_to(message, f"Here is the food list: {lists}")
    
@bot.message_handler(commands = ["rate"])
def rate_list(message):
    bot.reply_to(message, f"your completion rate is {(number2/number)*100}%")
    
@bot.message_handler(commands=['export'])
def export_food_list(message):
    try:
        with open('lists.json', 'w') as file:
            json.dump(lists, file, indent=4)
        bot.reply_to(message, "Food list has been successfully exported to lists.json.")
    except Exception as e:
        bot.reply_to(message, f"An error occurred while exporting the food list: {e}")
        
@bot.message_handler(commands=['import'])
def import_food_list(message):
    try:
        with open('lists.json', 'r') as file:
            imported_lists = json.load(file)
            global lists
            lists = imported_lists
        bot.reply_to(message, "Food list has been successfully imported from lists.json.")
    except FileNotFoundError:
        bot.reply_to(message, "No lists.json file found. Please export a food list first.")
    except Exception as e:
        bot.reply_to(message, f"An error occurred while importing the food list: {e}")
        
bot.infinity_polling()


