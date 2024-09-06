import os
from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from datetime import datetime
import logging

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Line Bot API 和 Webhook Handler 配置
    LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
    LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')

    line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
    handler = WebhookHandler(LINE_CHANNEL_SECRET)

    @app.route('/callback', methods=['POST'])
    def callback():
        # 取得請求並記錄log, 請求內容 = body
        signature = request.headers['X-Line-Signature']
        body = request.get_data(as_text=True)
        
        # 驗證請求, 取得時同時傳入驗證金鑰比對
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            abort(400)
        
        return 'OK'

    @handler.add(MessageEvent, message=TextMessage)
    def handle_message(event):
        # line bot會自動將收到的請求附值給event
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text)
        )
    
     # 設置允許的來源
    origins = ["http://localhost:8080", "http://localhost:5000/group"]
    CORS(app, resources={r"/*": {"origins": origins}})
    
    # 將app連接到database (本地開發用@localhost, 連上docker用@mysql)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql+mysqlconnector://solochiou:password@mysql:3310/split_the_bill')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize database ORM
    db.init_app(app)
    
    #管理資料庫遷移。保留現有的資料庫表和數據
    migrate = Migrate(app, db)
    
    # 設置日誌級別, 讓終端機可以用print 
    logging.basicConfig(level=logging.DEBUG)
    
    # 建立初始化資料庫
    with app.app_context():
        from .models import Group, User, Expense,SettleTheBalance
        # db.drop_all()
        # db.create_all()

    from .routes import main
    app.register_blueprint(main)

    return app
