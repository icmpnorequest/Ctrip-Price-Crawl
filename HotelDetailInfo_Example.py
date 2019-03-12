import requests
import json
from lxml import etree
import csv
from bs4 import BeautifulSoup
import re
import numpy as np
import pandas as pd

import requests.packages.urllib3.util.ssl_
# print(requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS)
# requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'

pd.set_option('display.max_columns', 10000)
pd.set_option('display.max_rows', 10000)
pd.set_option('display.max_colwidth', 10000)
pd.set_option('display.width',1000)


url="http://hotels.ctrip.com/Domestic/tool/AjaxHote1RoomListForDetai1.aspx?hotel=6147365"
headers = {"Connection":"keep-alive",
          "Accept-Language":"zh-CN,zh;q=0.9",
          "Cache-Control":"max-age=0",
          "Content-Type":"application/x-www-form-urlencoded; charset=utf-8",
          "Host": "hotels.ctrip.com",
          "If-Modified-Since": "Thu, 01 Jan 1970 00:00:00 GMT",
          "Referer": "http://hotels.ctrip.com/hotel/2231618.html",
          "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/69.0.3497.92 Safari/537.36"
}

r = requests.get(url,headers=headers)
# html=json.loads(html.text)
# Response is a json object.
html = r.json()['html']
# print(html)
soup = BeautifulSoup(html, "lxml")
# print(soup.prettify())
rooms = soup.findAll('td', attrs={"class":"child_name J_Col_RoomName"})
# print(rooms)
# print(type(rooms[0]))
# <class 'bs4.element.Tag'>

RoomID = []
RoomName = []
LowPrice = []
RoomSize = []
RoomLevel = []
IsSmoking = []
BedSize = []
IsAddBed = []
CustomerNum = []

baseroom_pattern = re.compile(r'<[^>]+>')   # r'<[^>]+>'

for idx in range(len(rooms)):
    if rooms[idx].has_attr(key='data-baseroominfo'):
        room_info_str = rooms[idx]['data-baseroominfo']

        ## Error
        # TypeError String indices must be integers

        room_info_json = json.loads(room_info_str)
        RoomID.append(str(room_info_json["RoomID"]))
        RoomName.append(room_info_json["RoomName"])
        LowPrice.append(room_info_json["LowPrice"])

        baseroom_info = room_info_json["BaseRoomInfo"]
        # print(type(baseroom_info))
        # <class 'str'>
        remove_tag = baseroom_pattern.sub("",baseroom_info)
        # print(remove_tag)

        RoomDetailInfo = remove_tag.split("|")
        # print(RoomDetailInfo)

        if len(RoomDetailInfo) == 4:
            RoomDetailInfo.insert(3,None)

        RoomSize.append(RoomDetailInfo[0])
        RoomLevel.append(RoomDetailInfo[1])
        BedSize.append(RoomDetailInfo[2])
        IsAddBed.append(RoomDetailInfo[3])
        CustomerNum.append(RoomDetailInfo[4])

    else:
        continue


# Combine the lists as an array
RoomInfo = np.array((RoomID, RoomName, LowPrice, RoomSize, RoomLevel, BedSize, IsAddBed, CustomerNum)).T
# Create a DataFrame object
column_name = ['RoomID', 'RoomName', 'LowPrice', 'RoomSize', 'RoomLevel', 'BedSize', 'IsAddBed', 'CustomerNum']
df = pd.DataFrame(data=RoomInfo, columns=column_name)
print(df)

'''

# 2019-03-12

['27541229', '27541231', '27541233', '33300631', '33300678', '37303662', '79467148', '79467149']
['豪华大床房', '豪华双床房', '豪华商务套房', '豪华商务大床房', '奢华特色套房', '高级大床房', '豪华公寓套房', '至尊公寓套房']
['3-8层', '3-8层', '3-5层', '3、5-8层', '3、5层', '3-10层', '9层', '11层']
['1张2米双人床', '2张1.35米单人床', '1张2米双人床', '1张2米双人床', '1张2米双人床', '1张2米双人床', '1张2米特大床', '1张2米特大床']
[None, '不可加床', None, None, None, '不可加床', None, None]
['2人', '2人', '2人', '2人', '2人', '2人', '2人', '2人']
'''


# Before
'''
[['27541229' '豪华大床房' '1609.0' '40平方米' '3-8层' '不可吸烟' '1张2米双人床' '2人']
 ['27541231' '豪华双床房' '1609.0' '40平方米' '3-8层' '不可吸烟' '2张1.35米单人床' '不可加床']
 ['27541233' '豪华商务套房' '3429.0' '80平方米' '3-5层' '不可吸烟' '1张2米双人床' '2人']
 ['33300631' '豪华商务大床房' '1839.0' '46平方米' '3、5-8层' '不可吸烟' '1张2米双人床' '2人']
 ['33300678' '奢华特色套房' '5459.0' '80平方米' '3、5层' '不可吸烟' '1张2米双人床' '2人']
 ['37303662' '高级大床房' '1328.0' '35平方米' '3-10层' '不可吸烟' '1张2米双人床' '不可加床']
 ['79467148' '豪华公寓套房' '3856.0' '80平方米' '9层' '不可吸烟' '1张2米特大床' '2人']
 ['79467149' '至尊公寓套房' '6438.0' '80平方米' '11层' '不可吸烟' '1张2米特大床' '2人']]
'''