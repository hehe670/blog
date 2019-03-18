"""截"""
import redis
from flask import Flask
from flask_script import Manager
from flask_session import Session

from back.views import back_blue
from back.models import db
from web.views import web_blue

app = Flask(__name__)

app.register_blueprint(blueprint=back_blue, url_prefix='/hehe/')
app.register_blueprint(blueprint=web_blue, url_prefix='/web/')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:12345678@127.0.0.1:3306/blog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis.Redis(host='127.0.0.1', port=6379)
# ,password='yixi8144.yixi'
app.secret_key = '123123412'  # 配置secret_key,否则不能实现session对话

# 初始化，将登陆后的cookice存在redis里面
Session(app)
db.init_app(app)

manage = Manager(app)
if __name__ == '__main__':
    manage.run()
