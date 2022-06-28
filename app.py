import re
from flask import Flask, request, abort,render_template, redirect
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

app = Flask(__name__,  static_url_path="/static")


#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

# Webページに関すること
@app.route("/contact_reqired")
def requied():
    return render_template("contact_required.html")

@app.route("/top_page", methods=["GET", "POST"])
def toppage():
    # お問い合わせフォームに関して
    if request.method == "POST":
        yourname = request.form.get("yourname")
        LINEname = request.form.get("LINEname")
        mail = request.form.get("mail")
        content = request.form.get("content")
        comment = request.form.get("comment")

        """
        PostgreSQLの書き方に準拠しなきゃ...だけど
        書き方が分からないので。Pちゃんに聞いてから直します。
        
        お問い合わせフォームで入力された内容をdbに格納したい!!
        上記の5つ+投稿時間を格納したdbを作成。
        """

        # 以下プログラム
        """
        from flask_sqlalchemy import SQLAlchemy
        from datetime import datetime
        import pytz

        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
        db = SQLAlchemy(app)

        class Post(db.Model):
            yourname = db.Column(db.String(80), nullable=False)
            LINEname = db.Column(db.String(80), nullable=False)
            mail = db.Column(db.String(80), unique=True, nullable=False)
            content = db.Column(db.String(50), nullable=False)
            comment = db.Column(db.String(500), nullable=False)
            created_at = db.Column(db.Datetime, nullable=False, default=datetime.now(pytz.timezone("Asia/Tokyo")))


        # インスタンス化
        post = Post(yourname=yourname, LINEname=LINEname, mail=mail, content=content, comment=comment)

        db.session.add(post)
        db.seseion.commit()

        """

        """
        まずやること
        $ python3
        $ from app import db
            # Warningがでるが気にしない
        $ db.create_all()
            # データベースを作成
        """

        return redirect("/contact_requied")

    else:
        return render_template("index.html")

@app.route("/sharedmusic")
def sharedmusic():
    return render_template("musiclist.html")

@app.route("/sharedmusic")
def sharemusic():
    return render_template("musiclist.html")

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
        items = get_items()
        random_select_items = items[:1] + random.sample(items[1:], 8)
        for item in random_select_items:
            print("item add to CarouselColumn : {}".format(item))
            columns_list.append(CarouselColumn(title=get_yt_info(item["uri"])["title"][:37]+"...", 
                                thumbnail_image_url=get_yt_info(item["uri"])["thumbnail_url"],
                                text="recomended by: {}".format(item["rec_by"]),
                                # text="recomended by: {} \ncomment: {}".format(item["rec_by"],item["comment"]),
                                actions=[URIAction(label="Listen",uri=item["uri"])]))
        carousel_template_message = TemplateSendMessage(
                        alt_text='music carousel',
                        template=CarouselTemplate(columns=columns_list)
            )
        line_bot_api.reply_message(event.reply_token, messages=carousel_template_message)
    
    elif event.message.text == "Visit the site!":
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