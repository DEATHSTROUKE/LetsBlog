from datetime import datetime
import sqlalchemy as sa
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .db_session import SqlAlchemyBase


class SubCategory(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'sub_category'
    id = sa.Column(sa.Integer,
                   primary_key=True, autoincrement=True)
    category = sa.Column(sa.Integer, sa.ForeignKey('categories.id'))
    user = sa.Column(sa.Integer, sa.ForeignKey('users.id'))
    user1 = orm.relation('User')
    category1 = orm.relation('Category')
