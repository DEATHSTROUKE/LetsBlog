from datetime import datetime
import sqlalchemy as sa
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .db_session import SqlAlchemyBase


class TagArticle(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'tag_article'
    id = sa.Column(sa.Integer,
                   primary_key=True, autoincrement=True)
    article = sa.Column(sa.Integer, sa.ForeignKey('articles.id'))
    tag = sa.Column(sa.Integer, sa.ForeignKey('tags.id'))
    article1 = orm.relation('Article')
    tag1 = orm.relation('Tag')
