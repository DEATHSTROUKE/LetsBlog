from datetime import datetime
import sqlalchemy as sa
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .db_session import SqlAlchemyBase


class Flow(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'flows'
    id = sa.Column(sa.Integer,
                   primary_key=True, autoincrement=True)
    title = sa.Column(sa.String)
    article = orm.relation('Article', back_populates='art_flow')
    category = orm.relation('Category', back_populates='category_flow')
