# 更新说明

## 2022.08.22

1. 增加天气范围（最高温、最低温）
2. 支持多个接收人
3. 所有字段都是彩色的

示例模板：

今天是 {{date_Y.DATA}} 年 {{date_M.DATA}} 月 {{date_D.DATA}} 日

今天天气：{{weather.DATA }}
{{weather_warning.DATA }}

当前温度：{{ temperature.DATA }} ℃

今日{{city.DATA}}气温：{{ lowest.DATA }} ℃ ~ {{ highest.DATA }} ℃

我们已经在一起 {{ love_days.DATA }} 天啦

距离ddb的生日还有：{{ birthday_left.DATA }} 天

距离fk的生日还有：{{ birthday_left2.DATA }} 天

{{ words.DATA }}
