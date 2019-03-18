from datetime import datetime

from flask import Blueprint, render_template, request, \
    redirect, url_for, session

# 密码加密与解密的包
from werkzeug.security import generate_password_hash, check_password_hash

from back.models import db, User, Fen_lei, Blogs
from utils.function import ff

back_blue = Blueprint('back', __name__)


# 登陆页面
@back_blue.route('/login/', methods=['GET', 'POST'])
def login():
    print('==========')
    if request.method == 'GET':
        return render_template('/back/login.html/')
    if request.method == 'POST':
        username = request.form.get('nameuser')
        password = request.form.get('password')
        u1 = User.query.filter(User.username == username).first()

        if username and password and u1:
            # 解析哈希密码，并判断与新的密码是否相等
            if check_password_hash(u1.password, password) and username == u1.username:
                session['user_id'] = u1.id
                return redirect(url_for('back.index'))
        else:
            cw = '帐号密码不能为空'
            return render_template('/back/login.html/', cw=cw)


# 登陆后的内容页面
@back_blue.route('/index/')
@ff
def index():
    return render_template('/back/index.html/')


@back_blue.route('/zhuce/', methods=['GET', 'POST'])
def zhuce():
    if request.method == 'GET':
        return render_template('/back/zhuce.html/')
    if request.method == 'POST':
        nameuser = request.form.get('nameuser')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        if nameuser and password:

            user = User.query.filter(User.username == nameuser).first()
            if user:
                cw = '用户名已经注册'
                return render_template('/back/zhuce.html/', cw=cw)
            else:
                if password == password2:

                    u1 = User()
                    u1.username = nameuser
                    u1.password = generate_password_hash(password)
                    u1.save()
                    return redirect(url_for('back.login'))
                else:
                    cw = '两次密码不一样'
                    return render_template('/back/zhuce.html/', cw=cw)

        else:
            cw = '请填写完整的信息'
            return render_template('/back/zhuce.html/', cw=cw)


@back_blue.route('/logout/', methods=['GET'])
@ff
def logout():
    del session['user_id']
    return redirect(url_for('back.login'))


@back_blue.route('/a_type/', methods=['GET', 'POST'])
def a_type():
    if request.method == "GET":
        a_typefenlei = Fen_lei.query.all()
        return render_template('back/type_fenlei_list.html', a_typefenlei=a_typefenlei)


@back_blue.route('/fenlei/', methods=['GET', 'POST'])
def fenlei():
    if request.method == "GET":
        return render_template('back/tianjiafenlei.html')
    if request.method == "POST":
        fenleiname = request.form.get('fenleiname')
        if fenleiname:
            # 保存分类信息
            fen = Fen_lei()
            fen.f_name = fenleiname
            db.session.add(fen)
            db.session.commit()
            return redirect(url_for('back.a_type'))
        else:
            cw = '请填写分类名'
            return render_template('back/tianjiafenlei.html', cw=cw)


@back_blue.route('/del_type/<int:id>/', methods=['GET'])
def del_type(id):
    afenlei = Fen_lei.query.get(id)
    db.session.delete(afenlei)
    db.session.commit()
    return redirect(url_for('back.a_type'))


# 文章列表页面.展示博客名，简介，写的时间
@back_blue.route('/article_list/', methods=['GET'])
def article_list():
    blogall = Blogs.query.all()
    type1 = Fen_lei.query.all()
    print(blogall)
    return render_template('back/article_list.html', blogall=blogall,type1=type1)


# 添加博客
@back_blue.route('/addblog/', methods=["GET", 'POST'])
def addblog():
    a_type2 = Fen_lei.query.all()
    if request.method == "GET":
        return render_template('back/addblog.html', a_type2=a_type2)
    if request.method == "POST":
        title = request.form.get('name')
        miaoshu = request.form.get('goods_sn')
        fenlei1 = request.form.get('category')
        lenrong = request.form.get('goods_brief')

        if title and lenrong:
            bke = Blogs()
            bke.title = title
            bke.desc = miaoshu
            bke.bcontent = lenrong
            bke.type = fenlei1

            bke.creste_date = datetime.now()
            db.session.add(bke)

            db.session.commit()
            print('============')
            return redirect(url_for('back.article_list'))

        else:
            cw = '请填写完整内容'
            return render_template('back/addblog.html', cw=cw)

# 修改
@back_blue.route('/addblog1/<int:id>/', methods=["GET", 'POST'])
def addblog1(id):
    if request.method == "GET":
        ablog1 = Blogs.query.get(id)

        a_type1 = Fen_lei.query.all()
        return render_template('back/addblog222.html', a_type1=a_type1,ablog1=ablog1)
    if request.method == "POST":
        title = request.form.get('name')
        miaoshu = request.form.get('goods_sn')
        fenlei1 = request.form.get('category')
        fenlei1 = Fen_lei.query.filter(Fen_lei.id == fenlei1).first()
        fenlei1 = fenlei1.id
        lenrong = request.form.get('goods_brief')
        if title and lenrong:
            bke = Blogs()
            bke.title = title
            bke.desc = miaoshu
            bke.bcontent = lenrong

            bke.type = fenlei1
            bke.creste_date = datetime.now()
            db.session.add(bke)
            db.session.commit()
            return redirect(url_for('back.article_list'))

        else:
            cw = '请填写完整内容'
            return render_template('back/addblog.html', cw=cw)

# 删除对应一行的博客
@back_blue.route('/del_blog/<int:id>', methods=['GET'])
def del_blog(id):
        ablog = Blogs.query.get(id)
        db.session.delete(ablog)
        db.session.commit()
        return redirect(url_for('back.article_list'))




