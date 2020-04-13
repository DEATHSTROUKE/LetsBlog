from datetime import datetime
import sqlalchemy as sa
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .db_session import SqlAlchemyBase


class Bookmark(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'bookmarks'
    id = sa.Column(sa.Integer,
                   primary_key=True, autoincrement=True)
    article = sa.Column(sa.Integer, sa.ForeignKey('articles.id'))
    art = orm.relation('Article')
    user_bookmark = orm.relation('UserBookmark', back_populates='bookmark1')
