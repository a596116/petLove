import requests 
from bs4 import BeautifulSoup
import csv 
import os 
import time 
import urllib

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

from .address_to_coordinate import *

#糧價查詢的URL
def grain_merchant(address,latitude_o,longitude_o):
    st_time = time.time()
    print("地址：",address,"緯度：",latitude_o,"經度：",longitude_o)

    url = 'https://data.coa.gov.tw/Service/OpenData/DataFileService.aspx?UnitId=078&$top=5000&$skip=0'
    region_list = ["基隆市中正區","基隆市七堵區","基隆市暖暖區","基隆市仁愛區","基隆市中山區","基隆市安樂區","基隆市信義區",
            "臺北市松山區","臺北市信義區","臺北市大安區","臺北市中山區","臺北市中正區","臺北市大同區","臺北市萬華區","臺北市文山區","臺北市南港區","臺北市內湖區","臺北市士林區","臺北市北投區",
            "新北市板橋區","新北市三重區","新北市中和區","新北市永和區","新北市新莊區","新北市新店區","新北市樹林區","新北市鶯歌區","新北市三峽區","新北市淡水區","新北市汐止區","新北市瑞芳區","新北市土城區","新北市蘆洲區","新北市五股區","新北市泰山區","新北市林口區","新北市深坑區","新北市石碇區","新北市坪林區","新北市三芝區","新北市石門區","新北市八里區","新北市平溪區","新北市雙溪區","新北市貢寮區","新北市金山區","新北市萬里區","新北市烏來區",
            "桃園市桃園區","桃園市中壢區","桃園市大溪區","桃園市楊梅區","桃園市蘆竹區","桃園市大園區","桃園市龜山區","桃園市八德區","桃園市龍潭區","桃園市平鎮區","桃園市新屋區","桃園市觀音區","桃園市復興區",
            "新竹市東區","新竹市北區","新竹市香山區",
            "新竹縣竹北市","新竹縣竹東鎮","新竹縣新埔鎮","新竹縣關西鎮","新竹縣湖口鄉","新竹縣新豐鄉","新竹縣芎林鄉","新竹縣橫山鄉","新竹縣北埔鄉","新竹縣寶山鄉","新竹縣峨眉鄉","新竹縣尖石鄉","新竹縣五峰鄉",
            "苗栗縣苗栗市","苗栗縣苑裡鎮","苗栗縣通霄鎮","苗栗縣竹南鎮","苗栗縣頭份市","苗栗縣後龍鎮","苗栗縣卓蘭鎮","苗栗縣大湖鄉","苗栗縣公館鄉","苗栗縣銅鑼鄉","苗栗縣南庄鄉","苗栗縣頭屋鄉","苗栗縣三義鄉","苗栗縣西湖鄉","苗栗縣造橋鄉","苗栗縣三灣鄉","苗栗縣獅潭鄉","苗栗縣泰安鄉",
            "臺中市中區","臺中市東區","臺中市南區","臺中市西區","臺中市北區","臺中市西屯區","臺中市南屯區","臺中市北屯區","臺中市豐原區","臺中市東勢區","臺中市大甲區","臺中市清水區","臺中市沙鹿區","臺中市梧棲區","臺中市后里區","臺中市神岡區","臺中市潭子區","臺中市大雅區","臺中市新社區","臺中市石岡區","臺中市外埔區","臺中市大安區","臺中市烏日區","臺中市大肚區","臺中市龍井區","臺中市霧峰區","臺中市太平區","臺中市大里區","臺中市和平區",
            "彰化縣彰化市","彰化縣鹿港鎮","彰化縣和美鎮","彰化縣線西鄉","彰化縣伸港鄉","彰化縣福興鄉","彰化縣秀水鄉","彰化縣花壇鄉","彰化縣芬園鄉","彰化縣員林市","彰化縣溪湖鎮","彰化縣田中鎮","彰化縣大村鄉","彰化縣埔鹽鄉","彰化縣埔心鄉","彰化縣永靖鄉","彰化縣社頭鄉","彰化縣二水鄉","彰化縣北斗鎮","彰化縣二林鎮","彰化縣田尾鄉","彰化縣埤頭鄉","彰化縣芳苑鄉","彰化縣大城鄉","彰化縣竹塘鄉","彰化縣溪州鄉",
            "南投縣南投市","南投縣埔里鎮","南投縣草屯鎮","南投縣竹山鎮","南投縣集集鎮","南投縣名間鄉","南投縣鹿谷鄉","南投縣中寮鄉","南投縣魚池鄉","南投縣國姓鄉","南投縣水里鄉","南投縣信義鄉","南投縣仁愛鄉",
            "雲林縣斗六市","雲林縣斗南鎮","雲林縣虎尾鎮","雲林縣西螺鎮","雲林縣土庫鎮","雲林縣北港鎮","雲林縣古坑鄉","雲林縣大埤鄉","雲林縣莿桐鄉","雲林縣林內鄉","雲林縣二崙鄉","雲林縣崙背鄉","雲林縣麥寮鄉","雲林縣東勢鄉","雲林縣褒忠鄉","雲林縣臺西鄉","雲林縣元長鄉","雲林縣四湖鄉","雲林縣口湖鄉","雲林縣水林鄉",
            "嘉義市東區","嘉義市西區",
            "義縣太保市","義縣朴子市","義縣布袋鎮","義縣大林鎮","義縣民雄鄉","義縣溪口鄉","義縣新港鄉","義縣六腳鄉","義縣東石鄉","義縣義竹鄉","義縣鹿草鄉","義縣水上鄉","義縣中埔鄉","義縣竹崎鄉","義縣梅山鄉","義縣番路鄉","義縣大埔鄉","義縣阿里山鄉",
            "臺南市新營區","臺南市鹽水區","臺南市白河區","臺南市柳營區","臺南市後壁區","臺南市東山區","臺南市麻豆區","臺南市下營區","臺南市六甲區","臺南市官田區","臺南市大內區","臺南市佳里區","臺南市學甲區","臺南市西港區","臺南市七股區","臺南市將軍區","臺南市北門區","臺南市新化區","臺南市善化區","臺南市新市區","臺南市安定區","臺南市山上區","臺南市玉井區","臺南市楠西區","臺南市南化區","臺南市左鎮區","臺南市仁德區","臺南市歸仁區","臺南市關廟區","臺南市龍崎區","臺南市永康區","臺南市東區","臺南市南區","臺南市北區","臺南市安南區","臺南市安平區","臺南市中西區",
            "高雄市鹽埕區","高雄市鼓山區","高雄市左營區","高雄市楠梓區","高雄市三民區","高雄市新興區","高雄市前金區","高雄市苓雅區","高雄市前鎮區","高雄市旗津區","高雄市小港區","高雄市鳳山區","高雄市林園區","高雄市大寮區","高雄市大樹區","高雄市大社區","高雄市仁武區","高雄市鳥松區","高雄市岡山區","高雄市橋頭區","高雄市燕巢區","高雄市田寮區","高雄市阿蓮區","高雄市路竹區","高雄市湖內區","高雄市茄萣區","高雄市永安區","高雄市彌陀區","高雄市梓官區","高雄市旗山區","高雄市美濃區","高雄市六龜區","高雄市甲仙區","高雄市杉林區","高雄市內門區","高雄市茂林區","高雄市桃源區","高雄市那瑪夏區",
            "屏東縣屏東市","屏東縣潮州鎮","屏東縣東港鎮","屏東縣恆春鎮","屏東縣萬丹鄉","屏東縣長治鄉","屏東縣麟洛鄉","屏東縣九如鄉","屏東縣里港鄉","屏東縣鹽埔鄉","屏東縣高樹鄉","屏東縣萬巒鄉","屏東縣內埔鄉","屏東縣竹田鄉","屏東縣新埤鄉","屏東縣枋寮鄉","屏東縣新園鄉","屏東縣崁頂鄉","屏東縣林邊鄉","屏東縣南州鄉","屏東縣佳冬鄉","屏東縣琉球鄉","屏東縣車城鄉","屏東縣滿州鄉","屏東縣枋山鄉","屏東縣三地門鄉","屏東縣霧臺鄉","屏東縣瑪家鄉","屏東縣泰武鄉","屏東縣來義鄉","屏東縣春日鄉","屏東縣獅子鄉","屏東縣牡丹鄉",
            "宜蘭縣宜蘭市","宜蘭縣羅東鎮","宜蘭縣蘇澳鎮","宜蘭縣頭城鎮","宜蘭縣礁溪鄉","宜蘭縣壯圍鄉","宜蘭縣員山鄉","宜蘭縣冬山鄉","宜蘭縣五結鄉","宜蘭縣三星鄉","宜蘭縣大同鄉","宜蘭縣南澳鄉",
            "花蓮縣花蓮市","花蓮縣鳳林鎮","花蓮縣玉里鎮","花蓮縣新城鄉","花蓮縣吉安鄉","花蓮縣壽豐鄉","花蓮縣光復鄉","花蓮縣豐濱鄉","花蓮縣瑞穗鄉","花蓮縣富里鄉","花蓮縣秀林鄉","花蓮縣萬榮鄉","花蓮縣卓溪鄉",
            "臺東縣臺東市","臺東縣成功鎮","臺東縣關山鎮","臺東縣卑南鄉","臺東縣鹿野鄉","臺東縣池上鄉","臺東縣東河鄉","臺東縣長濱鄉","臺東縣太麻里鄉","臺東縣大武鄉","臺東縣綠島鄉","臺東縣海端鄉","臺東縣延平鄉","臺東縣金峰鄉","臺東縣達仁鄉","臺東縣蘭嶼鄉",
            "澎湖縣馬公市","澎湖縣湖西鄉","澎湖縣白沙鄉","澎湖縣西嶼鄉","澎湖縣望安鄉","澎湖縣七美鄉",
            "金門縣金城鎮","金門縣金沙鎮","金門縣金湖鎮","金門縣金寧鄉","金門縣烈嶼鄉","金門縣烏坵鄉",
            "連江縣南竿鄉","連江縣北竿鄉","連江縣莒光鄉","連江縣東引鄉"]
    if '台' in address:
        address = address.replace('台','臺')
    for region in region_list:
        try:
            if region in address:
                user_region=region
        except:
            return TextSendMessage(text='此位置無法查詢，請再嘗試搜尋其他位置')
            
    res_get = requests.get(url)
    a = res_get.json()
    contents=dict()
    contents['type']='carousel'
    bubbles=[]
    i=1
    for b in a:
        ed_time = time.time()
        if i<=10 and user_region in b['機構地址'] and int(ed_time-st_time)<=15:
            # latitude_b , longitude_b = get_latitude_longtitude(b['機構地址'])
            # if abs(latitude_o-latitude_b)<0.1 and abs(longitude_o-longitude_b)<0.1:
            if b["機構名稱"] == '':
                b["機構名稱"] = 'X'
            if b["負責獸醫"] == '':
                b["負責獸醫"] = 'X'
            if b["機構電話"] == '':
                b["機構電話"] = 'X'
            if b["機構地址"] == '':
                b["機構地址"] = 'X'
            if b["字號"] == '':
                b["字號"] = 'X'
            if b["發照日期"] == '':
                b["發照日期"] = 'X'
            bubble = {
                        "type": "bubble",
                        "body": {
                            "type": "box",
                            "layout": "vertical",
                            "contents": [
                            {
                                "type": "text",
                                "text": b['機構名稱'],
                                "weight": "bold",
                                "size": "xxl",
                                "margin": "md",
                                "wrap": True,
                                "style": "normal",
                                "align": "center",
                                "color": "#a3c2c2"
                            },
                            {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": "聯絡資訊↓",
                                    "margin": "md",
                                    "size": "lg",
                                    "align": "start",
                                    "decoration": "none",
                                    "offsetBottom": "sm",
                                    "color": "#ddddbb"
                                },
                                {
                                    "type": "separator"
                                },
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "margin": "sm",
                                    "spacing": "sm",
                                    "contents": [
                                    {
                                        "type": "text",
                                        "text": "獸醫：　" + b['負責獸醫'],
                                        "size": "sm",
                                        "wrap": True,
                                        "align": "start"
                                    }
                                    ],
                                    "paddingTop": "sm"
                                },
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                    {
                                        "type": "text",
                                        "text": "電話：　"+b['機構電話'],
                                        "size": "sm",
                                        "wrap": True
                                    }
                                    ],
                                    "margin": "sm",
                                    "paddingTop": "sm"
                                },
                                {
                                    "type": "box",
                                    "layout": "horizontal",
                                    "contents": [
                                    {
                                        "type": "text",
                                        "text": "地址：　"+b['機構地址'],
                                        "size": "sm"
                                    }
                                    ],
                                    "margin": "sm",
                                    "paddingTop": "sm"
                                },
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "margin": "sm",
                                    "spacing": "sm",
                                    "contents": [
                                    {
                                        "type": "text",
                                        "text": "字號：　" + b['字號'],
                                        "size": "sm",
                                        "wrap": True,
                                        "align": "start"
                                    }
                                    ],
                                    "paddingTop": "sm"
                                }
                                ],
                                "paddingTop": "sm"
                            },
                            {
                                "type": "button",
                                "action": {
                                "type": "uri",
                                "label": "Map",
                                "uri": "https://www.google.com.tw/maps/place/" + urllib.parse.quote(b['機構地址'])
                                },
                                "height": "sm",
                                "style": "secondary",
                                "color": "#d0e1e1",
                                "margin": "md"
                            }
                            ]
                        },
                        "footer": {
                            "type": "box",
                            "layout": "horizontal",
                            "margin": "md",
                            "contents": [
                            {
                                "type": "text",
                                "text": "發照日期:",
                                "size": "xs",
                                "color": "#aaaaaa"
                            },
                            {
                                "type": "text",
                                "text": b['發照日期'][0:4]+'/'+b['發照日期'][4:6]+'/'+b['發照日期'][6:8],
                                "color": "#aaaaaa",
                                "size": "xs",
                                "align": "end"
                            }
                            ]
                        },
                        "styles": {
                            "footer": {
                            "separator": True
                            }
                        }
                        }
            bubbles.append(bubble)
            i+=1
            ed_time=time.time()


    if len(bubbles)!=0:
        contents['contents']=bubbles
        message = FlexSendMessage(alt_text='醫院資訊',contents=contents)
    elif len(bubbles)==0:
        message = TextSendMessage(text='附近未搜尋到寵物醫院相關資訊')
    return message












def pet_shopping(address):
    st_time = time.time()
    url = 'https://data.coa.gov.tw/Service/OpenData/TransService.aspx?UnitId=fNT9RMo8PQRO&$top=10000&$skip=0'
    region_list = ["基隆市中正區","基隆市七堵區","基隆市暖暖區","基隆市仁愛區","基隆市中山區","基隆市安樂區","基隆市信義區",
            "臺北市松山區","臺北市信義區","臺北市大安區","臺北市中山區","臺北市中正區","臺北市大同區","臺北市萬華區","臺北市文山區","臺北市南港區","臺北市內湖區","臺北市士林區","臺北市北投區",
            "新北市板橋區","新北市三重區","新北市中和區","新北市永和區","新北市新莊區","新北市新店區","新北市樹林區","新北市鶯歌區","新北市三峽區","新北市淡水區","新北市汐止區","新北市瑞芳區","新北市土城區","新北市蘆洲區","新北市五股區","新北市泰山區","新北市林口區","新北市深坑區","新北市石碇區","新北市坪林區","新北市三芝區","新北市石門區","新北市八里區","新北市平溪區","新北市雙溪區","新北市貢寮區","新北市金山區","新北市萬里區","新北市烏來區",
            "桃園市桃園區","桃園市中壢區","桃園市大溪區","桃園市楊梅區","桃園市蘆竹區","桃園市大園區","桃園市龜山區","桃園市八德區","桃園市龍潭區","桃園市平鎮區","桃園市新屋區","桃園市觀音區","桃園市復興區",
            "新竹市東區","新竹市北區","新竹市香山區",
            "新竹縣竹北市","新竹縣竹東鎮","新竹縣新埔鎮","新竹縣關西鎮","新竹縣湖口鄉","新竹縣新豐鄉","新竹縣芎林鄉","新竹縣橫山鄉","新竹縣北埔鄉","新竹縣寶山鄉","新竹縣峨眉鄉","新竹縣尖石鄉","新竹縣五峰鄉",
            "苗栗縣苗栗市","苗栗縣苑裡鎮","苗栗縣通霄鎮","苗栗縣竹南鎮","苗栗縣頭份市","苗栗縣後龍鎮","苗栗縣卓蘭鎮","苗栗縣大湖鄉","苗栗縣公館鄉","苗栗縣銅鑼鄉","苗栗縣南庄鄉","苗栗縣頭屋鄉","苗栗縣三義鄉","苗栗縣西湖鄉","苗栗縣造橋鄉","苗栗縣三灣鄉","苗栗縣獅潭鄉","苗栗縣泰安鄉",
            "臺中市中區","臺中市東區","臺中市南區","臺中市西區","臺中市北區","臺中市西屯區","臺中市南屯區","臺中市北屯區","臺中市豐原區","臺中市東勢區","臺中市大甲區","臺中市清水區","臺中市沙鹿區","臺中市梧棲區","臺中市后里區","臺中市神岡區","臺中市潭子區","臺中市大雅區","臺中市新社區","臺中市石岡區","臺中市外埔區","臺中市大安區","臺中市烏日區","臺中市大肚區","臺中市龍井區","臺中市霧峰區","臺中市太平區","臺中市大里區","臺中市和平區",
            "彰化縣彰化市","彰化縣鹿港鎮","彰化縣和美鎮","彰化縣線西鄉","彰化縣伸港鄉","彰化縣福興鄉","彰化縣秀水鄉","彰化縣花壇鄉","彰化縣芬園鄉","彰化縣員林市","彰化縣溪湖鎮","彰化縣田中鎮","彰化縣大村鄉","彰化縣埔鹽鄉","彰化縣埔心鄉","彰化縣永靖鄉","彰化縣社頭鄉","彰化縣二水鄉","彰化縣北斗鎮","彰化縣二林鎮","彰化縣田尾鄉","彰化縣埤頭鄉","彰化縣芳苑鄉","彰化縣大城鄉","彰化縣竹塘鄉","彰化縣溪州鄉",
            "南投縣南投市","南投縣埔里鎮","南投縣草屯鎮","南投縣竹山鎮","南投縣集集鎮","南投縣名間鄉","南投縣鹿谷鄉","南投縣中寮鄉","南投縣魚池鄉","南投縣國姓鄉","南投縣水里鄉","南投縣信義鄉","南投縣仁愛鄉",
            "雲林縣斗六市","雲林縣斗南鎮","雲林縣虎尾鎮","雲林縣西螺鎮","雲林縣土庫鎮","雲林縣北港鎮","雲林縣古坑鄉","雲林縣大埤鄉","雲林縣莿桐鄉","雲林縣林內鄉","雲林縣二崙鄉","雲林縣崙背鄉","雲林縣麥寮鄉","雲林縣東勢鄉","雲林縣褒忠鄉","雲林縣臺西鄉","雲林縣元長鄉","雲林縣四湖鄉","雲林縣口湖鄉","雲林縣水林鄉",
            "嘉義市東區","嘉義市西區",
            "義縣太保市","義縣朴子市","義縣布袋鎮","義縣大林鎮","義縣民雄鄉","義縣溪口鄉","義縣新港鄉","義縣六腳鄉","義縣東石鄉","義縣義竹鄉","義縣鹿草鄉","義縣水上鄉","義縣中埔鄉","義縣竹崎鄉","義縣梅山鄉","義縣番路鄉","義縣大埔鄉","義縣阿里山鄉",
            "臺南市新營區","臺南市鹽水區","臺南市白河區","臺南市柳營區","臺南市後壁區","臺南市東山區","臺南市麻豆區","臺南市下營區","臺南市六甲區","臺南市官田區","臺南市大內區","臺南市佳里區","臺南市學甲區","臺南市西港區","臺南市七股區","臺南市將軍區","臺南市北門區","臺南市新化區","臺南市善化區","臺南市新市區","臺南市安定區","臺南市山上區","臺南市玉井區","臺南市楠西區","臺南市南化區","臺南市左鎮區","臺南市仁德區","臺南市歸仁區","臺南市關廟區","臺南市龍崎區","臺南市永康區","臺南市東區","臺南市南區","臺南市北區","臺南市安南區","臺南市安平區","臺南市中西區",
            "高雄市鹽埕區","高雄市鼓山區","高雄市左營區","高雄市楠梓區","高雄市三民區","高雄市新興區","高雄市前金區","高雄市苓雅區","高雄市前鎮區","高雄市旗津區","高雄市小港區","高雄市鳳山區","高雄市林園區","高雄市大寮區","高雄市大樹區","高雄市大社區","高雄市仁武區","高雄市鳥松區","高雄市岡山區","高雄市橋頭區","高雄市燕巢區","高雄市田寮區","高雄市阿蓮區","高雄市路竹區","高雄市湖內區","高雄市茄萣區","高雄市永安區","高雄市彌陀區","高雄市梓官區","高雄市旗山區","高雄市美濃區","高雄市六龜區","高雄市甲仙區","高雄市杉林區","高雄市內門區","高雄市茂林區","高雄市桃源區","高雄市那瑪夏區",
            "屏東縣屏東市","屏東縣潮州鎮","屏東縣東港鎮","屏東縣恆春鎮","屏東縣萬丹鄉","屏東縣長治鄉","屏東縣麟洛鄉","屏東縣九如鄉","屏東縣里港鄉","屏東縣鹽埔鄉","屏東縣高樹鄉","屏東縣萬巒鄉","屏東縣內埔鄉","屏東縣竹田鄉","屏東縣新埤鄉","屏東縣枋寮鄉","屏東縣新園鄉","屏東縣崁頂鄉","屏東縣林邊鄉","屏東縣南州鄉","屏東縣佳冬鄉","屏東縣琉球鄉","屏東縣車城鄉","屏東縣滿州鄉","屏東縣枋山鄉","屏東縣三地門鄉","屏東縣霧臺鄉","屏東縣瑪家鄉","屏東縣泰武鄉","屏東縣來義鄉","屏東縣春日鄉","屏東縣獅子鄉","屏東縣牡丹鄉",
            "宜蘭縣宜蘭市","宜蘭縣羅東鎮","宜蘭縣蘇澳鎮","宜蘭縣頭城鎮","宜蘭縣礁溪鄉","宜蘭縣壯圍鄉","宜蘭縣員山鄉","宜蘭縣冬山鄉","宜蘭縣五結鄉","宜蘭縣三星鄉","宜蘭縣大同鄉","宜蘭縣南澳鄉",
            "花蓮縣花蓮市","花蓮縣鳳林鎮","花蓮縣玉里鎮","花蓮縣新城鄉","花蓮縣吉安鄉","花蓮縣壽豐鄉","花蓮縣光復鄉","花蓮縣豐濱鄉","花蓮縣瑞穗鄉","花蓮縣富里鄉","花蓮縣秀林鄉","花蓮縣萬榮鄉","花蓮縣卓溪鄉",
            "臺東縣臺東市","臺東縣成功鎮","臺東縣關山鎮","臺東縣卑南鄉","臺東縣鹿野鄉","臺東縣池上鄉","臺東縣東河鄉","臺東縣長濱鄉","臺東縣太麻里鄉","臺東縣大武鄉","臺東縣綠島鄉","臺東縣海端鄉","臺東縣延平鄉","臺東縣金峰鄉","臺東縣達仁鄉","臺東縣蘭嶼鄉",
            "澎湖縣馬公市","澎湖縣湖西鄉","澎湖縣白沙鄉","澎湖縣西嶼鄉","澎湖縣望安鄉","澎湖縣七美鄉",
            "金門縣金城鎮","金門縣金沙鎮","金門縣金湖鎮","金門縣金寧鄉","金門縣烈嶼鄉","金門縣烏坵鄉",
            "連江縣南竿鄉","連江縣北竿鄉","連江縣莒光鄉","連江縣東引鄉"]
    if '台' in address:
        address = address.replace('台','臺')
    for region in region_list:
        try:
            if region in address:
                user_region=region
        except:
            return TextSendMessage(text='此位置無法查詢，請再嘗試搜尋其他位置')
            
    res_get = requests.get(url)
    a = res_get.json()
    contents=dict()
    contents['type']='carousel'
    bubbles=[]
    i=1
    for b in a:
        ed_time = time.time()
        if i<=10 and user_region in b['legaladdress'] and (int(ed_time-st_time)<=15)  :
            # latitude_b , longitude_b = get_latitude_longtitude(b['機構地址'])
            # if abs(latitude_o-latitude_b)<0.1 and abs(longitude_o-longitude_b)<0.1:
            bu = []
            if 'A' in b['busitem'] :
                bu.append("繁殖")
            if 'B' in b['busitem'] :
                bu.append("買賣")
            if 'C' in b['busitem'] :
                bu.append("寄養")
            busitem1 = ''    
            for busitem in bu:
                busitem1 += '、'+busitem
            busitem = busitem1[1:]

            if b['rank_code'] == 'A':
                rank_code = '優等'
            elif b['rank_code'] == 'B':
                rank_code = '甲等'
            elif b['rank_code'] == 'C':
                rank_code = '乙等'
            elif b['rank_code'] == 'D':
                rank_code = '丙等'

            if b['legalname'] == '':
                b['legalname'] = 'X'
            if b['own_name'] == '':
                b['own_name'] = 'X'
            if b['legaladdress'] == '':
                b['legaladdress'] = 'X'
            if b['animaltype'] == '':
                b['animaltype'] = 'X'

            bubbles.append({
                            "type": "bubble",
                            "body": {
                                "type": "box",
                                "layout": "vertical",
                                "contents": [
                                {
                                    "type": "text",
                                    "text": b['legalname'],
                                    "weight": "bold",
                                    "size": "xxl",
                                    "margin": "md",
                                    "wrap": True,
                                    "style": "normal",
                                    "align": "center",
                                    "color": "#c6d9eb"
                                },
                                {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                    {
                                        "type": "text",
                                        "text": "店家資訊",
                                        "margin": "md",
                                        "size": "lg",
                                        "align": "start",
                                        "decoration": "none",
                                        "offsetBottom": "sm",
                                        "color": "#ffcccc"
                                    },
                                    {
                                        "type": "separator"
                                    },
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "margin": "sm",
                                        "spacing": "sm",
                                        "contents": [
                                        {
                                            "type": "text",
                                            "text": "負責人姓名：" + b['own_name'],
                                            "size": "md",
                                            "wrap": True,
                                            "align": "start"
                                        }
                                        ],
                                        "paddingTop": "sm"
                                    },
                                    {
                                        "type": "box",
                                        "layout": "horizontal",
                                        "contents": [
                                        {
                                            "type": "text",
                                            "text": "機構地址：" + b['legaladdress'],
                                            "size": "md",
                                            "wrap": True
                                        }
                                        ],
                                        "margin": "sm",
                                        "paddingTop": "sm"
                                    },
                                    {
                                        "type": "separator",
                                        "margin": "sm"
                                    },
                                    {
                                        "type": "box",
                                        "layout": "horizontal",
                                        "contents": [
                                        {
                                            "type": "text",
                                            "text": "業務項目：" + busitem, 
                                            "size": "md",
                                            "wrap": True
                                        }
                                        ],
                                        "margin": "sm",
                                        "paddingTop": "sm"
                                    },
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "margin": "sm",
                                        "spacing": "sm",
                                        "contents": [
                                        {
                                            "type": "text",
                                            "text": "特定種類：" + b['animaltype'],
                                            "size": "md",
                                            "wrap": True,
                                            "align": "start"
                                        }
                                        ],
                                        "paddingTop": "sm"
                                    },
                                    {
                                        "type": "box",
                                        "layout": "vertical",
                                        "margin": "sm",
                                        "spacing": "sm",
                                        "contents": [
                                        {
                                            "type": "text",
                                            "text": "評鑑等級：" + rank_code,
                                            "size": "md",
                                            "wrap": True,
                                            "align": "start"
                                        }
                                        ],
                                        "paddingTop": "sm"
                                    }
                                    ],
                                    "paddingTop": "sm"
                                },
                                {
                                    "type": "button",
                                    "action": {
                                    "type": "uri",
                                    "label": "Map",
                                    "uri": "https://www.google.com.tw/maps/place/" + urllib.parse.quote(b['legaladdress'])
                                    },
                                    "height": "sm",
                                    "style": "secondary",
                                    "color": "#eee6ff",
                                    "margin": "lg"
                                }
                                ]
                            },
                            "styles": {
                                "footer": {
                                "separator": True
                                }
                            }
                            })


            i+=1
            ed_time=time.time()

    if len(bubbles)!=0:
        contents['contents']=bubbles
        message = FlexSendMessage(alt_text='寵物店',contents=contents)
    elif len(bubbles)==0:
        message = TextSendMessage(text='附近未搜尋到寵物店相關資訊')
    return message