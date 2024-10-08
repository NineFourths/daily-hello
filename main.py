from datetime import date, datetime ,timedelta
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()+timedelta(hours=8)
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']
birthday2 = os.environ['BIRTHDAY2']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_ids = os.environ["USER_ID"].split("\n")
template_id = os.environ["TEMPLATE_ID"]

r1 = []


def get_weather():
  url = "https://devapi.qweather.com/v7/weather/3d?lang=cn&gzip=n&location=101010700&key=300db3a6b17447f7bbf92aca06a6aee3"
  res = requests.get(url).json()
  tempMax = res['daily'][0]['tempMax']
  tempMin = res['daily'][0]['tempMin']

  url = "https://devapi.qweather.com/v7/weather/now?lang=cn&gzip=n&location=cn101010700&key=300db3a6b17447f7bbf92aca06a6aee3"
  res = requests.get(url).json()
  text = res['now']['text']
  temp = res['now']['temp']

  return text, int(temp), int(tempMax), int(tempMin)

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
    if ( (next - today).days == -1 ):
        return "就是今天!!!"
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

  # url = "https://devapi.qweather.com/v7/weather/now?lang=cn&gzip=n&location=cn101280102&key=300db3a6b17447f7bbf92aca06a6aee3"
  # res = requests.get(url).json()
  # text = res['now']['text']
  # return text

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)

def get_birthday2():
  next = datetime.strptime(str(date.today().year) + "-" + birthday2, "%Y-%m-%d")
  if next < datetime.now():
      next = next.replace(year=next.year + 1)
      if ((next - today).days == -1):
          return "就是今天!!!"
  return (next - today).days

def get_wea_war():
  tem_wea, tem_a, tem_b, tem_c = get_weather()
  if str(tem_wea) == "晴":
    return "可能有点晒,记得带把伞"
  elif str(tem_wea) == "阴":
    return "天气不错,出去走走⑧"
  else:
    return "要是下雨记得带伞捏"

def slice_love_words():
    s1 = get_words()
    maxLen = 19
    maxList = 6
    for i in range(len(s1)):
        if i % maxLen == 0 and i != 0:
            r1.append(s1[i - maxLen: i])
    t = len(s1) % maxLen
    r1.append(s1[len(s1) - t:])
    if len(r1) < maxList:
        for i in range(maxList - len(r1)):
            r1.append('')

def get_slice_words(cnt):
    return r1[cnt]


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature, highest, lowest = get_weather()
now_year = today.year
now_month = today.month
now_day = today.day
slice_love_words()
data = {
        # "weather_warning":{"value": get_wea_war(), "color":get_random_color()},
        "date_D":{"value":now_day, "color":get_random_color()},
        "date_M":{"value":now_month, "color":get_random_color()},
        "date_Y":{"value":now_year, "color":get_random_color()},
        "weather":{"value":wea,"color":get_random_color()},
        "temperature":{"value":temperature,"color":get_random_color()},
        "love_days":{"value":get_count(),"color":get_random_color()},
        "birthday_left":{"value":get_birthday(),"color":get_random_color()},
        "birthday_left2":{"value":get_birthday2(),"color":get_random_color()},
        "words":{"value":get_words(),"color":get_random_color()},
        "highest": {"value":highest,"color":get_random_color()},
        "lowest":{"value":lowest, "color":get_random_color()},
        "city":{"value":city, "color":get_random_color()},
        "words0":{"value":get_slice_words(0),"color":get_random_color()},
        "words1":{"value":get_slice_words(1),"color":get_random_color()},
        "words2":{"value":get_slice_words(2),"color":get_random_color()},
        "words3":{"value":get_slice_words(3),"color":get_random_color()},
        "words4":{"value":get_slice_words(4),"color":get_random_color()},
        "words5":{"value":get_slice_words(5),"color":get_random_color()},
        }

count = 0
for user_id in user_ids:
  res = wm.send_template(user_id, template_id, data)
  count+=1

print("发送了" + str(count) + "条消息")
