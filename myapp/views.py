from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
 
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

from .qr_code import qr
from .Grain_Merchant import grain_merchant,pet_shopping
from .Pet_adoption import pet_adoption
from .google_sheet import google_sheet
 
from liffpy import (LineFrontendFramework as LIFF,ErrorResponse)
import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import json
import re
import time
from bs4 import BeautifulSoup
from flask import render_template
import difflib
import sys
import datetime
import urllib.request

static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
liff_api = LIFF(settings.LINE_CHANNEL_ACCESS_TOKEN)

 
@csrf_exempt
def callback(request):
    if request.method == 'GET':
        return render(request,'home.html')
    elif request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
 
        try:
            events = parser.parse(body, signature)  # 傳入的事件
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
 
        for event in events:
            if isinstance(event, MessageEvent):  
                if event.message.type=='location':
                    sheet = google_sheet('1soCwzHNYjPYfaLHvizLi3osIL7lPoN9kA_Z4zu2iWCw')
                    address = sheet.cell(sheet.col_values(1).index('Ue5be659c6afe872f37d292341c5873cb') +1, 2).value
                    latitude = 24.12
                    longitude = 120.15
                    # address = event.message.address
                    # latitude = event.message.latitude
                    # longitude = event.message.longitude
                    if sheet.cell(sheet.col_values(1).index('Ue5be659c6afe872f37d292341c5873cb') +1, 3).value == "A":
                        message=[]
                        message.append(grain_merchant(address,latitude,longitude))
                        line_bot_api.reply_message(event.reply_token,message)
                    elif sheet.cell(sheet.col_values(1).index('Ue5be659c6afe872f37d292341c5873cb') +1, 3).value == "B":
                        line_bot_api.reply_message(event.reply_token,pet_shopping(address))


                elif event.message.text[:3] == "###" and len(event.message.text)>3:
                    sheet = google_sheet('1l5qPUTYVgQgAv7Nw5GrIPRZeTBG5Hl0JchoSFoinra4')
                    sheet.update_cell(sheet.col_values(4).index(event.message.text[3:-5]) +1 ,7 , event.source.user_id)
                    num = sheet.find(event.message.text[3:-5],in_column=4).row-1
                    img = qr(event.message.text[3:-5],num)
                    sheet.update_cell(sheet.col_values(4).index(event.message.text[3:-5]) +1 ,8 , img)
                    mes = ImageSendMessage(original_content_url=img , preview_image_url=img)
                    try:
                        line_bot_api.reply_message(event.reply_token, mes)
                    except:
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='錯誤！'))
                    

                elif event.message.text == "id":
                    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=str(event.source.user_id)))

                elif event.message.text == "查看寵物資料":
                    sheet = google_sheet('1l5qPUTYVgQgAv7Nw5GrIPRZeTBG5Hl0JchoSFoinra4')
                    findrow = sheet.findall(event.source.user_id,in_column=7)
                    if len(findrow) == 0:
                        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='還沒有新增資料哦！'))
                    else:
                        a = json.load(open('newpet.json','r',encoding='utf-8'))
                        for i in range(len(findrow)):
                            if sheet.row_values(findrow[i].row)[5] == '':
                                img = 'https://upload.cc/i1/2021/04/09/PlS8Oh.png'
                            else:
                                img = sheet.row_values(findrow[i].row)[5]
                            a['contents'].append({"type": "bubble","size": "mega","hero": {"type": "image","url": img,"size": "full",
                                                "aspectRatio": "11:9","aspectMode": "cover","action": {"type": "postback","label": "action","data": "photo"+sheet.row_values(findrow[i].row)[7]}},"body": {"type": "box","layout": "vertical",
                                                "contents": [{"type": "text","text": sheet.row_values(findrow[i].row)[3],"weight": "bold","size": "xl","margin": "none","align": "center","color": "#79a6d2"},{"type": "box",
                                                    "layout": "vertical","margin": "xl","spacing": "sm","contents": [{"type": "box","layout": "baseline","spacing": "sm","contents": [{
                                                    "type": "text","text": "主人姓名","color": "#669999","size": "md","flex": 3,"align": "center"},{"type": "text","wrap": True,"color": "#9999ff",
                                                    "size": "sm","flex": 5,"text": sheet.row_values(findrow[i].row)[0]}]},{"type": "box","layout": "baseline","spacing": "sm","contents": [{"type": "text","text": "電   話",
                                                    "color": "#669999","size": "md","flex": 3,"align": "center"},{"type": "text","text": sheet.row_values(findrow[i].row)[1],"wrap": True,"color": "#9999ff","size": "sm",
                                                    "flex": 5}]},{"type": "box","layout": "baseline","spacing": "sm","contents": [{"type": "text","text": "Email","color": "#669999","size": "md",
                                                "flex": 3,"align": "center"},{"type": "text","text": sheet.row_values(findrow[i].row)[2],"wrap": True,"color": "#9999ff","size": "sm","flex": 5}]}]}]}})
                        line_bot_api.reply_message(event.reply_token, FlexSendMessage('寵物資料',a)) 

                elif event.message.text == '附近寵物醫院':
                    sheet = google_sheet('1soCwzHNYjPYfaLHvizLi3osIL7lPoN9kA_Z4zu2iWCw')
                    sheet.update_cell(sheet.col_values(1).index(event.source.user_id) +1 ,3 , 'A')
                    quick = TextSendMessage(text="place",quick_reply = QuickReply(items=[QuickReplyButton(action=LocationAction(label="發送位置~"))]))
                    line_bot_api.reply_message(event.reply_token,quick)

                elif event.message.text == '附近寵物店':
                    sheet = google_sheet('1soCwzHNYjPYfaLHvizLi3osIL7lPoN9kA_Z4zu2iWCw')
                    sheet.update_cell(sheet.col_values(1).index(event.source.user_id) +1 ,3 , 'B')
                    quick = TextSendMessage(text="place",quick_reply = QuickReply(items=[QuickReplyButton(action=LocationAction(label="發送位置~"))]))
                    line_bot_api.reply_message(event.reply_token,quick)


                #領養寵物   
                elif event.message.text == 'Dog':
                    line_bot_api.reply_message(event.reply_token,pet_adoption('狗'))
                elif event.message.text == 'Cat':
                    line_bot_api.reply_message(event.reply_token,pet_adoption('貓'))


                # elif event.message.text == '寵愛':
                #     try:
                #         #新增LIFF頁面到LINEBOT中
                #         liff_id = liff_api.add(
                #             view_type="tall",
                #             view_url='https://haodai1.herokuapp.com/haodai')

                #         line_bot_api.reply_message(event.reply_token,TextSendMessage(text='https://liff.line.me/'+liff_id))
                #     except:
                #         print('NO')


            #Postback
            elif isinstance(event, PostbackEvent):  
                #選單
                if event.postback.data == "page2":
                    line_bot_api.link_rich_menu_to_user(event.source.user_id,'richmenu-52ee189c6668b46cd491019486e230dd')
                elif event.postback.data == "page1":
                    line_bot_api.unlink_rich_menu_from_user(event.source.user_id)
                
                elif event.postback.data[0:5] == "photo":
                    photo = event.postback.data[5:]
                    line_bot_api.reply_message(event.reply_token,ImageSendMessage(original_content_url=photo, preview_image_url=photo))
                





        return HttpResponse()
    
    else:
        return HttpResponseBadRequest()


@csrf_exempt
def view(request):
    if request.method == 'GET':
        return render(request,'view.html')
    else:
        return HttpResponseBadRequest()

@csrf_exempt
def update(request):
    if request.method == 'GET':
        return render(request,'update.html')
    else:
        return HttpResponseBadRequest()
@csrf_exempt
def end(request):
    if request.method == 'GET':
        return render(request,'end.html')
    else:
        return HttpResponseBadRequest()       