from flask import Flask, render_template, redirect, request, url_for, jsonify
from data import db_session
from data.db_session import global_init, create_session
from imports import *
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from datetime import datetime
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ultra_secret_key'
global_init('db/lets_blog.db')
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


def render(template, **kwargs):
    session = create_session()
    flows = session.query(Flow).all()
    return render_template(template, flows=flows, **kwargs)


@app.route('/')
@app.route('/flow')
def default():
    session = create_session()
    return render('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password2.data:
            return render_template('signup.html', form=form,
                                   message="Пароли не совпадают")
        session = create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('signup.html', form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            email=form.email.data,
            nick=form.nick.data)
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/')
    return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('signin.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('signin.html', form=form)


# @app.route('/feed')
# @login_required
# def feed():
#     pass


@app.route('/users/<nick>')
def profile(nick):
    session = create_session()
    user = session.query(User).filter(User.nick == nick).first()
    if not user:
        return render('error_404.html')
    return render('profile.html', user=user)


@app.route('/users/<nick>/public')
def prof_public(nick):
    session = create_session()
    user = session.query(User).filter(User.nick == nick).first()
    if not user:
        return render('error_404.html')
    return render('profile_public.html', user=user)


@app.route('/users/<nick>/bookmarks')
def prof_bookmarks(nick):
    session = create_session()
    user = session.query(User).filter(User.nick == nick).first()
    if not user:
        return render('error_404.html')
    return render('profile_bookmarks.html', user=user)


# @app.route('/users/<nick>/subscribers')
# def prof_subs(nick):
#     pass
#
#
# @app.route('/users/<nick>/subscriptions')
# def prof_subscriptions(nick):
#     pass
#
#
# @app.route('/users/<nick>/rate')
# def prof_rate(nick):
#     pass


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def prof_settings():
    session = create_session()
    if request.method == 'GET':
        user = User(
            surname=current_user.surname if current_user.surname else '',
            name=current_user.name if current_user.name else '',
            nick=current_user.nick if current_user.nick else '',
            info=current_user.info if current_user.info else '',
            work=current_user.work if current_user.work else '',
            date_born=current_user.date_born if current_user.date_born else ''
        )
        return render('settings.html', user=user)
    elif request.method == 'POST':
        a = request.form['born'].split('-')
        date1 = datetime.date(int(a[0]), int(a[1]), int(a[2]))
        if request.files['avatar']:
            ava = request.files['avatar']
            rassh = ava.filename.split('.')[-1]
            ava.save(f'./static/img/avatars/{current_user.id}.{rassh}')
            sl = {
                'surname': request.form['surname'],
                'name': request.form['name'],
                'nick': request.form['nick'],
                'info': request.form['info'],
                'work': request.form['work'],
                'date_born': date1,
                'avatar': f'{current_user.id}.{rassh}',
            }
        else:
            sl = {
                'surname': request.form['surname'],
                'name': request.form['name'],
                'nick': request.form['nick'],
                'info': request.form['info'],
                'work': request.form['work'],
                'date_born': date1,
            }
        session.query(User).filter(User.id == current_user.id).update(sl)
        session.commit()
        return redirect(f'/users/{current_user.nick}')


# @app.route('/article/<int:num>')
# def article(num):
#     pass
#
#
# @app.route('/users')
# def users():
#     pass
#
#
# @app.route('/category')
# def categories():
#     pass
#
#
# @app.route('/category/<int:num>')
# def category(num):
#     pass
#
# @app.route('/flow/<int:num>')
# def flow(num):
#     pass


@app.route('/write', methods=['GET', 'POST'])
@login_required
def write():
    session = create_session()
    if request.method == 'GET':
        return render('write.html')
    elif request.method == 'POST':
        print(request.args['tinymce'])
        return redirect('/')


# @app.route('/edit/<int:num>')
# @login_required
# def edit(num):
#     pass


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.errorhandler(404)
def not_found(e):
    return render('error_404.html')


@app.errorhandler(401)
def not_found(e):
    return redirect('/login')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8900)
