
from flask import Flask, request, abort
# from db_handler import *

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
        columns_list.append(CarouselColumn(title="nobodyknows+ - ココロオドル / THE FIRST TAKE", text=f"recomended by P", actions=[URIAction(label="Listen it", uri=f"https://www.youtube.com/watch?v=XaVPr6HVrbI")]))
        columns_list.append(CarouselColumn(title="sana/HoneyWorks 『言葉のいらない約束』", text=f"recomended by Hama", actions=[URIAction(label="Listen it", uri=f"https://www.youtube.com/watch?v=S0uHhAVinVM")]))
        carousel_template_message = TemplateSendMessage(
                        alt_text='this is a music carousel',
                        template=CarouselTemplate(columns=columns_list)
            )
        line_bot_api.reply_message(event.reply_token, messages=carousel_template_message)
    
    elif event.message.text == " Visit the site!":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text))
    else:
        pass


if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)