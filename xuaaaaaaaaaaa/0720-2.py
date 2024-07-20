import telebot
import random
import time
from datetime import datetime, timedelta
from threading import Thread

API_TOKEN = '7434794125:AAGkODMCfLm-XaGwZLH7V5LtRCV9aho4s0s'

bot = telebot.TeleBot(API_TOKEN)

# 单词表
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

# 用户ID列表
subscribed_users = []

# 选择5个单词
def get_daily_words():
    random_numbers = [random.randint(0, 100) for _ in range(5)]
    result = ""
    for i in range(5):
        result += f"{str(" ".join([i for i in random.choice(words_)]))}\n"
    return result
get_daily_words()
# 发送每日单词
def send_daily_words():
    daily_words = get_daily_words()
    message = "\n".join([f"{word[0]} - {word[1]}" for word in daily_words])
    for user_id in subscribed_users:
        bot.send_message(user_id, message)

# 处理 /start 命令
@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.id not in subscribed_users:
        subscribed_users.append(message.chat.id)
        bot.reply_to(message, "You have subscribed to daily word push !")

@bot.message_handler(commands=['words'])
def words(message):
    text = get_daily_words()
    bot.reply_to(message, text)


# 计算距离明天8点的秒数
def seconds_until_tomorrow_8am():
    now = datetime.now()
    tomorrow_8am = datetime.combine(now.date() + timedelta(days=1), datetime.min.time()) + timedelta(hours=8)
    return (tomorrow_8am - now).total_seconds()

# 定时任务
def daily_task():
    while True:
        # 等待到明天早上8点
        time.sleep(seconds_until_tomorrow_8am())
        send_daily_words()

# 启动定时任务线程
task_thread = Thread(target=daily_task)
task_thread.start()

# 运行bot
bot.infinity_polling()
