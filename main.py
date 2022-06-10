
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import os

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
    if event.message.text == "test":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="success!!"))

    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text))




if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)