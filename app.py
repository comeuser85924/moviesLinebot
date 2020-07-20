
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import configparser

import random
import requests

app = Flask(__name__)

# LINE 聊天機器人的基本資料
config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))


# 近期上映
comimg_movieUrl = 'https://capi.showtimes.com.tw/1/programs/listUpcomingForStore/1?days=30&nocache=0'
comimgv_res = requests.get(comimg_movieUrl)
comimgArray = comimgv_res.json()['payload']['programs']
# 現正熱映
listPopularForStore = 'https://capi.showtimes.com.tw/1/programs/listPopularForStore/1?nocache=0'
popular_res = requests.get(listPopularForStore)
popularArray = popular_res.json()['payload']['programs']
# 電影時刻表
listPopularForStore = 'https://capi.showtimes.com.tw/1/programs/listPopularForStore/1?nocache=0'
popular_res = requests.get(listPopularForStore)
popularArray = popular_res.json()['payload']['programs']

# 電影時刻表flex message
def moviesList2():
    return{
        "type": "bubble",
        "hero": {
            "type": "image",
            "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_3_movie.png",
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover",
            "action": {
                "type": "uri",
                "uri": "http://linecorp.com/"
            }
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "spacing": "md",
            "contents": [
                {
                    "type": "text",
                    "text": "屍速列車：感染半島",
                    "wrap": True,
                    "weight": "bold",
                    "gravity": "center",
                    "size": "xl"
                },
                {
                    "type": "box",
                    "layout": "baseline",
                    "margin": "md",
                    "contents": [
                        {
                            "type": "text",
                            "text": "欣欣秀泰 影廳時刻表(07/20)",
                            "size": "sm",
                            "color": "#999999",
                            "margin": "md",
                            "flex": 0
                        }
                    ]
                },
                {
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
                                    "text": "1廳",
                                    "color": "#aaaaaa",
                                    "size": "sm",
                                    "flex": 1
                                },
                                {
                                    "type": "text",
                                    "text": "10:20 12:40 15:00 17:20 19:40 22:00 00:20",
                                    "wrap": True,
                                    "size": "sm",
                                    "color": "#666666",
                                    "flex": 4
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
                                    "text": "2廳",
                                    "color": "#aaaaaa",
                                    "size": "sm",
                                    "flex": 1
                                },
                                {
                                    "type": "text",
                                    "text": "11:20 13:40 16:00 18:20 20:40 23:00 01:20",
                                    "wrap": True,
                                    "color": "#666666",
                                    "size": "sm",
                                    "flex": 4
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    }

# 現正熱映、近期上映 flex message
def handleMoviesList(array, types):
    moviesList = []
    for item in array:
        if 'rating' in item:
            moviesList.append(
                {
                    'type': 'bubble',
                    'direction': 'ltr',
                    "hero": {
                        "type": "image",
                        "url": item['coverImagePortrait']['url'],
                        "size": "full",
                        "aspectRatio": "20:13",
                        "aspectMode": "cover",
                        "action": {
                            "type": "uri",
                            "uri": "https://www.showtimes.com.tw/events/byProgram/"+str(item['id'])
                        }
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": item['name'],
                                "weight": "bold",
                                "size": "xl"
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "margin": "md",
                                "contents": [
                                    {
                                        "type": "icon",
                                        "size": "3xl",
                                        "url": "https://www.showtimes.com.tw/images/rating/ic_rating_"+item['rating']+".png"
                                    },
                                    {
                                        "type": "text",
                                        "text": "上映日期:"+item['availableAt'][0:10],
                                        "size": "sm",
                                        "color": "#999999",
                                        "margin": "md",
                                        "flex": 0
                                    }
                                ]

                            },
                            {
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
                                                "text": "介紹",
                                                "color": "#aaaaaa",
                                                "size": "sm",
                                                "flex": 1
                                            },
                                            {
                                                "type": "text",
                                                "text": item['description'][0:50] + '...',
                                                "wrap": True,
                                                "color": "#666666",
                                                "size": "sm",
                                                "flex": 5
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    },
                    "footer": {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "button",
                                "style": "link",
                                "height": "sm",
                                "action": {
                                    "type": "message",
                                    "label": "預告片",
                                    "text": types + item['name'] + "預告片"
                                }
                            },
                            {
                                "type": "button",
                                "style": "link",
                                "height": "sm",
                                "action": {
                                    "type": "message",
                                    "label": "海報",
                                    "text": types + item['name'] + "海報"
                                }
                            },
                            {
                                "type": "spacer",
                                "size": "sm"
                            }
                        ],
                        "flex": 0
                    }
                }
            )
        else:
            moviesList.append(
                {
                    'type': 'bubble',
                    'direction': 'ltr',
                    "hero": {
                        "type": "image",
                        "url": item['coverImagePortrait']['data'],
                        "size": "full",
                        "aspectRatio": "20:13",
                        "aspectMode": "cover",
                        "action": {
                            "type": "uri",
                            "uri": "https://www.showtimes.com.tw/events/byProgram/"+str(item['id'])
                        }
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": item['name'],
                                "weight": "bold",
                                "size": "xl"
                            },
                            {
                                "type": "box",
                                "layout": "baseline",
                                "margin": "md",
                                "contents": [
                                    {
                                        "type": "text",
                                        "text": "上映日期:"+item['availableAt'][0:10],
                                        "size": "sm",
                                        "color": "#999999",
                                        "margin": "md",
                                        "flex": 0
                                    }
                                ]

                            },
                            {
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
                                                "text": "介紹",
                                                "color": "#aaaaaa",
                                                "size": "sm",
                                                "flex": 1
                                            },
                                            {
                                                "type": "text",
                                                "text": item['description'][0:50] + '...',
                                                "wrap": True,
                                                "color": "#666666",
                                                "size": "sm",
                                                "flex": 5
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    },
                    "footer": {
                        "type": "box",
                        "layout": "vertical",
                        "spacing": "sm",
                        "contents": [
                            {
                                "type": "button",
                                "style": "link",
                                "height": "sm",
                                "action": {
                                    "type": "message",
                                    "label": "預告片",
                                    "text": types + item['name'] + "預告片"
                                }
                            },
                            {
                                "type": "button",
                                "style": "link",
                                "height": "sm",
                                "action": {
                                    "type": "message",
                                    "label": "海報",
                                    "text": types + item['name'] + "海報"
                                }
                            },
                            {
                                "type": "spacer",
                                "size": "sm"
                            }
                        ],
                        "flex": 0
                    }
                }
            )
    return moviesList[0:10]

# 接收 LINE 的資訊


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        print(body, signature)
        handler.handle(body, signature)

    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    msg = event.message.text
    # print(type(msg))
    msg = msg.encode('utf-8')
    # 如果是近期上映 預告片/海報
    if ('近期上映' in event.message.text and '預告片' in event.message.text) or ('近期上映' in event.message.text and '海報' in event.message.text):
        for item in comimgArray:
            if event.message.text == '近期上映' + item['name'] + '預告片':
                print(item['previewVideo']['url'])
                # 回傳預告片
                line_bot_api.reply_message(
                    event.reply_token, VideoSendMessage(
                        original_content_url='https://www.youtube.com/embed/BmN0ixUUjig?rel=0', preview_image_url=item['previewVideo']['thumb'])
                )
            elif event.message.text == '近期上映' + item['name'] + '海報':
                print(item['coverImagePortrait']['url'])
                # 回傳海報
                line_bot_api.reply_message(event.reply_token, ImageSendMessage(
                    original_content_url=item['coverImagePortrait']['url'], preview_image_url=item['coverImagePortrait']['url']))
    # 如果是現正熱映 預告片/海報
    elif ('現正熱映' in event.message.text and '預告片' in event.message.text) or ('現正熱映' in event.message.text and '海報' in event.message.text):
        for item in popularArray:
            if event.message.text == '現正熱映' + item['name'] + '預告片':
                print(item['previewVideo']['url'])
                # 回傳預告片
                line_bot_api.reply_message(
                    event.reply_token, VideoSendMessage(
                        original_content_url=item['previewVideo']['url'], preview_image_url=item['previewVideo']['thumb'])
                )
            elif event.message.text == '現正熱映' + item['name'] + '海報':
                print(item['coverImagePortrait']['url'])
                # 回傳海報
                line_bot_api.reply_message(event.reply_token, ImageSendMessage(
                    original_content_url=item['coverImagePortrait']['url'], preview_image_url=item['coverImagePortrait']['url']))
    # 近期上映
    elif event.message.text == "近期上映":
        flex_message = FlexSendMessage(
            alt_text='你好，以下為近期上映的電影',
            contents={
                "type": "carousel",
                "contents": handleMoviesList(comimgArray, '近期上映')
            }
        )
        line_bot_api.reply_message(event.reply_token, flex_message)
    # 現正熱映
    elif event.message.text == "現正熱映":
        flex_message = FlexSendMessage(
            alt_text='你好，以下為現正熱映的電影',
            contents={
                "type": "carousel",
                "contents": handleMoviesList(popularArray, '現正熱映')
            }
        )
        line_bot_api.reply_message(event.reply_token, flex_message)
    # 電影時刻表
    elif event.message.text == "電影時刻表":
        flex_message = FlexSendMessage(
            alt_text='你好，以下為電影時刻表',
            contents={
                "type": "carousel",
                "contents": moviesList2(popularArray, '電影時刻表')
            }
        )
        line_bot_api.reply_message(event.reply_token, flex_message)

    # 以下為暫定測試模板
    elif event.message.text == "文字":
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text))
    elif event.message.text == "貼圖":
        line_bot_api.reply_message(
            event.reply_token, StickerSendMessage(package_id=1, sticker_id=2))
    elif event.message.text == "圖片":
        line_bot_api.reply_message(event.reply_token, ImageSendMessage(
            original_content_url='圖片網址', preview_image_url='圖片網址'))
    elif event.message.text == "影片":
        line_bot_api.reply_message(event.reply_token, VideoSendMessage(
            original_content_url='影片網址', preview_image_url='預覽圖片網址'))
    elif event.message.text == "音訊":
        line_bot_api.reply_message(event.reply_token, AudioSendMessage(
            original_content_url='音訊網址', duration=100000))
    elif event.message.text == "位置":
        line_bot_api.reply_message(event.reply_token, LocationSendMessage(
            title='my location', address='Tainan', latitude=22.994821, longitude=120.196452))
    elif event.message.text == "位置2":
        imagemap_message = ImagemapSendMessage(
            base_url='',
            alt_text='this is an imagemap',
            base_size=BaseSize(height=520, width=520),
            actions=[
                URIImagemapAction(
                    link_uri='',
                    area=ImagemapArea(
                        x=174, y=65, width=707, height=416
                    )
                ),
                MessageImagemapAction(
                    text='hello',
                    area=ImagemapArea(
                        x=520, y=0, width=520, height=520
                    )
                )
            ]
        )
        line_bot_api.reply_message(event.reply_token, imagemap_message)
    elif event.message.text == "樣板":
        buttons_template = TemplateSendMessage(
            alt_text='目錄 template',
            template=ButtonsTemplate(
                title='Template-樣板介紹',
                text='Template分為四種，也就是以下四種：',
                thumbnail_image_url='https://example.com/bot/images/image.jpg',
                actions=[
                    MessageTemplateAction(
                        label='Buttons Template',
                        text='Buttons Template'
                    ),
                    MessageTemplateAction(
                        label='Confirm template',
                        text='Confirm template'
                    ),
                    MessageTemplateAction(
                        label='Carousel template',
                        text='Carousel template'
                    ),
                    MessageTemplateAction(
                        label='Image Carousel',
                        text='Image Carousel'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
    elif event.message.text == "Buttons Template":
        buttons_template = TemplateSendMessage(
            alt_text='Buttons Template',
            template=ButtonsTemplate(
                title='這是ButtonsTemplate',
                text='ButtonsTemplate可以傳送text,uri',
                thumbnail_image_url='https://example.com/bot/images/image.jpg',
                actions=[
                    MessageTemplateAction(
                        label='ButtonsTemplate',
                        text='ButtonsTemplate'
                    ),
                    URITemplateAction(
                        label='VIDEO1',
                        uri='影片網址'
                    ),
                    PostbackTemplateAction(
                        label='postback',
                        text='postback text',
                        data='postback1'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)   
    elif event.message.text == "Confirm template":
        print("Confirm template")
        Confirm_template = TemplateSendMessage(
            alt_text='目錄 template',
            template=ConfirmTemplate(
                title='這是ConfirmTemplate',
                text='這就是ConfirmTemplate,用於兩種按鈕選擇',
                actions=[
                    PostbackTemplateAction(
                        label='Y',
                        text='Y',
                        data='action=buy&itemid=1'
                    ),
                    MessageTemplateAction(
                        label='N',
                        text='N',
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, Confirm_template)
    elif event.message.text == "Image Carousel":
        print("Image Carousel")
        Image_Carousel = TemplateSendMessage(
            alt_text='Image Carousel template',
            template=ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                        image_url='圖片網址',
                        action=PostbackTemplateAction(
                            label='postback1',
                            text='postback text1',
                            data='action=buy&itemid=1'
                        )
                    ),
                    ImageCarouselColumn(
                        image_url='圖片網址',
                        action=PostbackTemplateAction(
                            label='postback2',
                            text='postback text2',
                            data='action=buy&itemid=2'
                        )
                    )
                ]

            )
        )
        line_bot_api.reply_message(event.reply_token, Image_Carousel)
    return 'OK2'


if __name__ == "__main__":
    app.run()
