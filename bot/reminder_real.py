import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import datetime
import threading

TOKEN = "7243816280:AAHDIEAJgeZXl3QX6T1GtPTUe05q6VQKTu0"
bot = telebot.TeleBot(TOKEN, parse_mode=None)  # 

reminder_list = []  # 
reminder_data = {}  # 

@bot.message_handler(commands=['reminder'])  # 
def send_welcome(message):
    # 
    bot.send_message(message.chat.id, "Hi there! I can help you set reminders.😄📋 \nUse /add to add a new reminder or /reminderlist to see your reminders.")

@bot.message_handler(commands=['add'])  # 
def add_reminder(message):
    # 
    msg = bot.send_message(message.chat.id, "Please enter your reminder message 💭")
    # 
    bot.register_next_step_handler(msg, process_reminder_message)

def process_reminder_message(message):
    chat_id = message.chat.id
    reminder_data[chat_id] = {'message': message.text}  # 

    # 
    markup = InlineKeyboardMarkup()
    markup.row_width = 3
    markup.add(
        InlineKeyboardButton("🔔 Important", callback_data="🔔 Important"),
        InlineKeyboardButton("🚨 Emergency", callback_data="🚨 Emergency"),
        InlineKeyboardButton("🌻 Daily", callback_data="🌻 Daily")
    )

    # 
    bot.send_message(chat_id, "Please select the importance:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ["🔔 Important", "🚨 Emergency", "🌻 Daily"])
def callback_importance(call):
    chat_id = call.message.chat.id
    reminder_data[chat_id]['importance'] = call.data  
    bot.send_message(chat_id, "Please enter the reminder time in the format: YYYY-MM-DD HH:MM.")
    bot.register_next_step_handler_by_chat_id(chat_id, process_reminder_time)

def process_reminder_time(message):
    chat_id = message.chat.id
    reminder_time_str = message.text

    try:
        # 
        reminder_datetime = datetime.datetime.strptime(reminder_time_str, '%Y-%m-%d %H:%M')
    except ValueError:
        # 
        now = datetime.datetime.now()
        reminder_datetime = datetime.datetime.combine(now.date() + datetime.timedelta(days=1), datetime.time(8, 0))

    reminder_data[chat_id]['time'] = reminder_datetime  


    reminder = (chat_id, reminder_data[chat_id]['message'], reminder_data[chat_id]['importance'], reminder_data[chat_id]['time'])
    reminder_list.append(reminder)

    
    bot.send_message(chat_id, f'Reminder set for {reminder_datetime} with importance {reminder_data[chat_id]["importance"]}.')

    
    delay = (reminder_datetime - datetime.datetime.now()).total_seconds()  
    threading.Timer(delay, send_reminder, args=[reminder]).start()  

    
    del reminder_data[chat_id]

def send_reminder(reminder):
    chat_id, reminder_message, importance, reminder_datetime = reminder  
    
    bot.send_message(chat_id, f'Reminder: {reminder_message}\nImportance: {importance}')

@bot.message_handler(commands=['reminderlist'])  
def list_reminders(message):
    if not reminder_list:
        
        bot.send_message(message.chat.id, "You have no reminders set.")
    else:
        reminders = []
        for reminder in reminder_list:
            chat_id, reminder_message, importance, reminder_datetime = reminder
            if chat_id == message.chat.id:
                
                reminders.append(f'{reminder_message} at {reminder_datetime.strftime("%Y-%m-%d %H:%M")} (Importance: {importance})')
        if reminders:
            
            bot.send_message(message.chat.id, "\n".join(reminders))
        else:
            bot.send_message(message.chat.id, "You have no reminders set.")

@bot.message_handler(command=['aaa'])
def callback_choice(message):
    bot.send_message(message.chat.id, text = '3')

bot.polling() 
