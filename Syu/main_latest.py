import telebot, requests, random, datetime, time, math, threading, json
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from datetime import timedelta

bot = telebot.TeleBot("6430764623:AAGZ_y2t8OZh3AVit68xwLkrSrZZMqXYbHQ")
restaurant = []
home = []
setting_home = False
picker = False
user_options = {}
reminder_list = []
reminder_data = {}
tasks = []
completed_tasks = []
curriculum = ['no class','no class','no class','no class','no class','no class','no class']

words_ = [
    ("abrupt", "突然的"),
    ("benevolence", "仁慈"),
    ("coherence", "連貫性"),
    ("debilitate", "使衰弱"),
    ("elaborate", "詳細說明"),
    ("fluctuation", "波動"),
    ("gregarious", "群居的"),
    ("hypothesis", "假設"),
    ("indispensability", "不可或缺"),
    ("judiciousness", "明智"),
    ("keen", "敏銳的"),
    ("lucidity", "清晰"),
    ("meticulousness", "謹慎"),
    ("novelty", "新穎"),
    ("obstinacy", "固執"),
    ("pragmatism", "務實主義"),
    ("quintessence", "精髓"),
    ("resilience", "彈性"),
    ("scrutinize", "仔細檢查"),
    ("tangibility", "有形"),
    ("unanimity", "一致"),
    ("versatility", "多才多藝"),
    ("whimsy", "異想天開"),
    ("xenophobia", "排外"),
    ("yield", "產生"),
    ("zealousness", "熱心"),
    ("adversity", "逆境"),
    ("belligerence", "好戰"),
    ("compel", "強迫"),
    ("diligence", "勤奮"),
    ("empathize", "同情"),
    ("fortitude", "堅韌"),
    ("holism", "整體論"),
    ("imperative", "必要的"),
    ("jubilate", "歡欣鼓舞"),
    ("kinetics", "運動學"),
    ("lamentation", "哀悼"),
    ("magnitude", "重要性"),
    ("negligence", "疏忽"),
    ("obsolescence", "過時"),
    ("periphery", "周邊"),
    ("quaintness", "古雅"),
    ("rejuvenation", "恢復活力"),
    ("substantiate", "證實"),
    ("tenacity", "頑強"),
    ("ubiquity", "無所不在"),
    ("vigilance", "警惕"),
    ("wistfulness", "渴望"),
    ("xenial", "好客的"),
    ("yearn", "渴望"),
    ("zephyr", "微風"),
    ("astuteness", "機敏"),
    ("benevolence", "仁慈"),
    ("cognition", "認識"),
    ("dormancy", "休眠"),
    ("ephemerality", "短暫"),
    ("fastidiousness", "挑剔"),
    ("garrulity", "喋喋不休"),
    ("haphazardness", "隨意"),
    ("immutability", "不可變"),
    ("juxtaposition", "並列"),
    ("luminosity", "發光"),
    ("magnanimity", "寬宏大量"),
    ("nuance", "細微差別"),
    ("ostracism", "排擠"),
    ("prolificacy", "多產"),
    ("quintessence", "精髓"),
    ("reticence", "沉默"),
    ("solicitude", "關心"),
    ("tranquility", "寧靜"),
    ("unprecedented", "前所未有的"),
    ("vindication", "辯護"),
    ("wariness", "謹慎"),
    ("xenon", "氙"),
    ("yoke", "軛"),
    ("zealousness", "熱心"),
    ("abandon", "放棄"),
    ("benefit", "利益"),
    ("calculate", "計算"),
    ("delight", "高興"),
    ("enormous", "巨大的"),
    ("fascinate", "迷住"),
    ("genuine", "真正的"),
    ("harmony", "和諧"),
    ("identify", "識別"),
    ("justify", "辯護"),
    ("knowledge", "知識"),
    ("liberty", "自由"),
    ("magnitude", "大小"),
    ("navigate", "導航"),
    ("objective", "目標"),
    ("participate", "參與"),
    ("question", "問題"),
    ("reliable", "可靠的"),
    ("satisfy", "滿足"),
    ("thorough", "徹底的"),
    ("unique", "獨特的"),
    ("various", "各種各樣的"),
    ("wonder", "驚奇"),
    ("youth", "青春"),
    ("zeal", "熱情")
]

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

def loc_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton('restaurant', callback_data="restaurant"),
                InlineKeyboardButton('get_live_location', callback_data="get_live_location"))
    return markup

def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton('choose', callback_data="choice"))
    return markup

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

def get_daily_words():
    random_numbers = [random.randint(0, 100) for _ in range(5)]
    result = ""
    for i in range(5):
        result += f"{str(" ".join([i for i in random.choice(words_)]))}\n"
    return result

def send_daily_words():
    daily_words = get_daily_words()
    res = "\n".join([f"{word[0]} - {word[1]}" for word in daily_words])
    return res

def seconds_until_tomorrow_8am():
    now = datetime.datetime.now()
    tomorrow_8am = datetime.datetime.combine(now.date() + timedelta(days=1), datetime.datetime.min.time()) + timedelta(hours=8)
    return (tomorrow_8am - now).total_seconds()

def daily_task():
    while True:
        time.sleep(seconds_until_tomorrow_8am())
        send_daily_words()

@bot.message_handler(commands=['help', 'start'])
def get_help(message):
    bot.send_message(chat_id=message.chat.id, text = "\"/help\"以取得幫助\n\"/aqi\"以取得空氣品質\n\"/weather\"以取得未來36小時天氣預報\n傳送位置以取得 10 公里內的餐廳\n\"/daily_words\"啟用每日推播 5 單字\n\"/words\"以獲得額外 5 單字\n\"/lists\"以使用 to do list\n\"/picker\"以使用轉盤\n\"/reminder\"以使用設定提醒\n\"/curriculum\"以使用課表")

@bot.message_handler(commands=['aqi'])
def get_aqi(message):
    aqi_url = 'https://data.moenv.gov.tw/api/v2/aqx_p_432?api_key=e8dd42e6-9b8b-43f8-991e-b3dee723a52d&limit=1000&sort=ImportDate%20desc&format=JSON'
    aqi_data = requests.get(aqi_url, verify = False).json()
    for i in aqi_data['records']:
        if i['county'] == "新竹市":
            bot.send_message(chat_id=message.chat.id, text=f"{i['county']}, {i['sitename']}, AQI:{i['aqi']}, 空氣品質{i['status']}")

@bot.message_handler(commands=['weather'])
def get_weather(message):
    weather_url = 'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=CWA-44D2B087-21D1-4DB1-8F43-52A76EC011D1&format=JSON&locationName=%E6%96%B0%E7%AB%B9%E5%B8%82'
    weather_data = requests.get(weather_url).json()
    l = []
    for i in weather_data["records"]["location"][0]["weatherElement"][0]["time"]:
        l.append(f"{i['startTime']}~{i['endTime']}:{i['parameter']['parameterName']}")
    bot.send_message(message.chat.id, f"{weather_data['records']['datasetDescription']} - {weather_data['records']['location'][0]['locationName']}\n{'\n'.join(l)}")

@bot.message_handler(content_types=['location'])
def handle_location(message):
    location = f"{message.location.latitude},{message.location.longitude}"
    api_key = "AIzaSyC-1IY3lBsBYe69TBq6Gsuq1WIiQzC4ANs"    
    nearby_url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location}&radius=10000&type=restaurant&language=zh-TW&key={api_key}"
    res = requests.get(url=nearby_url).json()
    
    data = []
    for i in res["results"]:
        distance_url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={location}&destinations=place_id:{i['place_id']}&key={api_key}"
        r = requests.get(distance_url).json()
        
        restaurant_info = (
            f"{i['name']}\n"
            f"{i['vicinity']}\n"
            f"{i['rating']} 顆星 ({i['user_ratings_total']})\n"
            f"距離：{r['rows'][0]['elements'][0]['distance']['text']}\n"
        )
        data.append(restaurant_info)
    global restaurant
    restaurant = data
    response_text = f"10公里內的餐廳店家有：\n\n" + "\n".join(data) + "\n可點擊\'choose\'隨機選出一間"
    bot.send_message(message.chat.id, response_text, reply_markup=gen_markup())

@bot.callback_query_handler(func=lambda call: True)
def callback_choice(call):
    bot.send_message(call.message.chat.id, random.choice(restaurant), reply_markup=gen_markup())

@bot.message_handler(commands=['daily_words'])
def start(message):
    bot.reply_to(message, "You have subscribed to daily word push !")

@bot.message_handler(commands=['words'])
def words(message):
    text = get_daily_words()
    bot.reply_to(message, text)

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
    bot.reply_to(message, f"Option added: {message.text}\nContinue entering other options, or type /done to finish.")

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

@bot.message_handler(commands=['reminder'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Hi there! I can help you set reminders.😄📋 \nUse /add to add a new reminder or /reminderlist to see your reminders.")

@bot.message_handler(commands=['add'])
def add_reminder(message):
    # 
    msg = bot.send_message(message.chat.id, "Please enter your reminder message 💭")
    # 
    bot.register_next_step_handler(msg, process_reminder_message)

def process_reminder_message(message):
    chat_id = message.chat.id
    reminder_data[chat_id] = {'message': message.text}  # 

    markup = InlineKeyboardMarkup()
    markup.row_width = 3
    markup.add(
        InlineKeyboardButton("🔔 Important", callback_data="🔔 Important"),
        InlineKeyboardButton("🚨 Emergency", callback_data="🚨 Emergency"),
        InlineKeyboardButton("🌻 Daily", callback_data="🌻 Daily")
    )
    bot.send_message(chat_id, "Please select the importance:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data in ["🔔 Important", "🚨 Emergency", "🌻 Daily"])
def callback_importance(call):
    chat_id = call.message.chat.id
    reminder_data[chat_id]['importance'] = call.data  
    bot.send_message(chat_id, "Please enter the reminder time in the format: YYYY-MM-DD HH:MM.")
    bot.register_next_step_handler_by_chat_id(chat_id, process_reminder_time)

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



@bot.message_handler(commands=["lists"])
def send_welcome(message):
    bot.reply_to(message, """Hello, do you need a list?
Use /add_to_do_list to add an object to the list
Use /print to see the whole list
Use /del to delete an object
Use /done to mark an item as completed
Use /rate to see your completion rate""")

@bot.message_handler(commands=["add_to_do_list"])
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

@bot.message_handler(commands=["print"])
def print_list(message):
    global tasks, completed_tasks
    if tasks:
        bot.reply_to(message, f"Tasks: {tasks}\nCompleted Tasks: {completed_tasks}")
    else:
        bot.reply_to(message, "The task list is empty.")

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

@bot.message_handler(commands=["rate"])
def rate_list(message):
    global tasks, completed_tasks
    total_tasks = len(tasks) + len(completed_tasks)
    if total_tasks == 0:
        completion_rate = 0
    else:
        completion_rate = (len(completed_tasks) / total_tasks) * 100
    bot.reply_to(message, f"Your completion rate is {completion_rate:.2f}%")

task_thread = threading.Thread(target=daily_task)
task_thread.start()

print("bot online")
bot.infinity_polling()
