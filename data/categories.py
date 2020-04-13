from datetime import datetime
import sqlalchemy as sa
from flask_login import UserMixin
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .db_session import SqlAlchemyBase


class Category(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'categories'
    id = sa.Column(sa.Integer,
                   primary_key=True, autoincrement=True)
    title = sa.Column(sa.String, unique=True)
    flow = sa.Column(sa.Integer, sa.ForeignKey('flows.id'))
    category_flow = orm.relation('Flow')
    article_category = orm.relation('ArticleCategory', back_populates='category1')
