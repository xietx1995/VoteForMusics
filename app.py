# encoding=utf-8
from flask import Flask, render_template, session, redirect, url_for, request, flash
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
app.config['TABLE_NAME'] = 'musics_info'
# 防止CSRF攻击的密钥
app.config['SECRET_KEY'] = 'hard to guess string'
# 静态文件路径
app.config['MUSIC_FOLDER'] = 'static/musics'


# 服务器启动时，连接数据库
db = dt.connect_to_database(app.config['MYSQL_HOST'], app.config['MYSQL_USER'],
                            app.config['MYSQL_PASSWD'], app.config['DB_MUSICS'])


@app.route('/', methods=['GET', 'POST'])
def index():
    # 构造查询语句
    query_statement = 'SELECT * FROM ' + app.config['TABLE_NAME'] + ' LIMIT 10'

    # 在session中记录音乐的数量
    if not session.get('num_musics'):
        session['num_musics'] = 10

    # 查询音乐信息，并保存在session中
    musics = session.get('musics', dt.query(db, query_statement))
    # 取得session中音乐的数量
    n = session['num_musics']

    # 处理POST请求
    if request.method == 'POST':
        # 从form中获得用户评价信息，并写入数据库
        judge = request.form.getlist('choice')

        # 如果一个都没选，代表跳过
        if len(judge) == 0:
            session['num_musics'] -= 1
            # 如果已经评完，重定向到完成页面
            if session['num_musics'] == 0:
                session['finish'] = True
                return redirect(url_for('index'))
            return redirect(url_for('index'))

        # 判断选择数量是否符合要求
        if len(judge) > 4:
            flash('最多选4个，请重新选择')
            return redirect(url_for('index'))

        # 音乐记录的第零个字段为主键
        entry_id = musics[n-1][0]
        # 写数据
        dt.write(db, app.config['TABLE_NAME'], entry_id, judge)
        # 更新音乐数量
        session['num_musics'] -= 1
        # 显示提交成功的提示消息
        flash('提交成功，还剩余%d首歌' % session['num_musics'])

        # 如果已经评完，重定向到完成页面
        if session['num_musics'] == 0:
            session['finish'] = True
            return redirect(url_for('index'))

        return redirect(url_for('index'))

    # 处理GET请求
    return render_template('index.html', music=musics[n-1], n=n, finish=session.get('finish'))


@app.route('/finish')
def finish():
    return render_template('finish.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    manager.run()

