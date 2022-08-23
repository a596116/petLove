import requests 
from bs4 import BeautifulSoup
import csv 
import os 
import time 
import random


#======LINE API=========
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import (
    MessageEvent,
    TextSendMessage,
    TemplateSendMessage,
    ButtonsTemplate,
    MessageTemplateAction,
    PostbackEvent,
    PostbackTemplateAction,
    FlexSendMessage,
    ImageSendMessage,
    QuickReplyButton,
    QuickReply,PostbackAction,CameraAction,CameraRollAction,LocationAction,
    MessageAction,ImagemapSendMessage,MessageImagemapAction,BaseSize,ImagemapArea,CarouselColumn,CarouselTemplate,ImageMessage,
)
#=======================

def pet_adoption(Variety):
    url = 'https://data.coa.gov.tw/Service/OpenData/TransService.aspx?UnitId=QcbUEzN6E6DL&$top=5000&$skip=0'
    res_get = requests.get(url)
    a = res_get.json()
    list1 = []
    while len(list1)<12:
        ram = random.randint(0, 1000)
        if ram not in list1 and a[ram]["animal_kind"]==Variety:
            list1.append(ram)
    contents=dict()
    contents['type']='carousel'
    bubbles=[]
    for i in list1:
        if a[i]["album_file"] == '':
            photo_url = 'https://upload.cc/i1/2021/04/07/w2HD4s.jpg'
        else:
            photo_url = a[i]["album_file"]

        if a[i]["animal_sex"] == '':
            a[i]["animal_sex"] = 'X'
        if a[i]["animal_bodytype"] == '':
            a[i]["animal_bodytype"] = 'X'
        if a[i]["animal_colour"] == '':
            a[i]["animal_colour"] = 'X'
        if a[i]["animal_sterilization"] == '':
            a[i]["animal_sterilization"] = 'X'
        if a[i]["animal_bacterin"] == '':
            a[i]["animal_bacterin"] = 'X'
        if a[i]["animal_place"] == '':
            a[i]["animal_place"] = 'X'
        if a[i]["animal_opendate"] == '':
            a[i]["animal_opendate"] = 'X'
        if a[i]["shelter_tel"] == '':
            a[i]["shelter_tel"] = 'X'

        bubbles.append({
                        "type": "bubble",
                        "hero": {
                            "type": "image",
                            "url": photo_url,
                            "size": "full",
                            "aspectRatio": "15:13",
                            "aspectMode": "cover",
                            "action": {
                            "type": "postback",
                            "label": "action",
                            "data": "photo"+photo_url
                            }
                        },
                        "body": {
                            "type": "box",
                            "layout": "vertical",
                            "margin": "lg",
                            "spacing": "sm",
                            "contents": [
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": "性別：",
                                    "size": "sm",
                                    "flex": 0,
                                    "color": "#75a3a3"
                                },
                                {
                                    "type": "text",
                                    "text": a[i]["animal_sex"],
                                    "color": "#c2c2a3",
                                    "size": "sm",
                                    "flex": 7,
                                    "wrap": True
                                },
                                {
                                    "type": "text",
                                    "text": "體型：",
                                    "offsetStart": "xxl",
                                    "flex": 10,
                                    "size": "sm",
                                    "color": "#75a3a3"
                                },
                                {
                                    "type": "text",
                                    "text": a[i]["animal_bodytype"],
                                    "flex": 28,
                                    "offsetStart": "xxl",
                                    "size": "sm",
                                    "color": "#c2c2a3"
                                }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": "毛色：",
                                    "size": "sm",
                                    "flex": 0,
                                    "color": "#75a3a3"
                                },
                                {
                                    "type": "text",
                                    "text": a[i]["animal_colour"],
                                    "flex": 0,
                                    "size": "sm",
                                    "color": "#c2c2a3"
                                },
                                {
                                    "type": "text",
                                    "text": "絕育：",
                                    "flex": 0,
                                    "size": "sm",
                                    "offsetStart": "xl",
                                    "color": "#75a3a3"
                                },
                                {
                                    "type": "text",
                                    "text": a[i]["animal_sterilization"],
                                    "flex": 0,
                                    "size": "sm",
                                    "offsetStart": "xl",
                                    "color": "#c2c2a3"
                                },
                                {
                                    "type": "text",
                                    "text": "疫苗：",
                                    "flex": 0,
                                    "size": "sm",
                                    "offsetStart": "xxl",
                                    "color": "#75a3a3"
                                },
                                {
                                    "type": "text",
                                    "text": a[i]["animal_bacterin"],
                                    "flex": 0,
                                    "size": "sm",
                                    "offsetStart": "xl",
                                    "color": "#c2c2a3"
                                }
                                ]
                            },
                            {
                                "type": "separator",
                                "margin": "md",
                                "color": "#b3cccc"
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": "地點：",
                                    "size": "sm",
                                    "flex": 0,
                                    "color": "#75a3a3"
                                },
                                {
                                    "type": "text",
                                    "wrap": True,
                                    "color": "#c2c2a3",
                                    "size": "sm",
                                    "flex": 7,
                                    "text": a[i]["animal_place"]
                                }
                                ],
                                "paddingTop": "sm"
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": "開放認養時間：",
                                    "size": "sm",
                                    "flex": 4,
                                    "color": "#75a3a3"
                                },
                                {
                                    "type": "text",
                                    "wrap": True,
                                    "color": "#c2c2a3",
                                    "size": "sm",
                                    "flex": 5,
                                    "text": a[i]["animal_opendate"]
                                }
                                ]
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "spacing": "sm",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": "連絡電話：",
                                    "size": "sm",
                                    "flex": 3,
                                    "color": "#75a3a3"
                                },
                                {
                                    "type": "text",
                                    "wrap": True,
                                    "color": "#c2c2a3",
                                    "size": "sm",
                                    "flex": 5,
                                    "text": a[i]["shelter_tel"]
                                }
                                ]
                            }
                            ]
                        }
                        })
    res_get.close()
    contents['contents']=bubbles
    message = FlexSendMessage(alt_text='寵物領養',contents=contents)
        
    return message


























