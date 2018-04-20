#! coding:utf8

"""

    　爬取会议列表: "https://www.aminer.cn/ranks/conf"

"""


import re
import requests
import json

html = requests.get("https://api.aminer.cn/api/rank/conf/list/1").text

data = json.loads(html)

confs = data['list']

for data in confs:

    x = [data['FULL_NAME'], data['SHORT_NAME'], data['H5']]

    # 信息不完整的不要
    if x[0] == "" or x[1] == "" or x[2] == "":
        continue

    print x
