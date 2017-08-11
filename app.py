# encoding=utf-8
from flask import Flask, render_template, session, redirect, url_for
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired
from databaseTransaction import dt


class EssayForm(FlaskForm):
    essay = TextAreaField('待分类文本', validators=[DataRequired()])
    submit = SubmitField('提交')


app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)

# 连接MYSQL数据库需要的配置信息
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWD'] = 'daimao,./'
app.config['DB_MUSICS'] = 'musicslib'
# 防止CSRF攻击的密钥
app.config['SECRET_KEY'] = 'hard to guess string'
# 静态文件路径
app.config['MUSIC_FOLDER'] = 'static/musics'


# 服务器启动时，连接数据库
cursor = dt.connect_to_database(app.config['MYSQL_HOST'], app.config['MYSQL_USER'],
                                app.config['MYSQL_PASSWD'], app.config['DB_MUSICS'])


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')
    # user_agent = request.headers.get('User-Agent')
    # return '<h1>Hello World</h1><p>Your browser is %s</p>' % user_agent


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)
    # return '<h1>Hello, %s!</h1>' % name


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    # app.run(debug=True)
    manager.run()

