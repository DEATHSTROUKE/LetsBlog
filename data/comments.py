from datetime import datetime
import sqlalchemy as sa
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .db_session import SqlAlchemyBase


class Comment(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'comments'
    id = sa.Column(sa.Integer,
                   primary_key=True, autoincrement=True)
    author = sa.Column(sa.Integer, sa.ForeignKey('users.id'))
    text = sa.Column(sa.String)
    rate = sa.Column(sa.Integer)
    date = sa.Column(sa.DateTime, default=datetime.now)
    user = orm.relation('User')
