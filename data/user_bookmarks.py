from datetime import datetime
import sqlalchemy as sa
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .db_session import SqlAlchemyBase


class UserBookmark(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'user_bookmark'
    id = sa.Column(sa.Integer,
                   primary_key=True, autoincrement=True)
    user = sa.Column(sa.Integer, sa.ForeignKey('users.id'))
    bookmark = sa.Column(sa.Integer, sa.ForeignKey('bookmarks.id'))
    user1 = orm.relation('User')
    bookmark1 = orm.relation('Bookmark')
