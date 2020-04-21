import flask
from flask import jsonify, request
from imports import *
from data.db_session import create_session

blueprint = flask.Blueprint('news_api', __name__,
                            template_folder='templates')


@blueprint.route('/api/articles')
def get_articles():
    session = create_session()
    articles = session.query(Article).all()
    return jsonify({
        'articles': [item.to_dict(only=('id', 'title', 'author',
                                        'text', 'flow', 'preview',
                                        'discription', 'date_public')) for item in articles]
    })


@blueprint.route('/api/articles/<int:num>')
def get_article(num):
    session = create_session()
    articles = session.query(Article).get(num)
    if articles:
        return jsonify({
            'articles': articles.to_dict(only=('id', 'title', 'author',
                                               'text', 'flow', 'preview',
                                               'discription', 'date_public'))
        })
    else:
        return jsonify({
            'error': 'Not found'
        })


@blueprint.route('/api/users')
def get_users():
    session = create_session()
    users = session.query(User).all()
    return jsonify({
        'users': [item.to_dict(only=('id', 'surname', 'name',
                                     'nick', 'email', 'avatar',
                                     'date_born', 'date_register',
                                     'work', 'is_author')) for item in users]
    })


@blueprint.route('/api/users/<int:num>')
def get_user(num):
    session = create_session()
    users = session.query(User).get(num)
    if users:
        return jsonify({
            'users': users.to_dict(only=('id', 'surname', 'name',
                                         'nick', 'email', 'avatar',
                                         'date_born', 'date_register',
                                         'work', 'is_author'))
        })
    else:
        return jsonify({
            'error': 'Not found'
        })
