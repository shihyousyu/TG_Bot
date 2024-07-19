import telebot
import datetime
curriculum=[
'國文, 數學, 公民, 歷史, 物理, 英文, 化學, 地科',
'數學, 公民, 歷史, 物理, 英文, 化學, 地科, 國文',
'公民, 歷史, 物理, 英文, 化學, 地科, 國文, 數學',
'歷史, 物理, 英文, 化學, 地科, 國文, 數學, 公民',
'物理, 英文, 化學, 地科, 國文, 數學, 公民, 歷史'
]
bot = telebot.TeleBot('7157007495:AAEfts9nkfVzWQSYIytVZ-CsBl7Jp1loDcQ')


@bot.message_handler(commands = ['class'])
def function_name(message):
    week=datetime.datetime.now()
    weekend=week.weekday()
    #now_hour=datetime.datetime.now().hour
    bot.reply_to(message,curriculum[weekend])

bot.infinity_polling()
