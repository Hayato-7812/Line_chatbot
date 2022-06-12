
from flask import Flask, request, abort
from db_handler import *

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,TemplateSendMessage,CarouselTemplate,CarouselColumn,
    PostbackEvent,
    QuickReply, QuickReplyButton

)
from linebot.models.actions import PostbackAction,URIAction
import os
import time
import re

app = Flask(__name__)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = "4gqA1mKoeRc57EWpN7ghpb8mE2KrDidW4FAsMWpkM1n8js/+XsDQ4JgHuD5Sht2uI/MIGHS1nwE+SVrjX4kSJuaODDYWaUAsmbg5RPAa+Yegd1NJZv69Apx8a6CaQDa6xmxfogroZ1vxuInnGockqwdB04t89/1O/w1cDnyilFU="
YOUR_CHANNEL_SECRET = "1dc09f06b2d107b6c1310c8507f07f41"

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/")
def Hello():
    return "Hello!!"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == "Share songs with others！":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="input link"))

    elif event.message.text == "What are other people's favorite songs?":
        columns_list = []
        # for item in get_items():
        #     columns_list.append(CarouselColumn(thumbnail_image_url=None,title="Music", text=f"recomended by {item.user}", actions=[URIAction(label="Listen it", uri=f"{item.url}")]))
        columns_list.append(CarouselColumn(thumbnail_image_url="https://www.google.com/imgres?imgurl=https%3A%2F%2Fi.ytimg.com%2Fvi%2FXaVPr6HVrbI%2Fmaxresdefault.jpg%3Fv%3D629f07c3&imgrefurl=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DXaVPr6HVrbI&tbnid=yL4OsrKsS4M-IM&vet=12ahUKEwjNgNHGsqf4AhVK6pQKHcTRCMsQMygAegQIARAd..i&docid=txOTwSxvgmSL2M&w=1280&h=720&q=%E5%BF%83%E8%BA%8D%E3%82%8B%E3%80%80%E3%83%95%E3%82%A1%E3%83%BC%E3%82%B9%E3%83%88%E3%83%86%E3%82%A4%E3%82%AF&ved=2ahUKEwjNgNHGsqf4AhVK6pQKHcTRCMsQMygAegQIARAd",title="nobodyknows+ - ココロオドル / THE FIRST TAKE", text=f"recomended by P", actions=[URIAction(label="Listen it", uri=f"https://www.youtube.com/watch?v=XaVPr6HVrbI")]))
        columns_list.append(CarouselColumn(thumbnail_image_url="data:image/jpeg;base64,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",title="sana/HoneyWorks 『言葉のいらない約束』", text=f"recomended by Hama", actions=[URIAction(label="Listen it", uri=f"https://www.youtube.com/watch?v=S0uHhAVinVM")]))
        carousel_template_message = TemplateSendMessage(
                        alt_text='this is a music carousel',
                        template=CarouselTemplate(columns=columns_list)
            )
        line_bot_api.reply_message(event.reply_token, messages=carousel_template_message)
    
    elif event.message.text == " Visit the site!":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text))

    elif event.message.text == "まさや":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="あお"))

    elif event.message.text == "P":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="いつもありがとう大好きだよ"))

    else: 
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text))


if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)