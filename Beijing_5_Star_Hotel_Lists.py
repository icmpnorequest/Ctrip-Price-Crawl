# coding=utf8
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
import random
import time
import csv
import json
import re

pd.set_option('display.max_columns', 10000)
pd.set_option('display.max_rows', 10000)
pd.set_option('display.max_colwidth', 10000)
pd.set_option('display.width',1000)

# Beijing 5 star hotel list url
five_star_url = "http://hotels.ctrip.com/Domestic/Tool/AjaxHotelList.aspx"
filename = "./Data/Beijing 5 star hotel list.csv"

def Scrap_hotel_lists():
    """
    It aims to crawl the 5 star hotel lists in Beijing and save in a csv file.
    """
    headers = {
        "Connection": "keep-alive",
        "origin": "http://hotels.ctrip.com",
        "Host": "hotels.ctrip.com",
        "referer": "http://hotels.ctrip.com/hotel/beijing1",
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36",
        "Content-Type":"application/x-www-form-urlencoded; charset=utf-8"
    }

    id = []
    name = []
    hotel_url = []
    address = []
    score = []

    # 8 pages
    for page in range(1,8):
        data = {
            "StartTime": "2019-03-18",  # The value depends on the date you want to scrap.
            "DepTime": "2019-03-20",
            "RoomGuestCount": "0,1,2",
            "cityId": 1,
            "cityPY": " beijing",
            "cityCode": "010",
            "cityLat": 39.9105329229,
            "cityLng": 116.413784021,
            "page": page,
            "star": 5,
            "orderby": 3
        }
        html = requests.post(five_star_url, headers=headers, data=data)
        hotel_list = html.json()["hotelPositionJSON"]

        for item in hotel_list:
            id.append(item['id'])
            name.append(item['name'])
            hotel_url.append(item['url'])
            address.append(item['address'])
            score.append(item['score'])

        time.sleep(random.randint(3,5))

    hotel_array = np.array((id, name, score, hotel_url, address)).T
    list_header = ['id', 'name', 'score', 'url', 'address']
    array_header = np.array((list_header))
    hotellists = np.vstack((array_header, hotel_array))
    with open(filename, 'w', encoding="utf-8-sig", newline="") as f:
        csvwriter = csv.writer(f, dialect='excel')
        csvwriter.writerows(hotellists)


def hotel_detail(hotel_id):
    """
    It aims to scrap the detailed information of a specific hotel.
    """
    headers = {"Connection": "keep-alive",
               "Accept-Language": "zh-CN,zh;q=0.9",
               "Cache-Control": "max-age=0",
               "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
               "Host": "hotels.ctrip.com",
               "If-Modified-Since": "Thu, 01 Jan 1970 00:00:00 GMT",
               "Referer": "http://hotels.ctrip.com/hotel/2231618.html",
               "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/69.0.3497.92 Safari/537.36"
               }

    basic_url = "http://hotels.ctrip.com/Domestic/tool/AjaxHote1RoomListForDetai1.aspx?hotel="
    url = basic_url + str(hotel_id)

    r = requests.get(url, headers=headers)
    # Response is a json object.
    html = r.json()['html']
    soup = BeautifulSoup(html, "lxml")
    rooms = soup.findAll('td', attrs={"class": "child_name J_Col_RoomName"})

    RoomID = []
    RoomName = []
    LowPrice = []
    RoomSize = []
    RoomLevel = []
    IsAddBed = []
    BedSize = []
    CustomerNum = []

    # Regex Pattern
    baseroom_pattern = re.compile(r'<[^>]+>')  # r'<[^>]+>'

    for idx in range(len(rooms)):
        if rooms[idx].has_attr(key='data-baseroominfo'):
            room_info_str = rooms[idx]['data-baseroominfo']
            room_info_json = json.loads(room_info_str)
            RoomID.append(str(room_info_json["RoomID"]))
            RoomName.append(room_info_json["RoomName"])
            LowPrice.append(room_info_json["LowPrice"])

            baseroom_info = room_info_json["BaseRoomInfo"]
            # print(type(baseroom_info))
            # <class 'str'>
            remove_tag = baseroom_pattern.sub("", baseroom_info)
            RoomDetailInfo = remove_tag.split("|")
            if len(RoomDetailInfo) == 4:
                RoomDetailInfo.insert(3, None)

            RoomSize.append(RoomDetailInfo[0])
            RoomLevel.append(RoomDetailInfo[1])
            BedSize.append(RoomDetailInfo[2])
            IsAddBed.append(RoomDetailInfo[3])
            CustomerNum.append(RoomDetailInfo[4])
        else:
            continue

    RoomInfo = np.array((RoomID, RoomName, LowPrice, RoomSize, RoomLevel, BedSize, IsAddBed, CustomerNum)).T
    # Create a DataFrame object
    # print(RoomInfo)
    column_name = ['RoomID', 'RoomName', 'LowPrice', 'RoomSize', 'RoomLevel', 'BedSize', 'IsAddBed', 'CustomerNum']
    df = pd.DataFrame(data=RoomInfo, columns=column_name)
    print(df)


if __name__ == "__main__":

    # 1. Scrap 5 star hotel list in Beijing
    # Scrap_hotel_lists()

    # 2. Scrap the detailed hotel information
    df = pd.read_csv(filename, encoding='utf8')
    print("1. Beijing 5 Star Hotel Lists")
    print(df)
    hotelID = df["id"]
    print('\n')

    while True:
        print("2.1 If you find to search the detail hotel information, please input the hotel index in the DataFrame.")
        print("2.2 If you want to quit, input 'q'.")

        print("Please input the Parameter: ")
        input_param = input()
        if input_param.isnumeric():
            hotel_index = int(input_param)
            if 0 <= hotel_index <= 170:
                print("3. The detail information of the Hotel:")
                hotel_detail(hotelID[hotel_index])
            else:
                print('Hotel Index out of range! ')
                print('Remember: 0 <= Hotel Index <= 170')
                print('Please input again.')
                continue
        elif input_param == 'q':
            print('See you later!')
            break
        else:
            print('Invalid Input!')
            print('\n')
            continue