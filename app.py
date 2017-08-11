# encoding=utf-8
from flask import Flask, render_template, session, redirect, url_for
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired


class EssayForm(FlaskForm):
    essay = TextAreaField('待分类文本', validators=[DataRequired()])
    submit = SubmitField('提交')


app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['MUSIC_FOLDER'] = 'static/musics'
manager = Manager(app)
bootstrap = Bootstrap(app)


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

