# encoding=utf-8
from flask import Flask, render_template, session, redirect, url_for, request, flash
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired
from databaseTransaction import dt
from music_clustering import mc
from test_decomposition import td
import sys
import time
import numpy as np


reload(sys)
sys.setdefaultencoding('utf8')


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
# 音乐导入密码
app.config['IMPORT_PASSWD'] = 'qwer1234'


@app.route('/', methods=['GET', 'POST'])
def index():
    # 在session中记录音乐的数量
    if not session.get('num_musics'):
        session['num_musics'] = 10

    # 用户第一次访问时，获取音乐信息，并保存在session中
    if not session.get('musics'):
        # 构造查询语句
        query_statement = 'SELECT * FROM ' + app.config['TABLE_NAME'] + ' LIMIT 10'
        # 连接数据库
        db = dt.connect_to_database(app.config['MYSQL_HOST'], app.config['MYSQL_USER'],
                                    app.config['MYSQL_PASSWD'], app.config['DB_MUSICS'])
        # 查询音乐信息，并保存在session中
        session['musics'] = dt.query(db, query_statement)
        db.close()

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
        entry_id = session['musics'][n-1][0]

        # 连接数据库
        db = dt.connect_to_database(app.config['MYSQL_HOST'], app.config['MYSQL_USER'],
                                    app.config['MYSQL_PASSWD'], app.config['DB_MUSICS'])
        # 写数据
        dt.write(db, app.config['TABLE_NAME'], entry_id, judge)
        # 断开连接
        db.close()
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
    return render_template('index.html', music=session['musics'][n-1], n=n, finish=session.get('finish'))


@app.route('/finish')
def finish():
    return render_template('finish.html')


@app.route('/guide')
def guide():
    return render_template('guide.html')


@app.route('/import', methods=['GET', 'POST'])
def import_musics():
    # 在session中保存验证信息
    if not session.get('verified'):
        session['verified'] = False

    # 处理POST请求
    if request.method == 'POST':
        if not session['verified']:
            passwd = request.form.get('password')
            if passwd == app.config['IMPORT_PASSWD']:
                session['verified'] = True
                return render_template('import.html', verified=session['verified'])
            else:
                flash('Verification code is not correct')
        else:
            # 获得歌曲信息
            names = request.form.getlist('name')
            urls = request.form.getlist('url')
            absolutes = request.form.getlist('absolute')

            # 连接数据库
            db = dt.connect_to_database(app.config['MYSQL_HOST'], app.config['MYSQL_USER'],
                                        app.config['MYSQL_PASSWD'], app.config['DB_MUSICS'])
            # 插入新记录
            num_musics = dt.insert(db, app.config['TABLE_NAME'], names, absolutes, urls)
            # 断开连接
            db.close()
            flash('inserted %d new musics' % num_musics)

    # 处理GET请求
    return render_template('import.html', verified=session['verified'])


@app.route('/query')
def info():
    sql_statement = 'SELECT * FROM ' + app.config['TABLE_NAME']
    # 连接数据库
    db = dt.connect_to_database(app.config['MYSQL_HOST'], app.config['MYSQL_USER'],
                                app.config['MYSQL_PASSWD'], app.config['DB_MUSICS'])
    musics = dt.query(db, sql_statement)
    db.close()
    return render_template('info.html', musics=musics)


@app.route('/cluster', methods=['GET', 'POST'])
def cluster():
    # 构造查询语句
    query_statement = 'SELECT * FROM ' + app.config['TABLE_NAME']
    # 连接数据库
    db = dt.connect_to_database(app.config['MYSQL_HOST'], app.config['MYSQL_USER'],
                                app.config['MYSQL_PASSWD'], app.config['DB_MUSICS'])
    # 查询音乐信息
    musics = dt.query(db, query_statement)
    db.close()

    # 音乐的数量
    len_m = len(musics)

    if request.method == 'POST':
        # 执行聚类算法
        try:
            k = int(request.form.get('k'))
        except ValueError:
            flash("请输入整数")
            return render_template('cluster.html', len_m=len_m)

        if k < 1:
            flash("聚类数必须大于等于1")
            return render_template('cluster.html', len_m=len_m)
        elif k > len_m:
            flash("聚类数必须小于等于歌曲的数量: %d" % len_m)
            return render_template('cluster.html', len_m=len_m)

        sentiments = mc.get_sentiments(musics)
        kmeans = mc.cluster_musics(list(sentiments), k)
        img_filename = str(time.time()) + '.png'
        td.decomp(np.mat(sentiments), img_filename, kmeans.labels_)

        # 构造聚类字典
        clusters = {}
        num_cluster = len(kmeans.cluster_centers_)
        for i in range(num_cluster):
            clusters['%d' % i] = []  # i用于在页面顺序显示聚类

        labels = kmeans.labels_.tolist()
        # print labels
        for i in range(len(musics)):
            music_info = [musics[i][1], musics[i][-1]]  # 歌名和播放地址
            clusters['%d' % labels[i]].append(music_info)

        # print clusters
        return render_template('cluster.html', clusters=clusters, len_m=len_m, img_filename=img_filename)

    return render_template('cluster.html', len_m=len_m)


# 此路由用于将聚类结果写入数据库
@app.route('/admin/cluster/<int:k>')
def admin_cluster(k):
    # 构造查询语句
    query_statement = 'SELECT * FROM ' + app.config['TABLE_NAME']
    # 连接数据库
    db = dt.connect_to_database(app.config['MYSQL_HOST'], app.config['MYSQL_USER'],
                                app.config['MYSQL_PASSWD'], app.config['DB_MUSICS'])
    # 查询音乐信息
    musics = dt.query(db, query_statement)

    sentiments = mc.get_sentiments(musics)  # 获得情感列表
    # print 'sentiments:'
    # print sentiments
    # print 'k:', k
    kmeans = mc.cluster_musics(list(sentiments), int(k))  # 聚类
    mc.write_cluster_to_database(kmeans.labels_.tolist(), db, app.config['TABLE_NAME'])
    db.close()

    return 'Succeed'


@app.route('/analysis/<essay>')
def analysis(essay):
    from sentimentAnalysis import sa  # 导入情感分析模块
    word_list = sa.word_segmentation(essay=essay)  # 分词
    word_freq = sa.frequency_count(word_list)  # 词频统计
    word_info = sa.make_query(word_freq)  # 获得词语信息
    sentiment = sa.method_weighted_word_freq(word_info=word_info, word_freq=word_freq)  # 获得情感分类


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
