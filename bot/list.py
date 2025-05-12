import telebot
from datetime import datetime
import json

TOKEN = "7244810771:AAFmORh_BFexyGrj26AuCFzTMhxBU189BTE"
bot = telebot.TeleBot(TOKEN, parse_mode=None)

# 使用两个列表来分别保存任务和已完成的任务
tasks = []
completed_tasks = []

@bot.message_handler(commands=["lists"])
def send_welcome(message):
    bot.reply_to(message, """Hello, do you need a list?
Use /add_list to add an object to the list
Use /print to see the whole list
Use /del to delete an object
Use /done to mark an item as completed
Use /rate to see your completion rate""")

@bot.message_handler(commands=["add_list"])
def add_list(message):
    global tasks
    task = message.text[5:]
    if task:
        tasks.append(task)
        bot.reply_to(message, f"Added: {task}")
    else:
        bot.reply_to(message, "Please provide an item to add.")

@bot.message_handler(commands=["del"])
def del_list(message):
    global tasks
    task = message.text[5:]
    if task in tasks:
        tasks.remove(task)
        bot.reply_to(message, f"Deleted: {task}")
    else:
        bot.reply_to(message, "Item not found in the list.")

@bot.message_handler(commands=["done"])
def done_list(message):
    global tasks, completed_tasks
    task = message.text[6:]
    if task in tasks:
        tasks.remove(task)
        completed_tasks.append(task)
        bot.reply_to(message, f"Marked as completed: {task}")
    else:
        bot.reply_to(message, "Item not found in the list.")

@bot.message_handler(commands=["print"])
def print_list(message):
    global tasks, completed_tasks
    if tasks:
        bot.reply_to(message, f"Tasks: {tasks}\nCompleted Tasks: {completed_tasks}")
    else:
        bot.reply_to(message, "The task list is empty.")

@bot.message_handler(commands=["rate"])
def rate_list(message):
    global tasks, completed_tasks
    total_tasks = len(tasks) + len(completed_tasks)
    if total_tasks == 0:
        completion_rate = 0
    else:
        completion_rate = (len(completed_tasks) / total_tasks) * 100
    bot.reply_to(message, f"Your completion rate is {completion_rate:.2f}%")

@bot.message_handler(commands=['export'])
def export_food_list(message):
    try:
        with open('lists.json', 'w') as file:
            json.dump({'tasks': tasks, 'completed_tasks': completed_tasks}, file, indent=4)
        bot.reply_to(message, "Task list has been successfully exported to lists.json.")
    except Exception as e:
        bot.reply_to(message, f"An error occurred while exporting the task list: {e}")

@bot.message_handler(commands=['import'])
def import_food_list(message):
    global tasks, completed_tasks
    try:
        with open('lists.json', 'r') as file:
            data = json.load(file)
            tasks = data.get('tasks', [])
            completed_tasks = data.get('completed_tasks', [])
        bot.reply_to(message, "Task list has been successfully imported from lists.json.")
    except FileNotFoundError:
        bot.reply_to(message, "No lists.json file found. Please export a task list first.")
    except Exception as e:
        bot.reply_to(message, f"An error occurred while importing the task list: {e}")

@bot.message_handler(command=['aaa'])
def callback_choice(message):
    bot.send_message(message.chat.id, text = '5')

bot.infinity_polling()