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
from datetime import datetime

pd.set_option('display.max_columns', 10000)
pd.set_option('display.max_rows', 10000)
pd.set_option('display.max_colwidth', 10000)
pd.set_option('display.width',1000)

# Beijing 5 star hotel list url
five_star_url = "http://hotels.ctrip.com/Domestic/Tool/AjaxHotelList.aspx"

# Bejing 5 star hotel list
filename = "./Data/Beijing 5 star hotel list.csv"

# User-agent list
ua_path = "Common User Agent.txt"

# date pattern
date_pattern = re.compile(r'\d{4}\-\d{2}\-\d{2}')
dateinput_pattern = re.compile(r'[a-zA-Z~!@#$%^&*(),.?]')


def hotel_detail(hotel_id,checkin,checkout):
    """
    It aims to scrap the detailed information of a specific hotel.
    """

    # Generate the header
    headers = {"Connection": "keep-alive",
               "Accept-Language": "zh-CN,zh;q=0.9",
               "Cache-Control": "max-age=0",
               "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
               "Host": "hotels.ctrip.com",
               "If-Modified-Since": "Thu, 01 Jan 1970 00:00:00 GMT",
               "Referer": "http://hotels.ctrip.com/hotel/2231618.html",
               "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36",
               "startDate": checkin,
               "depDate": checkout
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


def date_check(date):
    '''
    It is a function to check and correct date format.
    '''

    if not date_pattern.findall(date):
        # print('Illegal Date Input! Please input again')
        return 0
    else:
        # date_trans = str(datetime.strptime(date,"%Y-%m-%d"))
        return date

def main():

    # 1. Beijing 5 Star Hotel List is as bellow
    df = pd.read_csv(filename, encoding='utf8')
    print("1. Beijing 5 Star Hotel Lists")
    print(df)
    hotelID = df["id"]
    print('\n')

    while True:

        print("2.1 Please input the CheckIn Date (Note: please input like 2019-03-18):")
        print('If you want to quit, please input "q"')

        checkIn_input = input()
        if checkIn_input == "q":
            print('Nice to see you again!')
            exit()
        checkIn_check = date_check(checkIn_input)
        if checkIn_check == 0:
            print('Illegal Date Input! Please input again')
            continue
        else:
            print('Check-In Date %s correct!' % checkIn_check)

        print("2.2 Please input the CheckOut Date (Note: please input like 2019-03-18):")
        print('If you want to quit, please input "q"')

        checkOut_input = input()
        if checkOut_input == "q":
            print('Nice to see you again!')
            exit()
        checkOut_check = date_check(checkOut_input)
        if checkOut_check == 0:
            print('Illegal Date Input! Please input again')
            continue
        else:
            print('Check-Out Date %s correct!' % checkOut_check)

        while True:

            print("2.3 Please input the hotel index in the DataFrame.")
            print("2.4 If you want to quit, please input 'q'.")
            print("2.5 If you want to modify the date, please input 'm'.")

            print("Please input the Parameter: ")
            input_param = input()
            if input_param.isnumeric():
                hotel_index = int(input_param)
                max_dflen = len(df)
                if 0 <= hotel_index <= max_dflen:
                    print("3. The detail information of the Hotel ", df['name'][hotel_index])
                    hotel_detail(hotelID[hotel_index], checkIn_check, checkOut_check)
                else:
                    print('Hotel Index out of range! ')
                    print('Remember: 0 <= Hotel Index <= ' + str(max_dflen))
                    print('Please input again.')
                    continue
            elif input_param == 'q':
                print('See you later!')
                exit()
            elif input_param == 'm':
                break
            else:
                print('Invalid Input!')
                print('\n')
                continue


if __name__ == "__main__":

    main()