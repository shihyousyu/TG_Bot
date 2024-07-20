import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
import math

# Replace with your bot's API token
TOKEN = 'telegram token'

bot = telebot.TeleBot(TOKEN)

# Dictionary to store options
user_options = {}

# List of random emojis
emojis = [
    "🐶", "🐱", "👄", "🌺", "🐰", "🍧", "🐻", "🎄", "🐨", "🐯",
    "🐸", "🐵", "🐔", "🐧", "🐦", "🐤", "🐣", "🐺", "🦋", "🥥",
    "🐢", "🐍", "🦎", "🐙", "🦑", "🦐", "🛸", "🦀", "🐡", "🐠",
    "🐟", "🎀", "🐳", "🩹", "🦈", "🦭", "🐊", "🐅", "🚗", "🦓",
    "🐘", "🦏", "🦛", "🐪", "🐫", "🦒", "🍄", "🦬", "🐃", "🏈",
    "🍎", "🍊", "🪅", "🍉", "🎧", "🍓", "🍒", "🍍", "🥭", "🥝",
    "🍅", "🍆", "🥑", "🥦", "🧩", "🥒", "🎮", "🌽", "🥕", "🏝️",
    "🧅", "🥔", "📷", "🥐", "🥯", "🍞", "🥖", "🥨", "🧀", "🍗",
    "🍖", "🍤", "🍳", "🥚", "🍔", "🍟", "🍕", "🌭", "🥪", "🌮",
    "🌯", "👒", "🥘", "🧼", "🧬", "🥎", "🧸", "🗿", "🌞", "🧤"
]

@bot.message_handler(commands=['picker']) #type in /picker 
def send_welcome(message):
    bot.reply_to(message, "Need a fun random picker? StraightABot can help you!😉🎲")
    bot.send_message(message.chat.id, "Please start entering your options, one option per message. Type /done to finish entering options.")
@bot.message_handler(commands=['done'])
def stop_input(message):
    chat_id = message.chat.id
    options = user_options.get(chat_id, [])
    if not options:
        bot.reply_to(message, "You haven't entered any options yet. Please start entering your options.")
        return

    random.shuffle(options)
    markup = InlineKeyboardMarkup()
    buttons_per_row = math.ceil(math.sqrt(len(options)))
    for i in range(0, len(options), buttons_per_row):
        row = []
        for j in range(i, min(i + buttons_per_row, len(options))):
            emoji = random.choice(emojis)
            row.append(InlineKeyboardButton(text=f"{emoji} Option {j+1}", callback_data=f"choose_{j}"))
        markup.add(*row)
    markup.add(InlineKeyboardButton(text="🎲 StraightAFerret Randomly Choose", callback_data="choose_random"))
    bot.send_message(chat_id, "Choose an option or let me randomly choose one for you:", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_options(message):
    chat_id = message.chat.id
    if message.text.lower() == '/done':
        stop_input(message)
        return

    if chat_id not in user_options:
        user_options[chat_id] = []
    user_options[chat_id].append(message.text)
    bot.reply_to(message, f"Option added: {message.text}\nContinue entering other options, or type /stop to finish.")

@bot.callback_query_handler(func=lambda call: call.data.startswith('choose_'))
def handle_query(call):
    chat_id = call.message.chat.id
    options = user_options.get(chat_id, [])
    if not options:
        bot.answer_callback_query(call.id, "No options available. Please start entering your options.")
        return

    if call.data == 'choose_random':
        index = random.randint(0, len(options) - 1)
    else:
        index = int(call.data.split('_')[1])
   
    chosen_option = options[index]
    bot.answer_callback_query(call.id, f"🗣️ You have chosen: {chosen_option}❗", show_alert=True)
    bot.send_message(chat_id, f"🗣️ You have chosen: {chosen_option}❗")

bot.polling()