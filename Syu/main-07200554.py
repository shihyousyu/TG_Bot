import telebot
import requests
import random
import time
from telebot.types import Message
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


bot = telebot.TeleBot("6430764623:AAE06hxXPRqmKb180h7FRu3QWctRQHWZrjA")
restaurant = []
home = []
setting_home = False

def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton('choose', callback_data="choice"))
    return markup

@bot.message_handler(commands=['help', 'start'])
def get_help(message):
    bot.send_message(chat_id=message.chat.id, text="\"/help\"以取得幫助\n\"/aqi\"以取得空氣品質\n\"/weather\"以取得未來36小時天氣預報\n傳送位置以取得 10 公里內的餐廳\n\"/home\"以設定家的位置")

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
    global home, setting_home
    if setting_home:
        home = (message.location.latitude, message.location.longitude)
        setting_home = False
        bot.send_message(chat_id=message.chat.id, text="家的位置已設定成功！")
    else:
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

@bot.message_handler(commands=['choice'])
def get_choice(message):
    try:
        bot.send_message(chat_id=message.chat.id, text=choose(restaurant), reply_markup=gen_markup())
    except:
        bot.send_message(chat_id=message.chat.id, text='沒有店家')

@bot.message_handler(commands=['home'])
def request_home_location(message):
    global setting_home
    setting_home = True
    bot.send_message(chat_id=message.chat.id, text="請傳送你的位置以設定家的位置。")

@bot.callback_query_handler(func=lambda call: True)
def callback_choice(call):
    bot.send_message(call.message.chat.id, random.choice(restaurant), reply_markup=gen_markup())

print("bot online")
bot.infinity_polling()