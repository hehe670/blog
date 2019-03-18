from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(10), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_delete = db.Column(db.Boolean, default=0)  # 删除则显示1
    creste_date = db.Column(db.DateTime, default=datetime.now()) #　创建时间

    __tablename__ = 'user'

    def save(self):
        db.session.add(self)
        db.session.commit()

class Blogs(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    title = db.Column(db.String(20),nullable=False)  #　标题
    desc = db.Column(db.String(100)) # 博客简读
    bcontent = db.Column(db.Text,nullable=False)  # 博客内容
    creste_date = db.Column(db.DateTime, default=datetime.now())  # 创建时间
    type = db.Column(db.Integer,db.ForeignKey('fen_lei.id'))

    __tablename__='blogs'


class Fen_lei(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    f_name = db.Column(db.String(20),nullable=False)
    blogsid = db.relationship('Blogs', backref='b')

