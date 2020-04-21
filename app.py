from flask import Flask, render_template, redirect, request, url_for, jsonify
from data import db_session
from data.db_session import global_init, create_session
from imports import *
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from datetime import datetime
import datetime
import json

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
def default():
    session = create_session()
    art = session.query(Article.id).order_by(Article.id.desc()).all()
    articles = []
    for i in art:
        article = session.query(Article).get(i)
        cats = []
        cat1 = session.query(ArticleCategory.category) \
            .filter(ArticleCategory.article == article.id).all()
        for j in cat1:
            c1 = session.query(Category).filter(Category.id == j[0]).first()
            cats.append(c1)

        sl = {
            'title': article.title,
            'preview': article.preview,
            'date_public': article.beauty_date(article.date_public),
            'author': article.user,
            'rate': article.rate if article.rate else 0,
            'id': article.id,
            'watches': article.watches,
            'cats': cats,
            'discription': article.discription if article.discription else ''
        }
        articles.append(sl)
    return render('index.html', title='Все потоки', articles=articles)


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
        login_user(user)
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


@app.route('/feed')
@login_required
def feed():
    return render('index.html', title='Моя лента')


@app.route('/users/<nick>')
def profile(nick):
    session = create_session()
    user = session.query(User).filter(User.nick == nick).first()
    if not user:
        return render('error_404.html')
    return render('profile.html', user=user, title=f'{user.nick}')


@app.route('/users/<nick>/public')
def prof_public(nick):
    session = create_session()
    user = session.query(User).filter(User.nick == nick).first()
    if not user:
        return render('error_404.html')
    return render('profile_public.html', user=user, title=f'{user.nick}')


@app.route('/users/<nick>/bookmarks')
def prof_bookmarks(nick):
    session = create_session()
    user = session.query(User).filter(User.nick == nick).first()
    if not user:
        return render('error_404.html')
    return render('profile_bookmarks.html', user=user, title=f'{user.nick}')


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
        return render('settings.html', user=user, title='Пользовательские настройки')
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


@app.route('/article/<int:num>')
def article(num):
    session = create_session()
    article = session.query(Article).filter(Article.id == num).first()
    return render('article.html', title=article.title, article=article)


@app.route('/add_comment', methods=['POST'])
def add_comment():
    return ''


@app.route('/users')
def users():
    session = create_session()
    users = session.query(User).filter(User.is_author == 1, User.id != current_user.id)
    subs1 = session.query(SubPerson.author).filter(SubPerson.user == current_user.id).all()
    subs = []
    for i in subs1:
        subs.append(i[0])
    return render('users.html', users=users, title='Авторы', subs=subs)


@app.route('/add_sub_person', methods=['POST'])
def add_sub_person():
    session = create_session()
    data = json.loads(request.data)
    data = int(data.split('=')[1])
    sub = session.query(SubPerson) \
        .filter(SubPerson.user == current_user.id, SubPerson.author == data).first()
    if sub:
        sub = session.query(SubPerson) \
            .filter(SubPerson.user == current_user.id, SubPerson.author == data).delete()
    else:
        sub = SubPerson(
            author=data,
            user=current_user.id
        )
        session.add(sub)
    session.commit()
    return request.data


@app.route('/category')
def category():
    session = create_session()
    category = session.query(Category).all()
    subs1 = session.query(SubCategory.category).filter(SubCategory.user == current_user.id).all()
    subs = []
    for i in subs1:
        subs.append(i[0])
    return render('category.html', category=category, title='Категории', subs=subs)


@app.route('/category/<int:num>')
def categories(num):
    session = create_session()
    category = session.query(Category).all()
    return render('category.html', category=category, title=f'{category.title}')


@app.route('/add_sub_category', methods=['POST'])
def add_sub_category():
    session = create_session()
    data = json.loads(request.data)
    data = int(data.split('=')[1])
    sub = session.query(SubCategory) \
        .filter(SubCategory.user == current_user.id, SubCategory.category == data).first()
    if sub:
        sub = session.query(SubCategory) \
            .filter(SubCategory.user == current_user.id, SubCategory.category == data).delete()
    else:
        sub = SubCategory(
            category=data,
            user=current_user.id
        )
        session.add(sub)
    session.commit()
    return request.data


@app.route('/add_watch', methods=['POST'])
def add_watch():
    return ''


# @app.route('/flow/<int:num>')
# def flow(num):
#     pass

@app.route('/edit/<int:num>', methods=['GET', 'POST'])
@login_required
def edit(num):
    session = create_session()
    if request.method == 'GET':
        article = session.query(Article).filter(Article.id == num).first()
        return render('edit.html', article=article, title='Редактирование')
    elif request.method == 'POST':
        return redirect(f'/users/{current_user.nick}/public')


@app.route('/write', methods=['GET', 'POST'])
@login_required
def write():
    session = create_session()
    if request.method == 'GET':
        if current_user.is_author:
            category1 = session.query(Category).order_by(Category.flow).all()
            return render('write.html', category=category1, title='Написание статьи')
        else:
            return redirect('/become_author')
    elif request.method == 'POST':
        all_keys = list(request.form.items())
        article = Article(
            title=request.form['title'],
            preview=request.form['preview'],
            author=current_user.id,
            flow=int(request.form['flow']),
            text=request.form['tinymce'],
            discription=request.form['disc']
        )
        session.add(article)
        session.commit()
        tags = request.form['tags'].split(', ')
        for i in tags:
            tag = Tag(title=i)
            session.add(tag)
            session.commit()
            art_tag = TagArticle(
                article=article.id,
                tag=tag.id
            )
            session.add(art_tag)
            session.commit()
        for i in all_keys:
            if 'cats' in i[0]:
                art_cat = ArticleCategory(
                    article=article.id,
                    category=int(i[1])
                )
                session.add(art_cat)
                session.commit()
        return redirect(f'/users/{current_user.nick}/public')


@app.route('/become_author', methods=['GET', 'POST'])
@login_required
def become_author():
    session = create_session()
    if request.method == 'GET':
        return render('become_author.html', title='Стань автором')
    else:
        user = session.query(User).filter(User.id == current_user.id).update({'is_author': 1})
        session.commit()
        return redirect('/write')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.errorhandler(404)
def not_found(e):
    return render('error_404.html')


@app.errorhandler(401)
def not_authorized(e):
    return redirect('/login')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8900)
