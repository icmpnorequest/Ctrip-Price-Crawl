import requests
import json
from lxml import etree
import csv
from bs4 import BeautifulSoup
import re
import numpy as np
import pandas as pd

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
        print(remove_tag)

        RoomDetailInfo = remove_tag.split("|")
        print(RoomDetailInfo)

        RoomSize.append(RoomDetailInfo[0])
        RoomLevel.append(RoomDetailInfo[1])
        IsSmoking.append(RoomDetailInfo[2])
        BedSize.append(RoomDetailInfo[3])
        CustomerNum.append(RoomDetailInfo[4])
    else:
        continue

# Combine the lists as an array
RoomInfo = np.array((RoomID, RoomName, LowPrice, RoomSize, RoomLevel, IsSmoking, BedSize, CustomerNum)).T
# Create a DataFrame object
df = pd.DataFrame(data=RoomInfo, columns=['RoomID', 'RoomName', 'LowPrice', 'RoomSiae', 'RoomLevel', 'IsSmoking', 'BedSize', 'CustomerNum'])
print(df)


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



'''
type: str
40平方米<span class="line">|</span>3-8层<span class="line">|</span>不可吸烟<span class="line">|</span>1张2米双人床<span class="line">|</span>2人
40平方米<span class="line">|</span>3-8层<span class="line">|</span>不可吸烟<span class="line">|</span>2张1.35米单人床<span class="line">|</span>不可加床<span class="line">|</span>2人
80平方米<span class="line">|</span>3-5层<span class="line">|</span>不可吸烟<span class="line">|</span>1张2米双人床<span class="line">|</span>2人
46平方米<span class="line">|</span>3、5-8层<span class="line">|</span>不可吸烟<span class="line">|</span>1张2米双人床<span class="line">|</span>2人
80平方米<span class="line">|</span>3、5层<span class="line">|</span>不可吸烟<span class="line">|</span>1张2米双人床<span class="line">|</span>2人
35平方米<span class="line">|</span>3-10层<span class="line">|</span>不可吸烟<span class="line">|</span>1张2米双人床<span class="line">|</span>不可加床<span class="line">|</span>2人
80平方米<span class="line">|</span>9层<span class="line">|</span>不可吸烟<span class="line">|</span>1张2米特大床<span class="line">|</span>2人
80平方米<span class="line">|</span>11层<span class="line">|</span>不可吸烟<span class="line">|</span>1张2米特大床<span class="line">|</span>2人

'''


'''
RoomInfo
{"RoomUrl":"//dimg12.c-ctrip.com/images/200b090000003y2zz574C_R_300_225.jpg","RoomID":27541229,"RoomName":"豪华大床房","BaseRoomInfo":"40平方米<span class=\"line\">|</span>3-8层<span class=\"line\">|</span>不可吸烟<span class=\"line\">|</span>1张2米双人床<span class=\"line\">|</span>2人","ConvenientFacilities":null,"MediaTechnology":null,"FoodBeverages":null,"Bathroom":null,"OutdoorsViews":null,"ServicesOthers":null,"PriceNum":3,"LowPrice":1609.0,"RoomTotalNum":3}
{"RoomUrl":"//dimg13.c-ctrip.com/images/200a0m000000djgmfE42D_R_300_225.jpg","RoomID":27541231,"RoomName":"豪华双床房","BaseRoomInfo":"40平方米<span class=\"line\">|</span>3-8层<span class=\"line\">|</span>不可吸烟<span class=\"line\">|</span>2张1.35米单人床<span class=\"line\">|</span>不可加床<span class=\"line\">|</span>2人","ConvenientFacilities":null,"MediaTechnology":null,"FoodBeverages":null,"Bathroom":null,"OutdoorsViews":null,"ServicesOthers":null,"PriceNum":2,"LowPrice":1609.0,"RoomTotalNum":2}
{"RoomUrl":"//dimg11.c-ctrip.com/images/200s090000003y41p18C8_R_300_225.jpg","RoomID":27541233,"RoomName":"豪华商务套房","BaseRoomInfo":"80平方米<span class=\"line\">|</span>3-5层<span class=\"line\">|</span>不可吸烟<span class=\"line\">|</span>1张2米双人床<span class=\"line\">|</span>2人","ConvenientFacilities":null,"MediaTechnology":null,"FoodBeverages":null,"Bathroom":null,"OutdoorsViews":null,"ServicesOthers":null,"PriceNum":2,"LowPrice":3429.0,"RoomTotalNum":2}
{"RoomUrl":"//dimg13.c-ctrip.com/images/20090d0000006y7k06A04_R_300_225.jpg","RoomID":33300631,"RoomName":"豪华商务大床房","BaseRoomInfo":"46平方米<span class=\"line\">|</span>3、5-8层<span class=\"line\">|</span>不可吸烟<span class=\"line\">|</span>1张2米双人床<span class=\"line\">|</span>2人","ConvenientFacilities":null,"MediaTechnology":null,"FoodBeverages":null,"Bathroom":null,"OutdoorsViews":null,"ServicesOthers":null,"PriceNum":2,"LowPrice":1839.0,"RoomTotalNum":2}
{"RoomUrl":"//dimg12.c-ctrip.com/images/20080d0000006y7xj88C1_R_300_225.jpg","RoomID":33300678,"RoomName":"奢华特色套房","BaseRoomInfo":"80平方米<span class=\"line\">|</span>3、5层<span class=\"line\">|</span>不可吸烟<span class=\"line\">|</span>1张2米双人床<span class=\"line\">|</span>2人","ConvenientFacilities":null,"MediaTechnology":null,"FoodBeverages":null,"Bathroom":null,"OutdoorsViews":null,"ServicesOthers":null,"PriceNum":1,"LowPrice":5459.0,"RoomTotalNum":1}
{"RoomUrl":"//dimg12.c-ctrip.com/images/20040n000000e01bjDEF1_R_300_225.jpg","RoomID":37303662,"RoomName":"高级大床房","BaseRoomInfo":"35平方米<span class=\"line\">|</span>3-10层<span class=\"line\">|</span>不可吸烟<span class=\"line\">|</span>1张2米双人床<span class=\"line\">|</span>不可加床<span class=\"line\">|</span>2人","ConvenientFacilities":null,"MediaTechnology":null,"FoodBeverages":null,"Bathroom":null,"OutdoorsViews":null,"ServicesOthers":null,"PriceNum":1,"LowPrice":1328.0,"RoomTotalNum":1}
{"RoomUrl":"//dimg11.c-ctrip.com/images/200p0v000000jszjtD57F_R_300_225.jpg","RoomID":79467148,"RoomName":"豪华公寓套房","BaseRoomInfo":"80平方米<span class=\"line\">|</span>9层<span class=\"line\">|</span>不可吸烟<span class=\"line\">|</span>1张2米特大床<span class=\"line\">|</span>2人","ConvenientFacilities":null,"MediaTechnology":null,"FoodBeverages":null,"Bathroom":null,"OutdoorsViews":null,"ServicesOthers":null,"PriceNum":1,"LowPrice":3856.0,"RoomTotalNum":1}
{"RoomUrl":"//dimg10.c-ctrip.com/images/20050v000000jwzjx420F_R_300_225.jpg","RoomID":79467149,"RoomName":"至尊公寓套房","BaseRoomInfo":"80平方米<span class=\"line\">|</span>11层<span class=\"line\">|</span>不可吸烟<span class=\"line\">|</span>1张2米特大床<span class=\"line\">|</span>2人","ConvenientFacilities":null,"MediaTechnology":null,"FoodBeverages":null,"Bathroom":null,"OutdoorsViews":null,"ServicesOthers":null,"PriceNum":1,"LowPrice":6436.0,"RoomTotalNum":1}
'''

# RoomID, RoomName, LowPrice


# print(len(rooms))
# 13
'''
[
[0] <td class="child_name J_Col_RoomName" data-addbed="1" data-bed="1" data-bf="3" data-ctrip="1" data-firstmap="47630895PP,47631641PP,47631642PP," data-hotelinvoice="1" data-networklan="1" data-networkwifi="1" data-pay="3" data-personmatch="false" data-policy="3" data-price="1609" data-pricedisplay="1609" data-reserve="1" data-roomid="47630895PP">
<span class="room_type_name">标准价</span>
<span data-params="{'options':{'type':'jmp_table','template':'#jmpTempGift','content':{'gift':'T','giftinfo':'每间夜可获得竹林自助餐厅午餐或晚餐1次，每次最多房间内2名已办理入住客人可用。仅限入住期间使用，具体餐次由客人自选，暂不提供周日和国家法定节假日最后一日晚餐。','ShadowGift':'F','package':'F'},'classNames':{'boxType':'jmp_table'},'css':{'maxWidth':500},'group':'gift'}}" data-role="jmp"><span class="label_onsale_orange" style="margin-right: 0px">礼</span></span><input class="spfrom" type="hidden" value="-1"/>
</td>, 

[1] <td class="child_name J_Col_RoomName" data-addbed="1" data-bed="1" data-bf="2" data-ctrip="1" data-hotelinvoice="1" data-networklan="1" data-networkwifi="1" data-pay="3" data-personmatch="false" data-policy="3" data-price="1659" data-pricedisplay="1659" data-reserve="1" data-roomid="47631641PP">
<span class="room_type_name">标准价</span>
<span data-params="{'options':{'type':'jmp_table','template':'#jmpTempGift','content':{'gift':'T','giftinfo':'每间夜可获得竹林自助餐厅午餐或晚餐1次，每次最多房间内2名已办理入住客人可用。仅限入住期间使用，具体餐次由客人自选，暂不提供周日和国家法定节假日最后一日晚餐。','ShadowGift':'F','package':'F'},'classNames':{'boxType':'jmp_table'},'css':{'maxWidth':500},'group':'gift'}}" data-role="jmp"><span class="label_onsale_orange" style="margin-right: 0px">礼</span></span><input class="spfrom" type="hidden" value="-1"/>
</td>, 

##[2] <td class="child_name J_Col_RoomName" data-addbed="1" data-baseroominfo='{"RoomUrl":"//dimg12.c-ctrip.com/images/200b090000003y2zz574C_R_300_225.jpg","RoomID":27541229,"RoomName":"豪华大床房","BaseRoomInfo":"40平方米&lt;span class=\"line\"&gt;|&lt;/span&gt;3-8层&lt;span class=\"line\"&gt;|&lt;/span&gt;不可吸烟&lt;span class=\"line\"&gt;|&lt;/span&gt;1张2米双人床&lt;span class=\"line\"&gt;|&lt;/span&gt;2人","ConvenientFacilities":null,"MediaTechnology":null,"FoodBeverages":null,"Bathroom":null,"OutdoorsViews":null,"ServicesOthers":null,"PriceNum":3,"LowPrice":1609.0,"RoomTotalNum":3}' data-baseroomname="豪华大床房" data-bed="1" data-bf="1" data-ctrip="1" data-hotelinvoice="1" data-networklan="1" data-networkwifi="1" data-pay="3" data-personmatch="false" data-policy="3" data-price="1828" data-pricedisplay="1828" data-reserve="1" data-roomid="47631642PP">
<span class="room_type_name">标准价</span>
<span data-params="{'options':{'type':'jmp_table','template':'#jmpTempGift','content':{'gift':'T','giftinfo':'每间夜可获得竹林自助餐厅午餐或晚餐1次，每次最多房间内2名已办理入住客人可用。仅限入住期间使用，具体餐次由客人自选，暂不提供周日和国家法定节假日最后一日晚餐。','ShadowGift':'F','package':'F'},'classNames':{'boxType':'jmp_table'},'css':{'maxWidth':500},'group':'gift'}}" data-role="jmp"><span class="label_onsale_orange" style="margin-right: 0px">礼</span></span><input class="spfrom" type="hidden" value="-1"/>
</td>, 

[3] <td class="child_name J_Col_RoomName" data-bed="2" data-bf="3" data-ctrip="1" data-firstmap="47630897PP,47631644PP," data-hotelinvoice="1" data-networklan="1" data-networkwifi="1" data-pay="3" data-personmatch="false" data-policy="3" data-price="1609" data-pricedisplay="1609" data-reserve="1" data-roomid="47630897PP">
<span class="room_type_name">标准价</span>
<span data-params="{'options':{'type':'jmp_table','template':'#jmpTempGift','content':{'gift':'T','giftinfo':'每间夜可获得竹林自助餐厅午餐或晚餐1次，每次最多房间内2名已办理入住客人可用。仅限入住期间使用，具体餐次由客人自选，暂不提供周日和国家法定节假日最后一日晚餐。','ShadowGift':'F','package':'F'},'classNames':{'boxType':'jmp_table'},'css':{'maxWidth':500},'group':'gift'}}" data-role="jmp"><span class="label_onsale_orange" style="margin-right: 0px">礼</span></span><input class="spfrom" type="hidden" value="-1"/>
</td>, 

##[4] <td class="child_name J_Col_RoomName" data-baseroominfo='{"RoomUrl":"//dimg13.c-ctrip.com/images/200a0m000000djgmfE42D_R_300_225.jpg","RoomID":27541231,"RoomName":"豪华双床房","BaseRoomInfo":"40平方米&lt;span class=\"line\"&gt;|&lt;/span&gt;3-8层&lt;span class=\"line\"&gt;|&lt;/span&gt;不可吸烟&lt;span class=\"line\"&gt;|&lt;/span&gt;2张1.35米单人床&lt;span class=\"line\"&gt;|&lt;/span&gt;不可加床&lt;span class=\"line\"&gt;|&lt;/span&gt;2人","ConvenientFacilities":null,"MediaTechnology":null,"FoodBeverages":null,"Bathroom":null,"OutdoorsViews":null,"ServicesOthers":null,"PriceNum":2,"LowPrice":1609.0,"RoomTotalNum":2}' data-baseroomname="豪华双床房" data-bed="2" data-bf="1" data-ctrip="1" data-hotelinvoice="1" data-networklan="1" data-networkwifi="1" data-pay="3" data-personmatch="false" data-policy="3" data-price="1848" data-pricedisplay="1848" data-reserve="1" data-roomid="47631644PP">
<span class="room_type_name">标准价</span>
<span data-params="{'options':{'type':'jmp_table','template':'#jmpTempGift','content':{'gift':'T','giftinfo':'每间夜可获得竹林自助餐厅午餐或晚餐1次，每次最多房间内2名已办理入住客人可用。仅限入住期间使用，具体餐次由客人自选，暂不提供周日和国家法定节假日最后一日晚餐。','ShadowGift':'F','package':'F'},'classNames':{'boxType':'jmp_table'},'css':{'maxWidth':500},'group':'gift'}}" data-role="jmp"><span class="label_onsale_orange" style="margin-right: 0px">礼</span></span><input class="spfrom" type="hidden" value="-1"/>
</td>, 

[5] <td class="child_name J_Col_RoomName" data-addbed="1" data-bed="1" data-bf="3" data-ctrip="1" data-firstmap="47630899PP,47631646PP," data-hotelinvoice="1" data-networklan="1" data-networkwifi="1" data-pay="3" data-personmatch="false" data-policy="3" data-price="3429" data-pricedisplay="3429" data-reserve="1" data-roomid="47630899PP">
<span class="room_type_name">标准价</span>
<span data-params="{'options':{'type':'jmp_table','template':'#jmpTempGift','content':{'gift':'T','giftinfo':'首日可获店酒（法国教皇新堡干红）1瓶&lt;br /&gt;每间夜可获竹林自助餐厅午餐和晚餐各1次，每次最多房间内2名已办理入住客人可用。仅限入住期间使用，暂不提供周日和国家法定节假日最后一日晚餐。','ShadowGift':'F','package':'F'},'classNames':{'boxType':'jmp_table'},'css':{'maxWidth':500},'group':'gift'}}" data-role="jmp"><span class="label_onsale_orange" style="margin-right: 0px">礼</span></span><input class="spfrom" type="hidden" value="-1"/>
</td>, 

##[6] <td class="child_name J_Col_RoomName" data-addbed="1" data-baseroominfo='{"RoomUrl":"//dimg11.c-ctrip.com/images/200s090000003y41p18C8_R_300_225.jpg","RoomID":27541233,"RoomName":"豪华商务套房","BaseRoomInfo":"80平方米&lt;span class=\"line\"&gt;|&lt;/span&gt;3-5层&lt;span class=\"line\"&gt;|&lt;/span&gt;不可吸烟&lt;span class=\"line\"&gt;|&lt;/span&gt;1张2米双人床&lt;span class=\"line\"&gt;|&lt;/span&gt;2人","ConvenientFacilities":null,"MediaTechnology":null,"FoodBeverages":null,"Bathroom":null,"OutdoorsViews":null,"ServicesOthers":null,"PriceNum":2,"LowPrice":3429.0,"RoomTotalNum":2}' data-baseroomname="豪华商务套房" data-bed="1" data-bf="1" data-ctrip="1" data-hotelinvoice="1" data-networklan="1" data-networkwifi="1" data-pay="3" data-personmatch="false" data-policy="3" data-price="3668" data-pricedisplay="3668" data-reserve="1" data-roomid="47631646PP">
<span class="room_type_name">标准价</span>
<span data-params="{'options':{'type':'jmp_table','template':'#jmpTempGift','content':{'gift':'T','giftinfo':'首日可获店酒（法国教皇新堡干红）1瓶&lt;br /&gt;每间夜可获竹林自助餐厅午餐和晚餐各1次，每次最多房间内2名已办理入住客人可用。仅限入住期间使用，暂不提供周日和国家法定节假日最后一日晚餐。','ShadowGift':'F','package':'F'},'classNames':{'boxType':'jmp_table'},'css':{'maxWidth':500},'group':'gift'}}" data-role="jmp"><span class="label_onsale_orange" style="margin-right: 0px">礼</span></span><input class="spfrom" type="hidden" value="-1"/>
</td>, 


[7]<td class="child_name J_Col_RoomName" data-addbed="1" data-bed="1" data-bf="3" data-ctrip="1" data-firstmap="58939955PP,58939956PP," data-hotelinvoice="1" data-networkwifi="1" data-pay="3" data-personmatch="false" data-policy="3" data-price="1839" data-pricedisplay="1839" data-reserve="1" data-roomid="58939955PP">
<span class="room_type_name">标准价</span>
<span data-params="{'options':{'type':'jmp_table','template':'#jmpTempGift','content':{'gift':'T','giftinfo':'每间夜可获得竹林自助餐厅午餐或晚餐1次，每次最多房间内2名已办理入住客人可用。仅限入住期间使用，具体餐次由客人自选，暂不提供周日和国家法定节假日最后一日晚餐。','ShadowGift':'F','package':'F'},'classNames':{'boxType':'jmp_table'},'css':{'maxWidth':500},'group':'gift'}}" data-role="jmp"><span class="label_onsale_orange" style="margin-right: 0px">礼</span></span><input class="spfrom" type="hidden" value="-1"/>
</td>, 

##[8]<td class="child_name J_Col_RoomName" data-addbed="1" data-baseroominfo='{"RoomUrl":"//dimg13.c-ctrip.com/images/20090d0000006y7k06A04_R_300_225.jpg","RoomID":33300631,"RoomName":"豪华商务大床房","BaseRoomInfo":"46平方米&lt;span class=\"line\"&gt;|&lt;/span&gt;3、5-8层&lt;span class=\"line\"&gt;|&lt;/span&gt;不可吸烟&lt;span class=\"line\"&gt;|&lt;/span&gt;1张2米双人床&lt;span class=\"line\"&gt;|&lt;/span&gt;2人","ConvenientFacilities":null,"MediaTechnology":null,"FoodBeverages":null,"Bathroom":null,"OutdoorsViews":null,"ServicesOthers":null,"PriceNum":2,"LowPrice":1839.0,"RoomTotalNum":2}' data-baseroomname="豪华商务大床房" data-bed="1" data-bf="2" data-ctrip="1" data-hotelinvoice="1" data-networkwifi="1" data-pay="3" data-personmatch="false" data-policy="3" data-price="1956" data-pricedisplay="1956" data-reserve="1" data-roomid="58939956PP">
<span class="room_type_name">标准价</span>
<span data-params="{'options':{'type':'jmp_table','template':'#jmpTempGift','content':{'gift':'T','giftinfo':'每间夜可获得竹林自助餐厅午餐或晚餐1次，每次最多房间内2名已办理入住客人可用。仅限入住期间使用，具体餐次由客人自选，暂不提供周日和国家法定节假日最后一日晚餐。','ShadowGift':'F','package':'F'},'classNames':{'boxType':'jmp_table'},'css':{'maxWidth':500},'group':'gift'}}" data-role="jmp"><span class="label_onsale_orange" style="margin-right: 0px">礼</span></span><input class="spfrom" type="hidden" value="-1"/>
</td>, 

[9]<td class="child_name J_Col_RoomName" data-addbed="1" data-baseroominfo='{"RoomUrl":"//dimg12.c-ctrip.com/images/20080d0000006y7xj88C1_R_300_225.jpg","RoomID":33300678,"RoomName":"奢华特色套房","BaseRoomInfo":"80平方米&lt;span class=\"line\"&gt;|&lt;/span&gt;3、5层&lt;span class=\"line\"&gt;|&lt;/span&gt;不可吸烟&lt;span class=\"line\"&gt;|&lt;/span&gt;1张2米双人床&lt;span class=\"line\"&gt;|&lt;/span&gt;2人","ConvenientFacilities":null,"MediaTechnology":null,"FoodBeverages":null,"Bathroom":null,"OutdoorsViews":null,"ServicesOthers":null,"PriceNum":1,"LowPrice":5459.0,"RoomTotalNum":1}' data-baseroomname="奢华特色套房" data-bed="1" data-bf="1" data-ctrip="1" data-hotelinvoice="1" data-networkwifi="1" data-pay="3" data-personmatch="false" data-policy="3" data-price="5459" data-pricedisplay="5459" data-reserve="1" data-roomid="58939960PP">
<span class="room_type_name">标准价</span>
<span data-params="{'options':{'type':'jmp_table','template':'#jmpTempGift','content':{'gift':'T','giftinfo':'首日可获店酒（法国教皇新堡干红）1瓶&lt;br /&gt;每间夜可获竹林自助餐厅午餐和晚餐各1次，每次最多房间内2名已办理入住客人可用。仅限入住期间使用，暂不提供周日和国家法定节假日最后一日晚餐。','ShadowGift':'F','package':'F'},'classNames':{'boxType':'jmp_table'},'css':{'maxWidth':500},'group':'gift'}}" data-role="jmp"><span class="label_onsale_orange" style="margin-right: 0px">礼</span></span><input class="spfrom" type="hidden" value="-1"/>
</td>, 

##[10]<td class="child_name J_Col_RoomName" data-baseroominfo='{"RoomUrl":"//dimg12.c-ctrip.com/images/20040n000000e01bjDEF1_R_300_225.jpg","RoomID":37303662,"RoomName":"高级大床房","BaseRoomInfo":"35平方米&lt;span class=\"line\"&gt;|&lt;/span&gt;3-10层&lt;span class=\"line\"&gt;|&lt;/span&gt;不可吸烟&lt;span class=\"line\"&gt;|&lt;/span&gt;1张2米双人床&lt;span class=\"line\"&gt;|&lt;/span&gt;不可加床&lt;span class=\"line\"&gt;|&lt;/span&gt;2人","ConvenientFacilities":null,"MediaTechnology":null,"FoodBeverages":null,"Bathroom":null,"OutdoorsViews":null,"ServicesOthers":null,"PriceNum":1,"LowPrice":1328.0,"RoomTotalNum":1}' data-baseroomname="高级大床房" data-bed="1" data-bf="3" data-ctrip="1" data-hotelinvoice="1" data-networkwifi="1" data-pay="3" data-personmatch="false" data-policy="1|2" data-price="1328" data-pricedisplay="1328" data-reserve="1" data-roomid="67950117PP">
<span class="room_type_name">(无景/不规则)</span>
<span data-params="{'options':{'type':'jmp_table','template':'#jmpTempGift','content':{'gift':'T','giftinfo':'每间夜可获得竹林自助餐厅午餐或晚餐1次，每次最多房间内2名已办理入住客人可用。仅限入住期间使用，具体餐次由客人自选，暂不提供周日和国家法定节假日最后一日晚餐。','ShadowGift':'F','package':'F'},'classNames':{'boxType':'jmp_table'},'css':{'maxWidth':500},'group':'gift'}}" data-role="jmp"><span class="label_onsale_orange" style="margin-right: 0px">礼</span></span><input class="spfrom" type="hidden" value="-1"/>
</td>, 

[11]<td class="child_name J_Col_RoomName" data-addbed="1" data-baseroominfo='{"RoomUrl":"//dimg11.c-ctrip.com/images/200p0v000000jszjtD57F_R_300_225.jpg","RoomID":79467148,"RoomName":"豪华公寓套房","BaseRoomInfo":"80平方米&lt;span class=\"line\"&gt;|&lt;/span&gt;9层&lt;span class=\"line\"&gt;|&lt;/span&gt;不可吸烟&lt;span class=\"line\"&gt;|&lt;/span&gt;1张2米特大床&lt;span class=\"line\"&gt;|&lt;/span&gt;2人","ConvenientFacilities":null,"MediaTechnology":null,"FoodBeverages":null,"Bathroom":null,"OutdoorsViews":null,"ServicesOthers":null,"PriceNum":1,"LowPrice":3856.0,"RoomTotalNum":1}' data-baseroomname="豪华公寓套房" data-bed="1" data-bf="3" data-ctrip="1" data-hotelinvoice="1" data-networkwifi="1" data-pay="3" data-personmatch="false" data-policy="1|2" data-price="3856" data-pricedisplay="3856" data-reserve="1" data-roomid="178457389PP">
<span class="room_type_name">标准价</span>
<input class="spfrom" type="hidden" value="-1"/>
</td>, 

[12]<td class="child_name J_Col_RoomName" data-addbed="1" data-baseroominfo='{"RoomUrl":"//dimg10.c-ctrip.com/images/20050v000000jwzjx420F_R_300_225.jpg","RoomID":79467149,"RoomName":"至尊公寓套房","BaseRoomInfo":"80平方米&lt;span class=\"line\"&gt;|&lt;/span&gt;11层&lt;span class=\"line\"&gt;|&lt;/span&gt;不可吸烟&lt;span class=\"line\"&gt;|&lt;/span&gt;1张2米特大床&lt;span class=\"line\"&gt;|&lt;/span&gt;2人","ConvenientFacilities":null,"MediaTechnology":null,"FoodBeverages":null,"Bathroom":null,"OutdoorsViews":null,"ServicesOthers":null,"PriceNum":1,"LowPrice":6436.0,"RoomTotalNum":1}' data-baseroomname="至尊公寓套房" data-bed="1" data-bf="3" data-ctrip="1" data-hotelinvoice="1" data-networkwifi="1" data-pay="3" data-personmatch="false" data-policy="1|2" data-price="6436" data-pricedisplay="6436" data-reserve="1" data-roomid="178457784PP">
<span class="room_type_name">标准价</span>
<input class="spfrom" type="hidden" value="-1"/>
</td>]
'''


