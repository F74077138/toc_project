import os
import requests
import bs4
#from lxml import etree
from bs4 import BeautifulSoup

#from bs4 import BeautifulSoup

from linebot import LineBotApi, WebhookParser
from linebot import models
from linebot.models import *
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, TemplateSendMessage, TemplateAction, Template, PostbackTemplateAction, ImageCarouselColumn, ImageCarouselTemplate, ButtonsTemplate, MessageTemplateAction, URITemplateAction, BaseSize, URIImagemapAction, ImagemapArea, MessageImagemapAction, ImageSendMessage, ImagemapSendMessage, CarouselTemplate, CarouselColumn


channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)

def send_button_message(id, img, title, uptext, labels, texts):
    line_bot_api = LineBotApi(channel_access_token)

    acts = []
    for i, lab in enumerate(labels):
        acts.append(
            MessageTemplateAction(
                label=lab,
                text=texts[i]
            )
        )

    message = TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(
            thumbnail_image_url=img,
            title=title,
            text=uptext,
            actions=acts
        )
    )
    line_bot_api.push_message(id, message)
    return "OK"


def send_image_carousel(id, imglinks, labels, texts):
    line_bot_api = LineBotApi(channel_access_token)
    cols = []
    for i, url in enumerate(imglinks):
        cols.append(
            ImageCarouselColumn(
                    image_url=url,
                    action=MessageTemplateAction(
                    label=labels[i],
                    text=texts[i]
                )
            )
        )
    message = TemplateSendMessage(
        alt_text='ImageCarousel template',
        template=ImageCarouselTemplate(columns=cols)
    )
    line_bot_api.push_message(id, message)
    return "OK"


def send_confirm_message(id, title, uptext, labels, texts):
    line_bot_api = LineBotApi(channel_access_token)

    Confirm_template = TemplateSendMessage(
        alt_text='confirm template',
        template=ConfirmTemplate(
            title=title,
            text=uptext,
            actions=[
                MessageTemplateAction(
                    label=labels[0],
                    text=texts[0]
                ),
                MessageTemplateAction(
                    label=labels[1],
                    text=texts[1]
                ),
            ]
        )
    )

    line_bot_api.push_message(id, Confirm_template)

    return "Ok"

def searchnewcartoon(userid, genreWant):
    line_bot_api = LineBotApi(channel_access_token)
    if genreWant == 'Comedy':
        r = requests.get('https://www.imdb.com/search/title/?title_type=tv_series&genres=animation&genres=Comedy&explore=title_type,genres&ref_=adv_explore_rhs')
        r.encoding = 'utf-8'

        soup = bs4.BeautifulSoup(r.text, 'lxml')
        t = ""

        for i, data in enumerate(soup.select('h3.lister-item-header a')):
            if i > 4:
                break
            t += data.text + ': ' + 'https://www.imdb.com' + data['href'] + '\n\n'

        push_message1(userid, t)
    elif genreWant == 'Adventure':
        r = requests.get('https://www.imdb.com/search/title/?title_type=tv_series&genres=animation&genres=Adventure&explore=title_type,genres&ref_=adv_explore_rhs')
        r.encoding = 'utf-8'

        soup = bs4.BeautifulSoup(r.text, 'lxml')
        t = ""

        for i, data in enumerate(soup.select('h3.lister-item-header a')):
            if i > 4:
                break
            t += data.text + ': ' + 'https://www.imdb.com' + data['href'] + '\n\n'

        push_message1(userid, t)
    elif genreWant == 'Drama':
        r = requests.get('https://www.imdb.com/search/title/?title_type=tv_series&genres=animation&genres=Drama&explore=title_type,genres&ref_=adv_explore_rhs')
        r.encoding = 'utf-8'

        soup = bs4.BeautifulSoup(r.text, 'lxml')
        t = ""

        for i, data in enumerate(soup.select('h3.lister-item-header a')):
            if i > 4:
                break
            t += data.text + ': ' + 'https://www.imdb.com' + data['href'] + '\n\n'

        push_message1(userid, t)
    else:
        push_message1(userid, "Oops! You chose wrong genre((")
        send_sticker(userid, '11539', '52114121')


def searchcartoon(userid, cartoontofind):
    if cartoontofind == 'Daria':
        result = "8/10 (IMDB)\n"
        result += "A smart and cynical girl goes through teenage life as a proud outsider in a world of mainly idiotic adolescents and condescending adults."
        push_message1(userid, result)
        url1 = "https://youtu.be/2TAGtY1SsfU"
        #send_text_message(reply_token, url1)
        push_message1(userid, url1)
    elif cartoontofind == 'Hilda':
        result = "8.6/10 (IMDB)\n"
        result += "A fearless blue-haired girl named Hilda leaves the forest to go to town and find new friends, great adventures, magic and mysterious creatures who might be dangerous. "
        push_message1(userid, result)
        url1 = "https://youtu.be/XCojP2Ubuto"
        push_message1(userid, url1)
        #send_text_message(reply_token, url1)
    elif cartoontofind == 'Gravity Falls':
        result = "8.9/10 (IMDB)\n"
        result += "Twin siblings Dipper and Mabel Pines spend the summer at their great-uncle's tourist trap in the enigmatic Gravity Falls, Oregon. "
        push_message1(userid, result)
        url1 = "https://youtu.be/X2DUpDxFJyg"
        push_message1(userid, url1)
        #send_text_message(reply_token, url1)
    elif cartoontofind == 'Infinity train':
        result = "8.4/10 (IMDB)\n"
        result += "Various people find themselves on a mysterious train with an endless number of cars, each one being its own universe, and they must find a way to get home in this animated anthology series. "
        push_message1(userid, result)
        url1 = "https://youtu.be/atutlhoyc_Q"
        push_message1(userid, url1)
        #send_text_message(reply_token, url1)
    else:
        push_message1(userid, "Oops! It's not my favorite cartoon((")
        send_sticker(userid, '11537', '52002754')


def shownew(id):
    line_bot_api = LineBotApi(channel_access_token)
    r = requests.get('https://www.imdb.com/list/ls040600443/')
    r.encoding = 'utf-8'

    soup = bs4.BeautifulSoup(r.text, 'lxml')
    t = ""

    for i, data in enumerate(soup.select('h3.lister-item-header a')):
        if i > 4:
            break
        t += data.text + ': ' + 'https://www.imdb.com' + data['href'] + '\n\n'

    push_message1(id, t)


def push_message1(userid, msg):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.push_message(userid, TextSendMessage(text=msg))
    return "OK"


def send_sticker(id, package_id, sticker_id):
    line_bot_api = LineBotApi(channel_access_token)
    message = StickerSendMessage(
        package_id=package_id,
        sticker_id=sticker_id
    )
    line_bot_api.push_message(id, message)


def send_text_message(reply_token, text):
    line_bot_api = LineBotApi(channel_access_token)
    line_bot_api.reply_message(reply_token, TextSendMessage(text=text))

    return "OK"


"""
def send_image_url(id, img_url):
    pass

def send_button_message(id, text, buttons):
    pass
"""
