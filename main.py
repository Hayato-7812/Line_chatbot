import re
from flask import Flask, request, abort
import os
from db_handler import *
from youtube_utils import *

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
app = Flask(__name__)

#環境変数取得
# YOUR_CHANNEL_ACCESS_TOKEN = "4gqA1mKoeRc57EWpN7ghpb8mE2KrDidW4FAsMWpkM1n8js/+XsDQ4JgHuD5Sht2uI/MIGHS1nwE+SVrjX4kSJuaODDYWaUAsmbg5RPAa+Yegd1NJZv69Apx8a6CaQDa6xmxfogroZ1vxuInnGockqwdB04t89/1O/w1cDnyilFU="
# YOUR_CHANNEL_SECRET = "1dc09f06b2d107b6c1310c8507f07f41"

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
            TextSendMessage(text="Please input YouTube link on the keyboard!!"))

    elif event.message.text == "What are other people's favorite songs?":
        columns_list = []
        for item in get_items():
            print(item)
            columns_list.append(CarouselColumn(title=get_yt_info(item["uri"])["title"], 
                                thumbnail_image_url=get_yt_info(item["uri"])["thumbnail_url"],
                                text="recomended by: {}".format(item["rec_by"]),
                                # text="recomended by: {} \ncomment: {}".format(item["rec_by"],item["comment"]),
                                actions=[URIAction(label="Listen it",uri=item["uri"])]))
        carousel_template_message = TemplateSendMessage(
                        alt_text='music carousel',
                        template=CarouselTemplate(columns=columns_list)
            )
        line_bot_api.reply_message(event.reply_token, messages=carousel_template_message)
    
    elif event.message.text == " Visit the site!":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text))
    else:
        try: #本当はここで追加の確認したい
            input_url = event.message.text
            yt = get_yt_info(input_url)
            profile = line_bot_api.get_profile(event.source.user_id)
            account_name = profile.display_name
            item_obj = dbvalue_urls(
                _id=get_next_id(),
                _rec_date = dt.today(),
                _rec_by = account_name,
                _title=yt["title"],
                _uri= input_url,
                _comment = "Just try!"
            )
            add_item(item_obj)
            reply = "add  your favorite song \n'{}'\n to shared songs list!!".format(yt["title"])
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=reply))
        
        except Exception as e:
            print("error: {}".format(e))
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="I'm sorry. You input invalid link to share. \nPlease input valid link or contact the developer (Hama,Hayato)if you need support."))


if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)