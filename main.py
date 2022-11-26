from datetime import date, datetime ,timedelta
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()+timedelta(hours=8)
# start_date = os.environ['START_DATE']
start_date = '2020-07-17'
city = os.environ['CITY']
# birthday = os.environ['BIRTHDAY']
# birthday2 = os.environ['BIRTHDAY2']
birthday  = '2022-07-17'
birthday2 = '2022-10-14'
app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_ids = os.environ["USER_ID"].split("\n")
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp']), math.floor(weather['high']), math.floor(weather['low'])

def get_count(aa):
  bb = datetime.strptime(aa, '%Y-%m-%d')
  interval = datetime.now() - bb
  return interval.days


def get_birthday(a):
  a = datetime.strptime(a, '%Y-%m-%d')
  interval = a - datetime.now()
  return interval.days


def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


def get_wea_war():
  tem_wea, tem_a, tem_b, tem_c = get_weather()
  if str(tem_wea) == "晴":
    return "可能有点晒,记得带把伞"
  elif str(tem_wea) == "阴":
    return "天气不错,出去走走⑧"
  else:
    return "要是下雨记得带伞捏"

# 获取星期
def getWeek():
    w = datetime.now().strftime('%w')
    data = {
        0: '天,要上日语课欸！',
        1: '一欸',
        2: '二欸',
        3: '三欸',
        4: '四欸，要不要疯狂星期四呀~',
        5: '五欸',
        6: '六欸'
    }
    return data[int(w)]


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature, highest, lowest = get_weather()
now_year = today.year
now_month = today.month
now_day = today.day
data = {"weather_warning":{"value": get_wea_war(), "color":get_random_color()},
        "date_D":{"value":now_day, "color":get_random_color()},
        "date_M":{"value":now_month, "color":get_random_color()},
        "date_Y":{"value":now_year, "color":get_random_color()},
        "weather":{"value":wea,"color":get_random_color()},
        "temperature":{"value":temperature,"color":get_random_color()},
        "love_days":{"value":get_count(start_date),"color":get_random_color()},
        "birthday_left":{"value":get_birthday(birthday),"color":get_random_color()},
        "birthday_left2":{"value":get_birthday(birthday2),"color":get_random_color()},
        "words":{"value":get_words(),"color":get_random_color()},
        "highest": {"value":highest,"color":get_random_color()},
        "lowest":{"value":lowest, "color":get_random_color()},
        "city":{"value":city, "color":get_random_color()},
        "week":{"value":getWeek(),"color":get_random_color()},
        }

count = 0
for user_id in user_ids:
  res = wm.send_template(user_id, template_id, data)
  count+=1

print("发送了" + str(count) + "条消息")
