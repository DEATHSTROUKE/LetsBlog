from datetime import datetime
import sqlalchemy as sa
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .db_session import SqlAlchemyBase


class Article(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'articles'
    id = sa.Column(sa.Integer,
                   primary_key=True, autoincrement=True)
    title = sa.Column(sa.String)
    text = sa.Column(sa.String)
    author = sa.Column(sa.Integer, sa.ForeignKey('users.id'))
    flow = sa.Column(sa.Integer, sa.ForeignKey('flows.id'))
    rate = sa.Column(sa.Integer)
    user = orm.relation('User')
    art_flow = orm.relation('Flow')
    bookmark = orm.relation('Bookmark', back_populates='art')
    art_category = orm.relation('SubCategory', back_populates='category1')
    tag_article = orm.relation('TagArticle', back_populates='article1')
    article_category = orm.relation('ArticleCategory', back_populates='article1')

