from flask import Blueprint,render_template

from back.models import Fen_lei, Blogs

web_blue = Blueprint('web',__name__)


@web_blue.route('/index/')
def index():
    # fenlei = Fen_lei.query.all()
    web_blog = Blogs.query.all()
    return render_template('web/index.html', web_blog=web_blog)


@web_blue.route('/about/')
def about():
    return render_template('web/about.html')


@web_blue.route('/content/<int:id>')
def content(id):
    web_blog1 = Blogs.query.get(id)
    webblogs = Blogs.query.all()
    return render_template('web/content.html',web_blog1=web_blog1,webblogs=webblogs)